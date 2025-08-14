import requests
import base64
import json
from typing import Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class PollinationsVisionInput(BaseModel):
    image_path: str = Field(description="Path to the screenshot or image file")
    query: str = Field(description="Question about the image content")
    model: str = Field(default="openai", description="Vision model to use (openai, sur, gemini)")

class PollinationsVisionTool(BaseTool):
    name: str = "pollinations_vision"
    description: str = """
    Analyze screenshots and images to understand web page content, UI elements, 
    forms, buttons, text, and layout. Perfect for web automation tasks.
    """
    args_schema: Type[BaseModel] = PollinationsVisionInput
    
    def _run(self, image_path: str, query: str, model: str = "openai") -> str:
        """Execute vision analysis using Pollinations API"""
        try:
            # Encode image to base64
            with open(image_path, "rb") as image_file:
                image_b64 = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Prepare payload in OpenAI format
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user", 
                        "content": [
                            {"type": "text", "text": query},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
                            }
                        ]
                    }
                ],
                "max_tokens": 500
            }
            
            # Make API call
            response = requests.post(
                "https://text.pollinations.ai/openai",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            return f"Vision analysis failed: {str(e)}"

    async def _arun(self, image_path: str, query: str, model: str = "openai") -> str:
        """Async version - implement if needed"""
        return self._run(image_path, query, model)