import time
from openoperator.tools.pollinations.vision_tool import PollinationsVisionTool

def safe_vision_call(image_path: str, query: str, retries: int = 3):
    """Make vision API call with retry logic"""
    for attempt in range(retries):
        try:
            tool = PollinationsVisionTool()
            return tool._run(image_path, query)
        except Exception as e:
            if attempt == retries - 1:
                return f"Vision analysis failed after {retries} attempts: {str(e)}"
            time.sleep(1)  # Brief delay before retry