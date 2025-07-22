# D:\Agentic Ai\health_wellness_agent\tools\goal_analyzer.py
from pydantic import BaseModel
from typing import Optional
from agents import function_tool, RunContextWrapper
from context import UserSessionContext
import re


class GoalOutput(BaseModel):
    quantity: float
    metric: str
    duration: str
    description: Optional[str] = None


@function_tool
async def analyze_health_goal(
    wrapper: RunContextWrapper[UserSessionContext],
    goal_description: str
) -> GoalOutput:
    text = goal_description.lower()

    weight_loss_keywords = ['lose weight', 'lose', 'slim', 'fat loss', 'reduce', 'weight loss']
    weight_gain_keywords = ['gain weight', 'gain', 'weight gain', 'increase weight', 'put on weight']
    muscle_gain_keywords = ['gain muscle', 'build muscle', 'bulk', 'muscle building', 'get stronger']
    fitness_keywords = ['fit', 'exercise', 'cardio', 'run', 'endurance', 'stamina']
    general_keywords = ['health', 'wellness', 'healthy', 'lifestyle']

    if any(kw in text for kw in weight_loss_keywords):
        goal_type = "Weight-loss goal"
    elif any(kw in text for kw in weight_gain_keywords):
        goal_type = "Weight-gain goal"
    elif any(kw in text for kw in muscle_gain_keywords):
        goal_type = "Muscle-gain goal"
    elif any(kw in text for kw in fitness_keywords):
        goal_type = "Fitness goal"
    elif any(kw in text for kw in general_keywords):
        goal_type = "General health goal"
    else:
        goal_type = "Unspecified goal"

    # Extract quantity and metric
    match_amount_unit = re.search(r'(\d+\.?\d*)\s*(kg|kilograms|lbs|pounds)?', text)
    quantity = float(match_amount_unit.group(1)) if match_amount_unit else 0.0
    metric = match_amount_unit.group(2) if match_amount_unit and match_amount_unit.group(2) else ""

    # Extract duration
    match_timeframe = re.search(r'(\d+)\s*(day|week|month|year)s?', text)
    if match_timeframe:
        duration = f"{match_timeframe.group(1)} {match_timeframe.group(2)}{'s' if int(match_timeframe.group(1)) > 1 else ''}"
    else:
        duration = ""

    # Save to user context
    wrapper.context.goal = {
        "goal_type": goal_type,
        "quantity": quantity,
        "metric": metric,
        "duration": duration,
        "description": goal_description.strip()
    }

    # Return pydantic object
    return GoalOutput(
        quantity=quantity,
        metric=metric,
        duration=duration,
        description=goal_type
    )
