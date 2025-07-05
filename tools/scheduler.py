from agents import function_tool

@function_tool
def checkin_scheduler(day: str = "Sunday") -> str:
    return f"📅 Health check-in set for {day} at 10 AM."

def schedule_checkins():
    return "Check-in scheduling tool"
