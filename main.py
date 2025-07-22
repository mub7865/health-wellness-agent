from agent import create_health_agent 
from context import UserSessionContext
from agents import Runner,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled
from dotenv import load_dotenv
from agents.run import RunConfig
import asyncio, os
from utils.streaming import stream_response

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = ("AIzaSyD5cwOmgg1_S7fOSjfI13SUJ3Di5e67i4Y")

if not API_KEY:
    raise ValueError("Error: GEMINI_API_KEY not found in .env file. Add your Gemini API key to proceed.")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client
)


print("*" * 5 ,"Health and Wellness AI Agent", "*" * 5,"\n")
print("Type 'exit' or 'quit' to Finish.\n")

History_save = []

async def main():
    user_context = UserSessionContext(name="khaid", uid=1001)
    while True:
        prompt = input("🧑 You : ")
        if prompt.lower() in ['exit', 'quit']:
            print("👋 Goodbye!")
            break

        user_context.messages.append({"role": "user", "content": prompt})
        health_agent = create_health_agent(model)

        try:
            result = Runner.run_streamed(
                health_agent,
                prompt,
                context=user_context,
                run_config=config
            )
            await stream_response(result, user_context)
            user_context.messages.append({"role": "assistant", "content": result.final_output})

        except Exception as e:
            if "InputGuardrailTripwireTriggered" in str(e):
                print("🛑 [Guardrail] Input not allowed (off-topic or unsafe).")

                # 🎯 Assistant explains what kind of input is expected
                fallback_response = (
                    "⚠️ Your input does not seem related to health, wellness, fitness, or nutrition. "
                    "I can only assist with those topics.\n"
                    "Please try again with a relevant question (e.g. 'I want to lose 5kg in 2 months')."
                )

                await stream_response(fallback_response, user_context)

            else:
                print(f"❌ [Unhandled Error] {e}")
                await stream_response("⚠️ Sorry, an unexpected error occurred.", user_context)

if __name__ == "__main__":
    asyncio.run(main())