
import logging
from typing import Annotated
from typing import List, Literal
from typing_extensions import TypedDict
import uuid

from langchain_core.messages import AnyMessage, SystemMessage, AIMessage, HumanMessage, RemoveMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, AIMessagePromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from browser.browser.context import BrowserContext, BrowserContextConfig
from browser.browser.browser import Browser
from browser.tools.browser_tools import GoToUrl, ClickElement, InputText, GoBack
from browser.tools.ops_tools import submit_result, think, raise_error, open_file
from prompts import REACT_PROMPT, CONCLUSIONS_TEMPLATE, LOG_MESSAGE_TEMPLATE, PUNISHMENT_MESSAGE_TEMPLATE, USER_INPUT_TEMPLATE

from llm_clients import llm
from langgraph.types import Command

logger = logging.getLogger(__name__)

browser = Browser()

class AgentInput(TypedDict):
    query: str
    url: str

class AgentOutput(TypedDict):
    final_output: str

class AgentState(TypedDict):
    browser: BrowserContext
    messages: Annotated[List[AnyMessage], add_messages]
    query: str
    final_output: str
    toolmessage_sub: AnyMessage

class OverallState(AgentState, AgentInput, AgentOutput):
    pass

graph = StateGraph(OverallState, input=AgentInput, output=AgentOutput)

tools = [GoToUrl(), ClickElement(), InputText(), GoBack(), submit_result, think, raise_error, open_file]

tool_node = ToolNode(tools)

# nodes

@graph.add_node
def build_browser(state: OverallState
                  ) -> Command[Literal["agent"]]:
    
    config = BrowserContextConfig(
        browser_window_size={"width": 1280, "height": 1100},
        highlight_elements=True
    )
    context = BrowserContext(browser, config)
    message = HumanMessagePromptTemplate.from_template(USER_INPUT_TEMPLATE)
    message = message.format(query=state['query'], url=state['url'])
    return Command(goto="agent", 
                   update={"browser": context, 
                           "messages": [message]})

@graph.add_node
def agent_preprocessing(state: OverallState):
    downloads = state["browser"].downloads.items
    new_downloads = [f"""
                     New file {item.name} has been downloaded, path: {item.fullpath}. 
                     Use tool 'open_file' to access it using the path as an argument.
                     """ 
                     for item in downloads if not item._notification_sent]
    if new_downloads:
        notification = SystemMessage(content="\n".join(new_downloads))
        for item in downloads:
            setattr(item, "_notification_sent", True)
        return Command(goto="agent", 
                       update={"messages": [notification]})
    if toolmessage_sub := state.get('toolmessage_sub'):
        return Command(goto="agent", 
                       update={"messages": [toolmessage_sub], 
                               "toolmessage_sub": None})
    return Command(goto="agent")


@graph.add_node
def agent(state: OverallState,
          config: RunnableConfig
          ) -> Command[Literal["tools", 
                               "agent", 
                               END]]: # type: ignore

    if state.get('final_output'):
        return Command(goto=END)

    available_files = state["browser"].downloads.state
    system = SystemMessagePromptTemplate.from_template(REACT_PROMPT)
    model = llm.with_config(config=config
              ).bind_tools(tools)
    history = state.get('messages') or []
    chat = ChatPromptTemplate.from_messages(
            [system, 
            MessagesPlaceholder('history')
            ]
        )
    response = (chat | model).invoke({"history": history, 
                                      "files": available_files})
    
    # routing tree
    if response.tool_calls: # type: ignore
        tool_call = response.tool_calls[0] # type: ignore

        # think tool doesn't need a tool node. instead we just turn it's args into an ai message and loop back to the agent node
        if tool_call.get("name") == "think": # type: ignore
            template = AIMessagePromptTemplate.from_template(CONCLUSIONS_TEMPLATE)
            payload = tool_call["args"] # type: ignore
            message = template.format(**payload)

            return Command(goto="agent", 
                           update={"messages": [message]})
        
        else:
            return Command(goto="tools", 
                           update={"messages": [response]})
        
    # if the response doesn't have tool calls, we add punishment message to the messages and go back to the agent node
    punishment_message = SystemMessage(content=PUNISHMENT_MESSAGE_TEMPLATE)
    return Command(goto="agent", 
                   update={"messages": [response, punishment_message]})


@graph.add_node
def message_splitter(state: AgentState
                     ) -> Command[Literal["agent"]]:
    last_message = state['messages'][-1]
    prev_screen = [message for message in state['messages'] 
                   if message.additional_kwargs.get("label", "") == "browser_screen"]
    
    if artifacts := last_message.artifact: # type: ignore
        screenshot = artifacts.get("screenshot")
        action_record = artifacts.get("action_record")

        new_screen = [HumanMessage(content=screenshot, 
                                   additional_kwargs={"label": "browser_screen"})]
        if prev_screen:
            log_message_template = LOG_MESSAGE_TEMPLATE.format(**action_record)
            log_message = SystemMessage(content=log_message_template, 
                                        id=prev_screen[0].id)
            new_screen.append(log_message) # type: ignore
            
        return Command(goto="agent_preprocessing", 
                       update={"messages": new_screen})
    
    return Command(goto="agent_preprocessing")

# @graph.add_node
# def process_downloads(state: AgentState
#                    ) -> Command[Literal["agent"]]:
    
#     return 

graph.set_entry_point("build_browser")
graph.add_node("tools", tool_node)
graph.add_edge("tools", "message_splitter")

app = graph.compile()
