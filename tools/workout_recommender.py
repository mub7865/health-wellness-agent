from pydantic import BaseModel
from typing import List
from agents import function_tool, RunContextWrapper
from context import UserSessionContext

class WorkoutPlanOutput(BaseModel):
    plan: List[str]

@function_tool
async def recommend_workout(ctx: RunContextWrapper[UserSessionContext]) -> WorkoutPlanOutput:
    goal = ctx.context.goal or {}
    experience = goal.get("experience_level", "beginner")
    injury = goal.get("injury", "").lower()  

    # Injury-Specific Workouts
    if injury == "knee":
        workouts = [
            "Day 1: Upper body stretching & resistance band arms",
            "Day 2: Seated dumbbell press + chest stretches",
            "Day 3: Light yoga (no lower body postures)",
            "Day 4: Rest day",
            "Day 5: Core workout (avoid leg raises)",
            "Day 6: Arm-focused resistance training (bands or light weights)",
            "Day 7: Rest day"
        ]
    elif injury == "back":
        workouts = [
            "Day 1: Gentle stretching (cat-cow, child's pose)",
            "Day 2: Core strengthening (bird-dog, dead bug)",
            "Day 3: Rest day",
            "Day 4: Low-impact walking (15 mins flat surface)",
            "Day 5: Light yoga (no forward bending)",
            "Day 6: Resistance bands upper body",
            "Day 7: Rest day"
        ]
    elif injury == "shoulder":
        workouts = [
            "Day 1: Lower body strength (bodyweight squats, lunges)",
            "Day 2: Walking (30 mins)",
            "Day 3: Gentle yoga (avoid overhead arm movements)",
            "Day 4: Rest day",
            "Day 5: Core and legs",
            "Day 6: Seated leg press + stationary bike (if available)",
            "Day 7: Rest day"
        ]
    else:
        # Regular Plans
        if experience == "beginner":
            workouts = [
                "Day 1: Full body stretching",
                "Day 2: Light cardio (15 mins)",
                "Day 3: Bodyweight strength (squats, pushups)",
                "Day 4: Rest day",
                "Day 5: Light yoga",
                "Day 6: Walking (30 mins)",
                "Day 7: Rest day"
            ]
        else:
            workouts = [
                "Day 1: Upper body strength",
                "Day 2: HIIT cardio",
                "Day 3: Lower body strength",
                "Day 4: Core workout",
                "Day 5: Yoga or mobility",
                "Day 6: Full body circuit",
                "Day 7: Active recovery"
            ]

    ctx.context.workout_plan = {
        "level": experience,
        "injury": injury if injury else "none",
        "schedule": workouts
    }
    return WorkoutPlanOutput(plan=workouts)
