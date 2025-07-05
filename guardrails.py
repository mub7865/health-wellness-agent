import re
from typing import Any

def validate_goal_input(user_input: str) -> bool:
    # Example: "lose 5kg in 2 months" or "gain muscle"
    pattern = r"^(lose|gain)\s+\d+\w*\s*(in\s*\d+\s*(month|week)s?)?.*$"
    return bool(re.match(pattern, user_input.lower())) or "muscle" in user_input.lower()

def validate_output(output: Any) -> Any:
    # Ensure output is structured (e.g., JSON or Pydantic model)
    if isinstance(output, dict) or hasattr(output, 'dict'):
        return output
    return {"error": "Invalid output format"}