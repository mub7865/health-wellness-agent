# D:\Agentic Ai\Health-Wellness-Planner-Agent\utils\streaming.py

def stream_response(step: dict) -> str:
    # Pretty print streamed output
    if "error" in step:
        return f"Error: {step['error']}"
    return str(step)