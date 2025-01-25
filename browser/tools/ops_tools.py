
from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import List, Annotated
from langgraph.types import Command
from langchain_core.tools.base import InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langchain_core.messages import ToolMessage

class AnswerSchema(BaseModel):
    ops_summary: str = Field(description="The summary of the operations you performed to find the information")
    answer: str = Field(description="The final answer to the user's request")
    sources: List[str] = Field(description="The sources you used to find the information")
    quotes: List[str] = Field(description="The quotes you found")
    tool_call_id: Annotated[str, InjectedToolCallId]


@tool(args_schema=AnswerSchema)
def submit_result(ops_summary: str, 
                  answer: str,
                  sources: List[str],
                  quotes: List[str],
                  tool_call_id: Annotated[str, InjectedToolCallId]):
    """Submit the final output of your search. Must be informative and specific."""
    final_output = {"answer": answer, 
                    "quotes": quotes, 
                    "sources": sources}
    return Command(update={"final_output": final_output, 
                           "messages": [ToolMessage(content=ops_summary, 
                                        tool_call_id=tool_call_id
                                        )]})

@tool
def raise_error(error_message: str, 
                tool_call_id: Annotated[str, InjectedToolCallId]):
    """Raise an error. Use this tool if you are absolutely sure that no relevant information can be found on this URL, or any other critical error occurs."""
    return Command(update={"final_output": error_message, 
                           "messages": [ToolMessage(content=error_message, 
                                        tool_call_id=tool_call_id
                                        )]})


class ThinkSchema(BaseModel):
    current_situation: str = Field(description="The current situation")
    analysis: str = Field(description="The analysis of the current situation")
    next_steps: str = Field(description="The next steps to take")
    tools_to_call: str = Field(description="Explain what tools you will need to call to execute the next steps")


@tool(args_schema=ThinkSchema)
def think(current_situation: str, \
          analysis: str, 
          next_steps: str, 
          tools_to_call: str):
    """Return helpful ideas and thoughts. This tool helps you make right decisions. Call this tool when you have doubts about your next steps."""
    return None


@tool
def open_file(file_path: str, 
              state: Annotated[dict, InjectedState], 
              tool_call_id: Annotated[str, InjectedToolCallId]):
    """Open a file. This tool opens a given file. If the file is a PDF, it will be converted to a set of images and provided to you inside a message from the user."""
    registry = state.get("downloads")
    message = registry.open_file(file_path) # type: ignore
    return Command(update={"toolmessage_sub": message, 
                           "messages": [ToolMessage(content="The file has been opened, and will be provided to you in the next message.", 
                                        tool_call_id=tool_call_id
                                        )]})