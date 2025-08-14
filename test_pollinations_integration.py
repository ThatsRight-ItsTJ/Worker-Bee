import os
from openoperator.tools.pollinations.vision_tool import PollinationsVisionTool
from openoperator.tools.pollinations.text_tool import PollinationsTextTool

def test_vision_tool():
    """Test vision analysis on a sample screenshot"""
    vision_tool = PollinationsVisionTool()
    
    # Assuming you have a test screenshot
    test_images = [
        "realistic-ferret-t-shirt-design-449cf9.jpeg",
        "public/images/screenshot.jpg", 
        "public/images/image.jpg"
    ]
    
    test_image = None
    for img_path in test_images:
        if os.path.exists(img_path):
            test_image = img_path
            break
    
    if test_image:
        print(f"Testing with image: {test_image}")
        result = vision_tool._run(
            image_path=test_image,
            query="Describe what you see in this image",
            model="openai"
        )
        print("Vision Analysis Result:")
        print(result)
    else:
        print("No test image found. Available images should be:")
        for img_path in test_images:
            print(f"  - {img_path}")
        print("Creating a simple test...")
        
        # Test with a simple prompt instead
        text_tool = PollinationsTextTool()
        result = text_tool._run(
            prompt="Describe what elements you would typically find on a web page screenshot",
            model="openai"
        )
        print("Alternative test result:")
        print(result)

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