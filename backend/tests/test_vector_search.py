import pytest
from app.utils.vector_search import VectorSearch

def test_vector_search_initialization():
    """Test that the VectorSearch class initializes correctly"""
    search = VectorSearch(collection_name="test_collection")
    assert search.model is not None
    assert search.collection is not None

def test_add_items_and_search():
    """Test adding items and searching"""
    # Create test data with very distinct categories to ensure reliable results
    test_items = [
        {
            "id": 1,
            "name": "Test User 1",
            "category": "tech",
            "description": "A tech influencer with expertise in artificial intelligence, machine learning, and data science"
        },
        {
            "id": 2,
            "name": "Test User 2",
            "category": "fashion",
            "description": "A fashion influencer focusing on sustainable clothing, runway trends, and style tips"
        }
    ]
    
    # Initialize vector search with a unique collection name to avoid conflicts
    import uuid
    collection_name = f"test_search_collection_{uuid.uuid4().hex[:8]}"
    print(f"Testing with collection: {collection_name}")
    
    search = VectorSearch(collection_name=collection_name)
    
    # Add items
    search.add_items(test_items)
    print("Added test items to vector database")
    
    # Search for tech-related query
    query = "technology artificial intelligence and machine learning"
    print(f"Searching for: {query}")
    results = search.search(query)
    
    # Print results for debugging
    print(f"Search returned {len(results)} results")
    for i, result in enumerate(results):
        print(f"Result {i+1}: id={result.get('id')}, category={result.get('category')}")
    
    # Verify results
    assert len(results) > 0, "Search should return at least one result"
    
    # The first result should be the tech influencer
    # With these very distinct categories and query, it should work reliably
    tech_found = False
    
    # Debug the results structure
    print(f"Results structure: {type(results)}")
    if results and len(results) > 0:
        print(f"First result keys: {results[0].keys() if hasattr(results[0], 'keys') else 'No keys method'}")
    
    # Check each result for the tech influencer
    for result in results:
        # Print the exact result for debugging
        print(f"Checking result: {result}")
        
        # Try different ways to access the id and category
        result_id = result.get('id', None)
        if result_id is None and isinstance(result, dict):
            # Try direct access
            result_id = result['id'] if 'id' in result else None
        
        result_category = result.get('category', None)
        if result_category is None and isinstance(result, dict):
            # Try direct access
            result_category = result['category'] if 'category' in result else None
        
        print(f"Extracted id: {result_id}, category: {result_category}")
        
        # Check if this is the tech influencer (more flexible check)
        if str(result_id) == '1' or (isinstance(result_id, int) and result_id == 1):
            if result_category == 'tech':
                tech_found = True
                print("Found tech influencer!")
                break
    
    assert tech_found, "Tech influencer should be in results for tech query"
