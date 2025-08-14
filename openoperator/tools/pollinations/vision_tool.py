import requests
import base64
import json
import time
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
        # Try multiple endpoints and approaches
        endpoints = [
            "https://text.pollinations.ai/openai",
            "https://text.pollinations.ai/",
            "https://image.pollinations.ai/prompt/"
        ]
        
        try:
            # Encode image to base64
            with open(image_path, "rb") as image_file:
                image_b64 = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Try different API approaches
            for i, endpoint in enumerate(endpoints):
                try:
                    if i == 0:  # OpenAI format
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
                        headers = {"Content-Type": "application/json"}
                    
                    elif i == 1:  # Alternative format
                        payload = {
                            "prompt": f"{query}\n\nImage: data:image/jpeg;base64,{image_b64}",
                            "model": model
                        }
                        headers = {"Content-Type": "application/json"}
                    
                    else:  # Simple GET request format
                        # For this endpoint, we'll just return a descriptive message
                        return f"Image analysis for query: '{query}' - API endpoint testing in progress"
                    
                    print(f"Trying endpoint {i+1}/{len(endpoints)}: {endpoint}")
                    
                    response = requests.post(
                        endpoint,
                        headers=headers,
                        json=payload,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if "choices" in result:
                            return result["choices"][0]["message"]["content"]
                        elif "response" in result:
                            return result["response"]
                        elif "text" in result:
                            return result["text"]
                        else:
                            return str(result)
                    else:
                        print(f"Endpoint {endpoint} returned status {response.status_code}: {response.text}")
                        
                except requests.exceptions.RequestException as e:
                    print(f"Request failed for endpoint {endpoint}: {str(e)}")
                    if i < len(endpoints) - 1:
                        time.sleep(1)  # Brief delay before trying next endpoint
                        continue
                    else:
                        raise e
            
            return "All API endpoints failed to respond properly"
            
        except FileNotFoundError:
            return f"Image file not found: {image_path}"
        except Exception as e:
            return f"Vision analysis failed: {str(e)}"
            
    def _run_fallback_analysis(self, image_path: str, query: str) -> str:
        """Fallback analysis when API is unavailable"""
        try:
            from PIL import Image
            img = Image.open(image_path)
            width, height = img.size
            mode = img.mode
            
            return f"""
            Image Analysis (Fallback Mode):
            - Image dimensions: {width}x{height}
            - Color mode: {mode}
            - File: {image_path}
            - Query: {query}
            
            Note: Full AI vision analysis is currently unavailable due to API issues.
            This is a basic technical analysis of the image file.
            """
        except Exception as e:
            return f"Even fallback analysis failed: {str(e)}"

    async def _arun(self, image_path: str, query: str, model: str = "openai") -> str:
        """Async version - implement if needed"""
        return self._run(image_path, query, model)