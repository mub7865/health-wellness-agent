from agents import Agent
from tools.meal_planner import meal_planner
from hooks import CustomRunHooks

class NutritionExpertAgent(Agent):
    def __init__(self, model):
        super().__init__(
            name="NutritionExpertAgent",
            instructions="You are a Nutrition Expert. Help users with diabetes or allergies by suggesting appropriate meal plans.",
            model=model,
            tools=[meal_planner],
            hooks=CustomRunHooks()
        )
