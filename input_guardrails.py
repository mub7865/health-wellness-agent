from agents.guardrail import input_guardrail, GuardrailFunctionOutput
from agents.run import Runner
from agents import RunContextWrapper, Agent
from pydantic import BaseModel
from agents import TResponseInputItem
from config import config,model

# Define output type
class HealthInputOutput(BaseModel):
    is_health_related_question: bool
    input: str
    reasoning: str
    answer: str

# Define agent used for input validation
health_guardrail_agent = Agent(
    name="Health Input Guardrail Agent",
    instructions="You are a friendly and helpful Health & Wellness assistant. "
        "Determine whether the user's message is related to health, wellness, or any supported topic. "
        "Supported topics include: health, fitness, diet, workout, exercise, progress tracking, check-in schedules, "
        "goal setting and analysis, meal planning, nutrition, injuries, escalation needs, and overall wellness. "
        "You should also accept polite greetings like 'hi', 'hello', or 'hey' as valid health-related input. "
        "If the input is clearly unrelated to these areas (e.g., about politics or math), mark it as not health-related.",
    output_type=HealthInputOutput,
    model=model
)

# actual guardrail function
@input_guardrail
async def health_input_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input:str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    try:
        result = await Runner.run(health_guardrail_agent, input, context=ctx.context, run_config=config)
        return GuardrailFunctionOutput(
            output_info=result.final_output,
            tripwire_triggered=not result.final_output.is_health_related_question
        )
    except Exception as e:
        print(f"[Guardrail Error] Input validation failed: {e}")
        return GuardrailFunctionOutput(
            output_info=None,
            tripwire_triggered=True
        )



