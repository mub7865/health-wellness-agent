from agents import function_tool

@function_tool
def goal_analyzer(goal: str) -> str:
    return f"🎯 Your goal '{goal}' sounds achievable and inspiring!"
