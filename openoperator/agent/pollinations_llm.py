import json
import logging
import os
from typing import Any, Dict, Iterator, List, Optional, Type, Sequence

import requests
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool
from pydantic import Field

logger = logging.getLogger(__name__)


class PollinationsChatModel(BaseChatModel):
    """Pollinations AI chat model using their OpenAI-compatible endpoint."""
    
    model_name: str = Field(default="openai", description="Model name to use")
    base_url: str = Field(default="https://text.pollinations.ai/openai", description="Base URL for Pollinations API")
    temperature: float = Field(default=0.7, description="Temperature for generation")
    max_tokens: int = Field(default=1000, description="Maximum tokens to generate")
    timeout: int = Field(default=60, description="Request timeout in seconds")
    api_key: Optional[str] = Field(default=None, description="Optional Pollinations API key")
    referrer: Optional[str] = Field(default=None, description="Optional referrer for authentication")
    bound_tools: List[Dict[str, Any]] = Field(default_factory=list, description="Tools bound to this model")
    
    def __init__(self, **kwargs):
        # Auto-load from environment if not provided
        if 'api_key' not in kwargs:
            kwargs['api_key'] = os.getenv('POLLINATIONS_API_KEY')
        if 'referrer' not in kwargs:
            kwargs['referrer'] = os.getenv('POLLINATIONS_REFERRER')
        super().__init__(**kwargs)
    
    @property
    def _llm_type(self) -> str:
        return "pollinations"
    
    def bind_tools(
        self,
        tools: Sequence[BaseTool],
        **kwargs: Any,
    ) -> "PollinationsChatModel":
        """Bind tools to the model for function calling."""
        formatted_tools = []
        for tool in tools:
            if hasattr(tool, 'args_schema') and tool.args_schema:
                # Convert LangChain tool to OpenAI format
                openai_tool = convert_to_openai_tool(tool)
                formatted_tools.append(openai_tool)
            else:
                # Fallback for tools without proper schema
                formatted_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                })
        
        return self.__class__(
            model_name=self.model_name,
            base_url=self.base_url,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=self.timeout,
            api_key=self.api_key,
            referrer=self.referrer,
            bound_tools=formatted_tools,
            **kwargs
        )
    
    def _convert_messages_to_pollinations_format(self, messages: List[BaseMessage]) -> List[Dict[str, Any]]:
        """Convert LangChain messages to Pollinations format."""
        converted = []
        
        for message in messages:
            if isinstance(message, SystemMessage):
                converted.append({"role": "system", "content": message.content})
            elif isinstance(message, HumanMessage):
                converted.append({"role": "user", "content": message.content})
            elif isinstance(message, AIMessage):
                converted.append({"role": "assistant", "content": message.content})
            else:
                # Fallback for other message types
                converted.append({"role": "user", "content": str(message.content)})
        
        return converted
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate a response using Pollinations API."""
        
        # Convert messages to Pollinations format
        pollinations_messages = self._convert_messages_to_pollinations_format(messages)
        
        # Prepare request payload
        payload = {
            "model": self.model_name,
            "messages": pollinations_messages,
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
        }
        
        # Add tools if bound
        if self.bound_tools:
            payload["tools"] = self.bound_tools
            payload["tool_choice"] = "auto"
        
        # Add stop sequences if provided
        if stop:
            payload["stop"] = stop
            
        # Add authentication if available
        if self.referrer:
            payload["referrer"] = self.referrer
        
        headers = {"Content-Type": "application/json"}
        
        # Add API key authentication if available
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            logger.debug(f"Making request to Pollinations API with payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            
            result = response.json()
            logger.debug(f"Received response: {json.dumps(result, indent=2)}")
            
            # Extract content from response
            if "choices" in result and len(result["choices"]) > 0:
                choice = result["choices"][0]
                message_data = choice["message"]
                
                # Handle tool calls if present
                if "tool_calls" in message_data and message_data["tool_calls"]:
                    logger.debug(f"Tool calls detected: {message_data['tool_calls']}")
                    message = AIMessage(
                        content=message_data.get("content", ""),
                        tool_calls=message_data["tool_calls"]
                    )
                else:
                    content = message_data.get("content", "")
                    if not content:
                        logger.warning("Empty content received from Pollinations API")
                        content = "I apologize, but I didn't receive a proper response. Let me try again."
                    message = AIMessage(content=content)
                
                generation = ChatGeneration(message=message)
                return ChatResult(generations=[generation])
            else:
                raise ValueError(f"Unexpected response format: {result}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to Pollinations API failed: {e}")
            # Try fallback with simple GET endpoint
            if "502" in str(e) or "503" in str(e):
                return self._fallback_generate(messages, **kwargs)
            raise ValueError(f"Pollinations API request failed: {e}")
        except Exception as e:
            logger.error(f"Error processing Pollinations response: {e}")
            raise ValueError(f"Error processing Pollinations response: {e}")
    
    def _fallback_generate(self, messages: List[BaseMessage], **kwargs) -> ChatResult:
        """Fallback generation using simple GET endpoint when OpenAI endpoint fails"""
        try:
            # Extract the last user message for simple generation
            user_messages = [msg for msg in messages if isinstance(msg, HumanMessage)]
            if not user_messages:
                raise ValueError("No user message found for fallback generation")
            
            last_message = user_messages[-1].content
            
            # Use simple GET endpoint as fallback
            fallback_url = f"https://text.pollinations.ai/{last_message}"
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.get(fallback_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            content = response.text.strip()
            if not content:
                content = "I apologize, but I'm having trouble generating a response right now."
            
            message = AIMessage(content=content)
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])
            
        except Exception as e:
            logger.error(f"Fallback generation also failed: {e}")
            # Last resort - return a helpful error message
            message = AIMessage(content="I'm experiencing technical difficulties. Please try again in a moment.")
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])
    
    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGeneration]:
        """Stream responses from Pollinations API."""
        # For now, fall back to non-streaming
        # TODO: Implement streaming using Pollinations SSE endpoint
        result = self._generate(messages, stop, run_manager, **kwargs)
        yield result.generations[0]
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get identifying parameters."""
        return {
            "model_name": self.model_name,
            "base_url": self.base_url,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }