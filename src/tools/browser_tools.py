import asyncio
import json
import logging

from pydantic import BaseModel, Field
from typing import Type, Annotated
from dataclasses import dataclass
from typing import Any, Dict, Optional, List, Tuple, Dict
from src.browser.context import BrowserContext, BrowserState

from langchain_core.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from langgraph.prebuilt import InjectedState

from .examples import BROWSER_STATE_EXAMPLES, DATA_LOG_EXAMPLES

logger = logging.getLogger(__name__)

# utils

async def format_output(context: BrowserContext, 
						action_status: str,
						browser_state_description: str,
						relevant_data: str
						) -> Tuple[List[dict], Dict[str, List[dict]]]:
	
	state: BrowserState = await context.get_state()
	selector_map = [f"""Element index: {index}, Element metadata: {element}""" for index, element in state.selector_map.items()]
	selector_map = "\n".join(selector_map)
	main_output = [
			{
				"type": "text", "text": f"{action_status}"
			}
		]
	screenshot_output = [
			{
				"type": "text",
				"text": "I attached the current browser viewport. Also, for your convinience I add the textual representation of all interactive elements too: " + selector_map
			},
			{
				"type": "image_url",
				"image_url": {"url": f"data:image/jpeg;base64,{state.screenshot}"},
			}
		]
	action_record = {
						"url": state.url, 
						"title": state.title, 
						"browser_state_description": browser_state_description, 
						"relevant_data": relevant_data
					}
	artifacts = {
					"screenshot": screenshot_output, 
					"action_record": action_record
				}
	logger.info(action_status)
	return main_output, artifacts

class BrowserToolInput(BaseModel):
	browser_state_description: str = Field(description="Provide observations about the current state of the browser. What happens on the screen? Examples: " + BROWSER_STATE_EXAMPLES)
	relevant_data: str = Field(description="If you found any relevant data or clues that will be a part of the final output, please log it here. Examples: " + DATA_LOG_EXAMPLES)
	reasoning: str = Field(description="Explain: Why are you calling this tool? Why did you decide to input the following arguments?")

# tools

class SearchGoogleInput(BrowserToolInput):
	query: str = Field(description="The query to search for in Google")
	state: Annotated[dict, InjectedState]

class SearchGoogle(BaseTool):
	name: str = "search_google"
	description: str = "This tool opens Google in browser and searches for the given query. Returns a screenshot of the search results."
	args_schema: Type[BaseModel] = SearchGoogleInput
	return_direct: bool = False
	tags: list[str] = ["browser_context"]
	response_format: str = "content_and_artifact"

	def _run(self, *args, relevant_data: str, reasoning: str, **kwargs):
		raise NotImplementedError("Tool does not support sync")

	async def _arun(
		self, 
		query: str,
		state: dict,
		relevant_data: str,
		reasoning: str,
		browser_state_description: str,
		run_manager: Optional[CallbackManagerForToolRun] = None
	) -> Tuple[List[dict], Dict[str, List[dict]]]:
		browser: BrowserContext = state["browser_context"]
		page = await browser.get_current_page()
		await page.goto(f'https://www.google.com/search?q={query}&udm=14')
		await page.wait_for_load_state()
		content, artifacts = await format_output(browser, f'Searched for "{query}" in Google has been successfully performed.', browser_state_description, relevant_data)
		return content, artifacts

# Basic Navigation Actions

class GoToUrlInput(BrowserToolInput):
	url: str = Field(description="The URL to navigate to")
	state: Annotated[dict, InjectedState]

class GoToUrl(BaseTool):
	name: str = "go_to_url"
	description: str = "This tool navigates to the specified URL in the browser and waits for the page to load."
	args_schema: Type[BaseModel] = GoToUrlInput
	return_direct: bool = False
	tags: list[str] = ["browser_context"]
	response_format: str = "content_and_artifact"

	def _run(self, *args, relevant_data: str, reasoning: str, **kwargs):
		raise NotImplementedError("Tool does not support sync")

	async def _arun(
		self,
		url: str,
		state: dict,
		relevant_data: str,
		reasoning: str,
		browser_state_description: str,
		run_manager: Optional[CallbackManagerForToolRun] = None
	) -> Tuple[List[dict], Dict[str, List[dict]]]:
		browser: BrowserContext = state["browser_context"]
		page = await browser.get_current_page()
		await page.goto(url)
		await page.wait_for_load_state()
		content, artifacts = await format_output(browser, f'🔗  Navigated to {url}', browser_state_description, relevant_data)
		return content, artifacts

class GoBackInput(BrowserToolInput):
	state: Annotated[dict, InjectedState]

class GoBack(BaseTool):
	name: str = "go_back"
	description: str = "This tool navigates back to the previous page in the browser history and waits for the page to load."
	args_schema: Type[BaseModel] = GoBackInput
	return_direct: bool = False
	tags: list[str] = ["browser_context"]
	response_format: str = "content_and_artifact"

	def _run(self, *args, relevant_data: str, reasoning: str, **kwargs):
		raise NotImplementedError("Tool does not support sync")

	async def _arun(
		self,
		state: dict,
		relevant_data: str,
		reasoning: str,
		browser_state_description: str,
		run_manager: Optional[CallbackManagerForToolRun] = None
	) -> Tuple[List[dict], Dict[str, List[dict]]]:
		browser: BrowserContext = state["browser_context"]
		page = await browser.get_current_page()
		await page.go_back()
		await page.wait_for_load_state()
		content, artifacts = await format_output(browser, '🔙  Navigated back', browser_state_description, relevant_data)
		return content, artifacts

# Element Interaction Actions
class ClickElementInput(BrowserToolInput):
	index: int = Field(description="The index of the element to click")
	state: Annotated[dict, InjectedState]
	xpath: Optional[str] = Field(default=None, description="Optional xpath to identify the element")

class ClickElement(BaseTool):
	name: str = "click_element"
	description: str = "This tool clicks on an element identified by its index in the browser and handles any resulting actions like new tab creation."
	args_schema: Type[BaseModel] = ClickElementInput
	return_direct: bool = False
	tags: list[str] = ["browser_context"]
	response_format: str = "content_and_artifact"
	
	def _run(self, *args, relevant_data: str, reasoning: str, **kwargs):
		raise NotImplementedError("Tool does not support sync")

	async def _arun(
		self,
		index: int,
		state: dict,
		relevant_data: str,
		reasoning: str,
		browser_state_description: str,
		xpath: Optional[str] = None,
		run_manager: Optional[CallbackManagerForToolRun] = None
	) -> Tuple[List[dict], Dict[str, List[dict]]]:
		
		browser: BrowserContext = state["browser_context"]
		session = await browser.get_session()
		browser_state = session.cached_state

		if index not in browser_state.selector_map:
			raise Exception(f'Element with index {index} does not exist - retry or use alternative actions')

		element_node = browser_state.selector_map[index]
		initial_pages = len(session.context.pages)

		# if element has file uploader then dont click
		if await browser.is_file_uploader(element_node):
			raise Exception(f'Index {index} - has an element which opens file upload dialog. To upload files please use a specific function to upload files')

		try:
			await browser._click_element_node(element_node)
			msg = f'Clicked button with index {index}: {element_node.get_all_text_till_next_clickable_element(max_depth=2)}'

			logger.debug(f'Element xpath: {element_node.xpath}')
			if len(session.context.pages) > initial_pages:
				new_tab_msg = 'New tab opened - switching to it'
				msg += f' - {new_tab_msg}'
				logger.info(new_tab_msg)
				await browser.switch_to_tab(-1)
			
			content, artifacts = await format_output(browser, msg, browser_state_description, relevant_data)
			return content, artifacts
		
		except Exception as e:
			logger.warning(f'Element no longer available with index {index} - most likely the page changed')
			content, artifacts = await format_output(browser, f'Error: {str(e)}', browser_state_description, relevant_data)
			return content, artifacts

class InputTextInput(BrowserToolInput):
	index: int = Field(description="The index of the element to input text into")
	text: str = Field(description="The text to input into the element")
	state: Annotated[dict, InjectedState]
	xpath: Optional[str] = Field(default=None, description="Optional xpath to identify the element")

class InputText(BaseTool):
	name: str = "input_text"
	description: str = "This tool inputs text into an element identified by its index in the browser."
	args_schema: Type[BaseModel] = InputTextInput
	return_direct: bool = False
	tags: list[str] = ["browser_context"]
	response_format: str = "content_and_artifact"

	def _run(self, *args, relevant_data: str, reasoning: str, **kwargs):
		raise NotImplementedError("Tool does not support sync")

	async def _arun(
		self,
		index: int,
		text: str,
		state: dict,
		relevant_data: str,
		reasoning: str,
		browser_state_description: str,
		xpath: Optional[str] = None,
		run_manager: Optional[CallbackManagerForToolRun] = None
	) -> Tuple[List[dict], Dict[str, List[dict]]]:
		browser = state["browser_context"]
		session = await browser.get_session()
		browser_state = session.cached_state

		if index not in browser_state.selector_map:
			raise Exception(f'Element index {index} does not exist - retry or use alternative actions')

		element_node = browser_state.selector_map[index]
		await browser._input_text_element_node(element_node, text)
		msg = f'Input "{text}" into index {index}'
		logger.debug(f'Element xpath: {element_node.xpath}')
		content, artifacts = await format_output(browser, msg, browser_state_description, relevant_data)
		return content, artifacts

# Tab Management Actions
class SwitchTabInput(BrowserToolInput):
	page_id: int = Field(description="The ID of the tab to switch to")
	state: Annotated[dict, InjectedState]

class SwitchTab(BaseTool):
	name: str = "switch_tab"
	description: str = "This tool switches to a different browser tab specified by its ID and waits for the page to load."
	args_schema: Type[BaseModel] = SwitchTabInput
	return_direct: bool = False
	tags: list[str] = ["browser_context"]
	response_format: str = "content_and_artifact"

	def _run(self, *args, relevant_data: str, reasoning: str, **kwargs):
		raise NotImplementedError("Tool does not support sync")

	async def _arun(
		self,
		page_id: int,
		state: dict,
		relevant_data: str,
		reasoning: str,
		browser_state_description: str,
		run_manager: Optional[CallbackManagerForToolRun] = None
	) -> Tuple[List[dict], Dict[str, List[dict]]]:
		browser = state["browser_context"]
		await browser.switch_to_tab(page_id)
		# Wait for tab to be ready
		page = await browser.get_current_page()
		await page.wait_for_load_state()
		content, artifacts = await format_output(browser, f'Switched to tab {page_id}', browser_state_description, relevant_data)
		return content, artifacts

class OpenTabInput(BrowserToolInput):
	url: str = Field(description="The URL to open in the new tab")
	state: Annotated[dict, InjectedState]

class OpenTab(BaseTool):
	name: str = "open_tab"
	description: str = "This tool creates a new browser tab and navigates to the specified URL."
	args_schema: Type[BaseModel] = OpenTabInput
	return_direct: bool = False
	tags: list[str] = ["browser_context"]
	response_format: str = "content_and_artifact"

	def _run(self, *args, relevant_data: str, reasoning: str, **kwargs):
		raise NotImplementedError("Tool does not support sync")

	async def _arun(
		self,
		url: str,
		state: dict,
		relevant_data: str,
		reasoning: str,
		browser_state_description: str,
		run_manager: Optional[CallbackManagerForToolRun] = None
	) -> Tuple[List[dict], Dict[str, List[dict]]]:
		browser = state["browser_context"]
		await browser.create_new_tab(url)
		content, artifacts = await format_output(browser, f'Opened new tab with {url}', browser_state_description, relevant_data)
		return content, artifacts

# Content Actions
class ExtractContentInput(BrowserToolInput):
	include_links: bool = Field(description="Whether to include links in the extracted content (markdown format) or just text")
	state: Annotated[dict, InjectedState]

class ExtractContent(BaseTool):
	name: str = "extract_content"
	description: str = "This tool extracts the content from the current page, either as markdown (with links) or plain text."
	args_schema: Type[BaseModel] = ExtractContentInput
	return_direct: bool = False
	tags: list[str] = ["browser_context"]
	response_format: str = "content_and_artifact"

	def _run(self, *args, relevant_data: str, reasoning: str, **kwargs):
		raise NotImplementedError("Tool does not support sync")

	async def _arun(
		self,
		include_links: bool,
		state: dict,
		relevant_data: str,
		reasoning: str,
		browser_state_description: str,
		run_manager: Optional[CallbackManagerForToolRun] = None
	) -> Tuple[List[dict], Dict[str, List[dict]]]:
		browser = state["browser_context"]
		page = await browser.get_current_page()
		output_format = 'markdown' if include_links else 'text'
		content = MainContentExtractor.extract(  # type: ignore
			html=await page.content(),
			output_format=output_format,
		)
		content, artifacts = await format_output(browser, f'Extracted page as {output_format}\n: {content}\n', browser_state_description, relevant_data)
		return content, artifacts

class ScrollDownInput(BrowserToolInput):
	state: Annotated[dict, InjectedState]
	amount: Optional[int] = Field(default=None, description="Amount of pixels to scroll down. If not specified, scrolls down one page")

class ScrollDown(BaseTool):
	name: str = "scroll_down"
	description: str = "This tool scrolls down the page by a specified amount of pixels or by one page if no amount is specified."
	args_schema: Type[BaseModel] = ScrollDownInput
	return_direct: bool = False
	tags: list[str] = ["browser_context"]
	response_format: str = "content_and_artifact"
	def _run(self, *args, relevant_data: str, reasoning: str, **kwargs):
		raise NotImplementedError("Tool does not support sync")

	async def _arun(
		self,
		state: dict,
		relevant_data: str,
		reasoning: str,
		browser_state_description: str,
		amount: Optional[int] = None,
		run_manager: Optional[CallbackManagerForToolRun] = None
	) -> Tuple[List[dict], Dict[str, List[dict]]]:
		browser = state["browser_context"]
		page = await browser.get_current_page()
		if amount is not None:
			await page.evaluate(f'window.scrollBy(0, {amount});')
		else:
			await page.keyboard.press('PageDown')

		amount_str = f'{amount} pixels' if amount is not None else 'one page'
		content, artifacts = await format_output(browser, f'🔍  Scrolled down the page by {amount_str}', browser_state_description, relevant_data)
		return content, artifacts

# scroll up
class ScrollUpInput(BrowserToolInput):
	state: Annotated[dict, InjectedState]
	amount: Optional[int] = Field(default=None, description="Amount of pixels to scroll up. If not specified, scrolls up one page")

class ScrollUp(BaseTool):
	name: str = "scroll_up"
	description: str = "This tool scrolls up the page by a specified amount of pixels or by one page if no amount is specified."
	args_schema: Type[BaseModel] = ScrollUpInput
	return_direct: bool = False
	tags: list[str] = ["browser_context"]
	response_format: str = "content_and_artifact"
	def _run(self, *args, relevant_data: str, reasoning: str, **kwargs):
		raise NotImplementedError("Tool does not support sync")

	async def _arun(
		self,
		state: dict,
		relevant_data: str,
		reasoning: str,
		browser_state_description: str,
		amount: Optional[int] = None,
		run_manager: Optional[CallbackManagerForToolRun] = None
	) -> Tuple[List[dict], Dict[str, List[dict]]]:
		browser = state["browser_context"]
		page = await browser.get_current_page()
		if amount is not None:
			await page.evaluate(f'window.scrollBy(0, -{amount});')
		else:
			await page.keyboard.press('PageUp')

		amount_str = f'{amount} pixels' if amount is not None else 'one page'
		content, artifacts = await format_output(browser, f'🔍  Scrolled up the page by {amount_str}', browser_state_description, relevant_data)
		return content, artifacts

# send keys
class SendKeysInput(BrowserToolInput):
	keys: str = Field(description="The keys to send to the page")
	state: Annotated[dict, InjectedState]

class SendKeys(BaseTool):
	name: str = "send_keys"
	description: str = "This tool sends keyboard keys to the current page."
	args_schema: Type[BaseModel] = SendKeysInput
	return_direct: bool = False
	tags: list[str] = ["browser_context"]
	response_format: str = "content_and_artifact"
	def _run(self, *args, relevant_data: str, reasoning: str, **kwargs):
		raise NotImplementedError("Tool does not support sync")

	async def _arun(
		self,
		keys: str,
		state: dict,
		relevant_data: str,
		reasoning: str,
		browser_state_description: str,
		run_manager: Optional[CallbackManagerForToolRun] = None
	) -> Tuple[List[dict], Dict[str, List[dict]]]:
		browser = state["browser_context"]
		page = await browser.get_current_page()
		await page.keyboard.press(keys)
		content, artifacts = await format_output(browser, f'⌨️  Sent keys: {keys}', browser_state_description, relevant_data)
		return content, artifacts

class ScrollToTextInput(BrowserToolInput):
	text: str = Field(description="The text to scroll to on the page")
	state: Annotated[dict, InjectedState]

class ScrollToText(BaseTool):
	name: str = "scroll_to_text"
	description: str = "This tool scrolls the page to make the specified text visible, trying different locator strategies."
	args_schema: Type[BaseModel] = ScrollToTextInput
	return_direct: bool = False
	tags: list[str] = ["browser_context"]
	response_format: str = "content_and_artifact"

	def _run(self, *args, relevant_data: str, reasoning: str, **kwargs):
		raise NotImplementedError("Tool does not support sync")

	async def _arun(
		self,
		text: str,
		state: dict,
		relevant_data: str,
		reasoning: str,
		browser_state_description: str,
		run_manager: Optional[CallbackManagerForToolRun] = None
		) -> Tuple[List[dict], Dict[str, List[dict]]]:
		browser = state["browser_context"]
		page = await browser.get_current_page()
		try:
			# Try different locator strategies
			locators = [
				page.get_by_text(text, exact=False),
				page.locator(f'text={text}'),
				page.locator(f"//*[contains(text(), '{text}')]"),
			]

			for locator in locators:
				try:
					# First check if element exists and is visible
					if await locator.count() > 0 and await locator.first.is_visible():
						await locator.first.scroll_into_view_if_needed()
						await asyncio.sleep(0.5)  # Wait for scroll to complete
						content, artifacts = await format_output(browser, f'🔍  Scrolled to text: {text}', browser_state_description, relevant_data)
						return content, artifacts
				except Exception as e:
					logger.debug(f'Locator attempt failed: {str(e)}')
					continue

			content, artifacts = await format_output(browser, f"Text '{text}' not found or not visible on page", browser_state_description, relevant_data)
			return content, artifacts

		except Exception as e:
			logger.error(f"Failed to scroll to text '{text}': {str(e)}")
			content, artifacts = await format_output(browser, f"Error: {str(e)}", browser_state_description, relevant_data)
			return content, artifacts

class GetDropdownOptionsInput(BrowserToolInput):
	index: int = Field(description="The index of the dropdown element to get options from")
	state: Annotated[dict, InjectedState]

class GetDropdownOptions(BaseTool):
	name: str = "get_dropdown_options"
	description: str = "This tool gets all options from a native dropdown element identified by its index."
	args_schema: Type[BaseModel] = GetDropdownOptionsInput
	return_direct: bool = False
	tags: list[str] = ["browser_context"]
	response_format: str = "content_and_artifact"

	def _run(self, *args, relevant_data: str, reasoning: str, **kwargs):
		raise NotImplementedError("Tool does not support sync")

	async def _arun(
		self,
		index: int,
		state: dict,
		relevant_data: str,
		reasoning: str,
		browser_state_description: str,
		run_manager: Optional[CallbackManagerForToolRun] = None
	) -> Tuple[List[dict], Dict[str, List[dict]]]:
		browser = state["browser_context"]
		page = await browser.get_current_page()
		selector_map = await browser.get_selector_map()
		dom_element = selector_map[index]

		try:
			# Frame-aware approach since we know it works
			all_options = []
			frame_index = 0

			for frame in page.frames:
				try:
					options = await frame.evaluate(
						"""
						(xpath) => {
							const select = document.evaluate(xpath, document, null,
								XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
							if (!select) return null;

							return {
								options: Array.from(select.options).map(opt => ({
									text: opt.text, //do not trim, because we are doing exact match in select_dropdown_option
									value: opt.value,
									index: opt.index
								})),
								id: select.id,
								name: select.name
							};
						}
						""",
						dom_element.xpath,
					)

					if options:
						logger.debug(f'Found dropdown in frame {frame_index}')
						logger.debug(f'Dropdown ID: {options["id"]}, Name: {options["name"]}')

						formatted_options = []
						for opt in options['options']:
							# encoding ensures AI uses the exact string in select_dropdown_option
							encoded_text = json.dumps(opt['text'])
							formatted_options.append(f'{opt["index"]}: text={encoded_text}')

						all_options.extend(formatted_options)

				except Exception as frame_e:
					logger.debug(f'Frame {frame_index} evaluation failed: {str(frame_e)}')

				frame_index += 1

			if all_options:
				msg = '\n'.join(all_options)
				msg += '\nUse the exact text string in select_dropdown_option'
				content, artifacts = await format_output(browser, msg, browser_state_description, relevant_data)
				return content, artifacts
			else:
				content, artifacts = await format_output(browser, 'No options found in any frame for dropdown', browser_state_description, relevant_data)
				return content, artifacts

		except Exception as e:
			logger.error(f'Failed to get dropdown options: {str(e)}')
			content, artifacts = await format_output(browser, f'Error getting options: {str(e)}', browser_state_description, relevant_data)
			return content, artifacts

class SelectDropdownOptionInput(BrowserToolInput):
	index: int = Field(description="The index of the dropdown element")
	text: str = Field(description="The text of the option to select")
	state: Annotated[dict, InjectedState]

class SelectDropdownOption(BaseTool):
	name: str = "select_dropdown_option"
	description: str = "This tool selects an option from a dropdown element by its text value."
	args_schema: Type[BaseModel] = SelectDropdownOptionInput
	return_direct: bool = False
	tags: list[str] = ["browser_context"]
	response_format: str = "content_and_artifact"
	def _run(self, *args, relevant_data: str, reasoning: str, **kwargs):
		raise NotImplementedError("Tool does not support sync")

	async def _arun(
		self,
		index: int,
		text: str,
		state: dict,
		relevant_data: str,
		reasoning: str,
		browser_state_description: str,
		run_manager: Optional[CallbackManagerForToolRun] = None
	) -> Tuple[List[dict], Dict[str, List[dict]]]:
		browser = state["browser_context"]
		page = await browser.get_current_page()
		selector_map = await browser.get_selector_map()
		dom_element = selector_map[index]

		# Validate that we're working with a select element
		if dom_element.tag_name != 'select':
			logger.error(f'Element is not a select! Tag: {dom_element.tag_name}, Attributes: {dom_element.attributes}')
			t, images = await format_output(browser, f'Cannot select option: Element with index {index} is a {dom_element.tag_name}, not a select', browser_state_description, relevant_data)
			return t, images

		logger.debug(f"Attempting to select '{text}' using xpath: {dom_element.xpath}")
		logger.debug(f'Element attributes: {dom_element.attributes}')
		logger.debug(f'Element tag: {dom_element.tag_name}')

		try:
			frame_index = 0
			for frame in page.frames:
				try:
					logger.debug(f'Trying frame {frame_index} URL: {frame.url}')

					# First verify we can find the dropdown in this frame
					find_dropdown_js = """
						(xpath) => {
							try {
								const select = document.evaluate(xpath, document, null,
									XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
								if (!select) return null;
								if (select.tagName.toLowerCase() !== 'select') {
									return {
										error: `Found element but it's a ${select.tagName}, not a SELECT`,
										found: false
									};
								}
								return {
									id: select.id,
									name: select.name,
									found: true,
									tagName: select.tagName,
									optionCount: select.options.length,
									currentValue: select.value,
									availableOptions: Array.from(select.options).map(o => o.text.trim())
								};
							} catch (e) {
								return {error: e.toString(), found: false};
							}
						}
					"""

					dropdown_info = await frame.evaluate(find_dropdown_js, dom_element.xpath)

					if dropdown_info:
						if not dropdown_info.get('found'):
							logger.error(f'Frame {frame_index} error: {dropdown_info.get("error")}')
							continue

						logger.debug(f'Found dropdown in frame {frame_index}: {dropdown_info}')

						selected_option_values = await frame.locator('//' + dom_element.xpath).nth(0).select_option(label=text, timeout=1000)
						msg = f'Selected option {text} with value {selected_option_values}'
						logger.info(msg + f' in frame {frame_index}')
						t, images = await format_output(browser, msg, browser_state_description, relevant_data)
						return t, images

				except Exception as frame_e:
					logger.error(f'Frame {frame_index} attempt failed: {str(frame_e)}')
					logger.error(f'Frame type: {type(frame)}')
					logger.error(f'Frame URL: {frame.url}')

				frame_index += 1

			content, artifacts = await format_output(browser, f"Could not select option '{text}' in any frame", browser_state_description, relevant_data)
			return content, artifacts

		except Exception as e:
			msg = f'Selection failed: {str(e)}'
			logger.error(msg)
			content, artifacts = await format_output(browser, msg, browser_state_description, relevant_data)
			return content, artifacts
