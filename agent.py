from agents import Agent
from tools.goal_analyzer import goal_analyzer
from tools.meal_planner import meal_planner
from tools.workout_recommender import workout_recommender
from tools.scheduler import checkin_scheduler
from tools.tracker import progress_tracker

from custom_agents.nutrition_expert_agent import NutritionExpertAgent
from custom_agents.injury_support_agent import InjurySupportAgent
from custom_agents.escalation_agent import EscalationAgent

from hooks import CustomRunHooks

def create_health_agent(model):
    nutrition_agent = NutritionExpertAgent(model=model)
    injury_agent = InjurySupportAgent(model=model)
    escalation_agent = EscalationAgent(model=model)

    # Main agent
    return Agent(
        name="HealthWellnessAgent",
        instructions="You are a Health & Wellness Planner Assistant. Help users set fitness and dietary goals, provide plans, and track progress. Handoff to specialized agents when needed.",
        model=model,
        tools=[
            goal_analyzer,
            meal_planner,
            workout_recommender,
            progress_tracker,
            checkin_scheduler,
        ],
        handoffs=[nutrition_agent, injury_agent, escalation_agent],
        hooks=CustomRunHooks(), 
    )
