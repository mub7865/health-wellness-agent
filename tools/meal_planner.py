from agents import function_tool

@function_tool
def meal_planner(diet: str = "balanced") -> str:
    return f"🥗 A {diet} meal plan includes protein, fiber, fruits, and water."

def generate_meal_plan():
    return "Meal plan generation tool"
