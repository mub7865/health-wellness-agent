from agents import Agent
from tools.workout_recommender import workout_recommender
from hooks import CustomRunHooks

class InjurySupportAgent(Agent):
    def __init__(self, model):
        super().__init__(
            name="InjurySupportAgent",
            instructions="You are an Injury Support Specialist. Provide safe workout plans for injured users.",
            model=model,
            tools=[workout_recommender],
            hooks=CustomRunHooks()
        )
