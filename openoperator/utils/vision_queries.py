# Common vision analysis queries for web automation
VISION_QUERIES = {
    "navigation": "What clickable navigation elements (menus, links, buttons) are visible on this page?",
    "forms": "What input fields, forms, and submission buttons are present? List their types and labels.",
    "errors": "Are there any error messages, warnings, or loading indicators visible?",
    "completion": "Has this page finished loading completely? Are there any loading spinners or incomplete elements?",
    "data_extraction": "Extract all visible text content, especially any structured data like tables, lists, or key-value pairs.",
    "page_type": "What type of page is this? (login, search results, product page, form, etc.)",
    "interactions": "What are the most important interactive elements a user would typically click or fill out on this page?"
}

def get_vision_query(query_type: str, custom_query: str = None) -> str:
    """Get a predefined vision query or return custom query"""
    if custom_query:
        return custom_query
    return VISION_QUERIES.get(query_type, VISION_QUERIES["navigation"])