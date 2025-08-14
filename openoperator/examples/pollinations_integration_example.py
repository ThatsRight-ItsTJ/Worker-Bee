"""
Example of how to integrate Pollinations vision capabilities into LangGraph workflow
"""

from langgraph import StateGraph
from openoperator.tools.pollinations.vision_tool import PollinationsVisionTool
from openoperator.utils.vision_queries import get_vision_query

def analyze_page_node(state):
    """Node that analyzes current page using vision"""
    vision_tool = PollinationsVisionTool()
    
    # Get current screenshot path from state
    screenshot_path = state.get("current_screenshot")
    
    if screenshot_path:
        # Analyze page content
        analysis = vision_tool._run(
            image_path=screenshot_path,
            query="Describe all interactive elements on this page including buttons, links, forms, and their locations. Also identify any error messages or loading states."
        )
        
        # Update state with analysis
        state["page_analysis"] = analysis
        
    return state

def enhanced_page_analysis_node(state):
    """Enhanced node that uses predefined vision queries"""
    vision_tool = PollinationsVisionTool()
    screenshot_path = state.get("current_screenshot")
    
    if screenshot_path:
        # Use different types of analysis
        analyses = {}
        
        # Check for navigation elements
        analyses["navigation"] = vision_tool._run(
            image_path=screenshot_path,
            query=get_vision_query("navigation")
        )
        
        # Check for forms
        analyses["forms"] = vision_tool._run(
            image_path=screenshot_path,
            query=get_vision_query("forms")
        )
        
        # Check for errors or loading states
        analyses["status"] = vision_tool._run(
            image_path=screenshot_path,
            query=get_vision_query("errors")
        )
        
        state["detailed_analysis"] = analyses
    
    return state

def create_enhanced_agent_workflow():
    """Example of creating a workflow with vision analysis"""
    workflow = StateGraph()
    
    # Add the new analysis nodes
    workflow.add_node("analyze_page", analyze_page_node)
    workflow.add_node("enhanced_analysis", enhanced_page_analysis_node)
    
    # Connect to existing nodes (example)
    workflow.add_edge("take_screenshot", "analyze_page")
    workflow.add_edge("analyze_page", "enhanced_analysis")  
    workflow.add_edge("enhanced_analysis", "plan_action")
    
    return workflow

# Example of replacing expensive OpenAI vision calls
def replace_openai_vision_example():
    """Example showing how to replace OpenAI Vision API calls"""
    
    # BEFORE (expensive OpenAI calls)
    # openai_response = openai.chat.completions.create(
    #     model="gpt-4-vision-preview",
    #     messages=[...],
    #     max_tokens=300
    # )
    
    # AFTER (free Pollinations calls)
    vision_tool = PollinationsVisionTool()
    response = vision_tool._run(
        image_path="screenshot.png",
        query="What elements can I interact with on this page?",
        model="openai"  # or "sur", "gemini"
    )
    
    return response