from typing import List, Dict, Any
## need to change 
def get_requests_from_api() -> List[Dict[str, Any]]:
    # Simulate fetching data
    return [
        {
            "name": "Sample Request 1",
            "method": "GET",
            "url": "https://api.example.com/resource1",
            "headers": {"Authorization": "Bearer token"},
            "body": {"key1": "value1"}
        },
        {
            "name": "Sample Request 2",
            "method": "POST",
            "url": "https://api.example.com/resource2",
            "headers": {"Authorization": "Bearer token"},
            "body": {"key2": "value2"}
        },
    ]
