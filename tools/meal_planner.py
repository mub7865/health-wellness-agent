# D:\Agentic Ai\health_wellness_agent\tools\meal_planner.py

from pydantic import BaseModel
from typing import List
from agents import function_tool, RunContextWrapper
from context import UserSessionContext

class MealPlanOutput(BaseModel):
    days: List[str]

@function_tool
async def plan_meals(ctx: RunContextWrapper[UserSessionContext]) -> MealPlanOutput:
    preference = (ctx.context.diet_preferences or "balanced").lower()
    goal_type = (ctx.context.goal.get("goal_type") if ctx.context.goal else "").lower()

    # Helper: prefix for calorie adjustments
    def adjust_prefix(base):
        if goal_type == "weight_gain":
            return f"🍽️ Higher-calorie: {base}"
        elif goal_type == "weight_loss":
            return f"🥗 Lower-calorie: {base}"
        else:
            return base

    if "vegetarian" in preference:
        plan = [
            adjust_prefix("Day 1: Veggie stir-fry with tofu"),
            adjust_prefix("Day 2: Lentil soup with whole grain bread"),
            adjust_prefix("Day 3: Grilled paneer with quinoa"),
            adjust_prefix("Day 4: Chickpea curry with brown rice"),
            adjust_prefix("Day 5: Stuffed bell peppers with oats"),
            adjust_prefix("Day 6: Mixed veggie pasta"),
            adjust_prefix("Day 7: Spinach and mushroom wrap")
        ]
    elif "vegan" in preference:
        plan = [
            adjust_prefix("Day 1: Quinoa salad with roasted vegetables"),
            adjust_prefix("Day 2: Vegan chili with kidney beans"),
            adjust_prefix("Day 3: Tofu scramble with avocado toast"),
            adjust_prefix("Day 4: Lentil dal with basmati rice"),
            adjust_prefix("Day 5: Stir-fried tempeh with greens"),
            adjust_prefix("Day 6: Vegan burger with grilled veggies"),
            adjust_prefix("Day 7: Hummus wrap with salad")
        ]
    elif "keto" in preference:
        plan = [
            adjust_prefix("Day 1: Grilled salmon with avocado salad"),
            adjust_prefix("Day 2: Chicken casserole with cheese"),
            adjust_prefix("Day 3: Omelette with mushrooms and spinach"),
            adjust_prefix("Day 4: Zucchini noodles with pesto"),
            adjust_prefix("Day 5: Beef steak with asparagus"),
            adjust_prefix("Day 6: Tuna salad with olive oil dressing"),
            adjust_prefix("Day 7: Egg muffins with bacon")
        ]
    elif "high-protein" in preference:
        plan = [
            adjust_prefix("Day 1: Grilled chicken with quinoa"),
            adjust_prefix("Day 2: Beef steak with mashed sweet potatoes"),
            adjust_prefix("Day 3: Protein pancakes with almond butter"),
            adjust_prefix("Day 4: Tuna egg salad"),
            adjust_prefix("Day 5: Greek yogurt with nuts"),
            adjust_prefix("Day 6: Turkey meatballs with rice"),
            adjust_prefix("Day 7: Smoothie with whey and chia seeds")
        ]
    elif "low-carb" in preference:
        plan = [
            adjust_prefix("Day 1: Chicken and broccoli stir-fry"),
            adjust_prefix("Day 2: Cauliflower crust pizza"),
            adjust_prefix("Day 3: Turkey lettuce wraps"),
            adjust_prefix("Day 4: Grilled shrimp with steamed vegetables"),
            adjust_prefix("Day 5: Zoodles with turkey meatballs"),
            adjust_prefix("Day 6: Stuffed cabbage rolls"),
            adjust_prefix("Day 7: Spinach salad with boiled eggs")
        ]
    elif "diabetic" in preference:
        plan = [
            adjust_prefix("Day 1: Grilled chicken with steamed vegetables"),
            adjust_prefix("Day 2: Lentil soup with whole grain toast"),
            adjust_prefix("Day 3: Quinoa salad with beans and greens"),
            adjust_prefix("Day 4: Baked fish with sweet potato"),
            adjust_prefix("Day 5: Vegetable stir-fry with tofu"),
            adjust_prefix("Day 6: Turkey and veggie wrap"),
            adjust_prefix("Day 7: Low-sugar oatmeal with seeds")
        ]
    else:  # default: balanced
        plan = [
            adjust_prefix("Day 1: Grilled chicken with brown rice and vegetables"),
            adjust_prefix("Day 2: Fish curry with quinoa"),
            adjust_prefix("Day 3: Egg and veggie sandwich"),
            adjust_prefix("Day 4: Chickpea salad with whole wheat pita"),
            adjust_prefix("Day 5: Lentil curry with rice"),
            adjust_prefix("Day 6: Baked tofu with stir-fried vegetables"),
            adjust_prefix("Day 7: Pasta with tomato sauce and chicken")
        ]

    ctx.context.meal_plan = plan
    return MealPlanOutput(days=plan)
