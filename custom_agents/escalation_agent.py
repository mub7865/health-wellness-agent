from agents import Agent
from hooks import CustomRunHooks

class EscalationAgent(Agent):
    def __init__(self, model):
        super().__init__(
            name="EscalationAgent",
            instructions="You help users escalate to human coaches when requested.",
            model=model,
            tools=[],
            hooks=CustomRunHooks()
        )
