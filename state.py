from typing import TypedDict, Dict, List

class State(TypedDict):
    original_body: Dict[str, str]
    user_inputs: Dict[str, str]
    generated_bodies: List[Dict]
    request_name: str
