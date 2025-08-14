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
            
            # Determine image format from file extension
            image_format = image_path.split('.')[-1].lower()
            if image_format == 'jpg':
                image_format = 'jpeg'
            
            # Use the correct OpenAI-compatible POST endpoint format
            payload = {
                "model": model,  # openai, openai-large, or claude-hybridspace for vision
                "messages": [
                    {
                        "role": "user", 
                        "content": [
                            {"type": "text", "text": query},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/{image_format};base64,{image_b64}"}
                            }
                        ]
                    }
                ],
                "max_tokens": 500
            }
            
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(
                "https://text.pollinations.ai/openai",
                headers=headers,
                json=payload,
                timeout=60  # Increased timeout for vision processing
            )
            
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return f"Unexpected response format: {result}"
            
        except FileNotFoundError:
            return f"Image file not found: {image_path}"
        except requests.exceptions.RequestException as e:
            return f"API request failed: {str(e)}"
        except Exception as e:
            return f"Vision analysis failed: {str(e)}"

    async def _arun(self, image_path: str, query: str, model: str = "openai") -> str:
        """Async version - implement if needed"""
        return self._run(image_path, query, model)