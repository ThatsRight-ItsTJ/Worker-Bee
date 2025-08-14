import requests
import os
from typing import Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class PollinationsTextInput(BaseModel):
    prompt: str = Field(description="Text prompt for AI generation")
    model: str = Field(default="openai", description="Text model to use")
    system_prompt: str = Field(default="You are a helpful assistant.", description="System prompt")

class PollinationsTextTool(BaseTool):
    name: str = "pollinations_text"
    description: str = """
    Generate text responses using Pollinations AI models. Can be used for 
    reasoning, planning, or generating responses when primary LLM is unavailable.
    """
    args_schema: Type[BaseModel] = PollinationsTextInput
    
    def _run(self, prompt: str, model: str = "openai", system_prompt: str = "You are a helpful assistant.") -> str:
        """Execute text generation using Pollinations API"""
        try:
            # Get authentication from environment
            api_key = os.getenv('POLLINATIONS_API_KEY')
            referrer = os.getenv('POLLINATIONS_REFERRER')
            
            # OpenAI-compatible format
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000
            }
            
            # Add authentication if available
            if referrer:
                payload["referrer"] = referrer
            
            headers = {"Content-Type": "application/json"}
            
            # Add API key authentication if available
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            response = requests.post(
                "https://text.pollinations.ai/openai",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            return f"Text generation failed: {str(e)}"

    async def _arun(self, prompt: str, model: str = "openai", system_prompt: str = "You are a helpful assistant.") -> str:
        return self._run(prompt, model, system_prompt)