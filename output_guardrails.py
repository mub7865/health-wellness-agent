from agents.guardrail import  GuardrailFunctionOutput,output_guardrail
from agents.run import Runner
from agents import RunContextWrapper, Agent
from pydantic import BaseModel
from agents import TResponseInputItem
from config import config,model


class HealthOutputValidation(BaseModel):
    is_safe: bool
    original_output: str
    feedback: str

# Output checking agent
output_checker_agent = Agent(
    name="Health Output Guardrail Agent",
    instructions="You are reviewing the assistant's response to ensure it is safe, relevant, and helpful. "
        "The response should be related to health, fitness, nutrition, wellness, workout planning, goal analysis, "
        "tracking progress, injury support, escalation handling, scheduling, or meal planning. "
        "Polite and friendly responses to greetings (like 'Hi! How can I help you today?') are also acceptable. "
        "Ensure the assistant avoids giving unrelated, offensive, or harmful advice. "
        "If the response is off-topic or unsafe, flag it as not acceptable. Otherwise, mark it as valid output.",
    output_type=HealthOutputValidation,
    model=model
)

@output_guardrail
async def health_output_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: str
) -> GuardrailFunctionOutput:
    try:
        result = await Runner.run(output_checker_agent, output, context=ctx.context, run_config=config)
        return GuardrailFunctionOutput(
            output_info=result.final_output,
            tripwire_triggered=not result.final_output.is_safe
        )
    except Exception as e:
        print(f"[Guardrail Error] Output validation failed: {e}")
        return GuardrailFunctionOutput(
            output_info=None,
            tripwire_triggered=True
        )