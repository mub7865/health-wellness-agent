from agents import Agent
#  ------------------------------------------------------tools--------------------------------------------------------------------------------------

from output_guardrails import health_output_guardrail
from tools.goal_analyzer import analyze_health_goal
from tools.meal_planner import plan_meals
from tools.workout_recommender import recommend_workout
from tools.scheduler import schedule_checkins
from tools.tracker import track_progress
#  ------------------------------------------------------special agents--------------------------------------------------------------------------------------
from custom_agents.nutrition_expert_agent import nutrition_expert_agent
from custom_agents.injury_support_agent import injury_support_agent
from custom_agents.escalation_agent import escalation_agent

#  ------------------------------------------------------hooks--------------------------------------------------------------------------------------
from hooks import CustomRunHooks

#  ------------------------------------------------------input guardrail--------------------------------------------------------------------------------------
from input_guardrails import health_input_guardrail

def create_health_agent(model):
    nutrition_agent = nutrition_expert_agent
    injury_agent = injury_support_agent
    escalationAgent = escalation_agent

    # Main agent
    return Agent(
        name="HealthWellnessAgent",
        instructions = """
You are a Health & Wellness Planner Assistant. Help users set fitness and dietary goals, provide plans, and track progress. Handoff to specialized agents when needed.

If the user asks for multiple tasks in one message — such as goal analysis, meal planning, workout recommendations, progress tracking, and scheduling — do not throw an error. Instead, intelligently break down the request and use the following tools in the correct order based on user input:

1. analyze_health_goal
2. plan_meals
3. recommend_workout
4. track_progress
5. schedule_checkins

Use each tool as needed and explain your responses in a friendly, helpful tone like a real health coach. Always provide value, and only ask for clarification if the input is unclear. 
"""
,
        model=model,
        tools=[
            analyze_health_goal,
            plan_meals,
            recommend_workout,
            track_progress,
            schedule_checkins,
        ],
        handoffs=[nutrition_agent, injury_agent, escalationAgent],
        hooks=CustomRunHooks(), 
        input_guardrails=[health_input_guardrail],
        output_guardrails=[health_output_guardrail]
    )