from agents import function_tool

@function_tool
def progress_tracker(metric: str = "steps") -> str:
    return f"📊 Tracking {metric}: Keep pushing towards your daily goal!"

def track_progress():
    return "Progress tracking tool"
