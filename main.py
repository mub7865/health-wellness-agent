import os
import sys
import asyncio
from dotenv import load_dotenv

from agents import (
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    ItemHelpers,
    set_default_openai_client,
    set_default_openai_api,
    set_tracing_disabled,
    RunContextWrapper,
)

from agents.run import RunConfig

from context import UserSessionContext
from guardrails import validate_goal_input, validate_output
from agent import create_health_agent

sys.path.append(os.path.dirname(__file__))
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

set_default_openai_client(client=external_client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)

config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)

async def main():
    agent = create_health_agent(model)

    # ✅ Create user context
    user_context = RunContextWrapper(UserSessionContext(
        name="User",
        uid=1,
        goal=None,
        diet_preferences=None,
        workout_plan=None,
        meal_plan=[],
        injury_notes=None,
        handoff_logs=[],
        progress_logs=[]
    ))

    print("CustomRunHooks module loaded\n")

    while True:
        user_input = input("Enter Your Question (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            break

        try:
            validate_goal_input(user_input)
        except ValueError as e:
            print(f"Input Error: {e}")
            continue

        print("\nAssistant:")

        result = Runner.run_streamed(agent, input=user_input, context=user_context)

        async for event in result.stream_events():
            if event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    print(f"[Tool Call] {getattr(event.item, 'tool', 'UnknownTool')}")
                elif event.item.type == "tool_call_output_item":
                    print(f"[Tool Output] {event.item.output}")
                elif event.item.type == "message_output_item":
                    print(ItemHelpers.text_message_output(event.item))

        try:
            validate_output(result.final_output)
        except ValueError as e:
            print(f"Output Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
