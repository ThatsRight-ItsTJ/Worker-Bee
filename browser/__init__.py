from browser.logging_config import setup_logging

setup_logging()

from browser.browser.browser import Browser as Browser
from browser.browser.browser import BrowserConfig as BrowserConfig
from browser.dom.service import DomService as DomService
from browser.tools.browser_tools import (
    SearchGoogle,
    GoToUrl,
    GoBack,
    ClickElement,
    InputText,
    SwitchTab,
    OpenTab,
    ExtractContent,
    ScrollDown,
    ScrollUp,
    SendKeys,
    ScrollToText,
    GetDropdownOptions,
    SelectDropdownOption
)

from browser.tools.ops_tools import submit_result, think, raise_error

__all__ = [
	'Browser',
	'BrowserConfig',
	'DomService',
	'SearchGoogle',
	'GoToUrl',
	'GoBack',
	'ClickElement',
	'InputText',
	'SwitchTab',
	'OpenTab',
	'ExtractContent',
	'ScrollDown',
	'ScrollUp',
	'SendKeys',
	'ScrollToText',
	'GetDropdownOptions',
	'SelectDropdownOption',
	'submit_result',
	'think',
	'raise_error'
]
