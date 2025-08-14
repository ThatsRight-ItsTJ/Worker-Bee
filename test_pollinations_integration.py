import os
from openoperator.tools.pollinations.vision_tool import PollinationsVisionTool
from openoperator.tools.pollinations.text_tool import PollinationsTextTool

def test_vision_tool():
    """Test vision analysis on a sample screenshot"""
    vision_tool = PollinationsVisionTool()
    
    # Assuming you have a test screenshot
    test_image = "/images/screenshot.jpg"
    if os.path.exists(test_image):
        result = vision_tool._run(
            image_path=test_image,
            query="Describe what you see in this image",
            model="openai"
        )
        print("Vision Analysis Result:")
        print(result)
    else:
        print("No test image found")

def test_text_tool():
    """Test text generation"""
    text_tool = PollinationsTextTool()
    
    result = text_tool._run(
        prompt="Explain how web automation works in simple terms",
        model="openai"
    )
    print("Text Generation Result:")
    print(result)

if __name__ == "__main__":
    test_vision_tool()
    test_text_tool()