from fpdf import FPDF
from datetime import datetime
import os

class PDFReportGenerator:
    def __init__(self, context_dict: dict):
        self.context = context_dict

    def generate_report(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="Health & Wellness Report", ln=True, align="C")
        pdf.set_font("Arial", size=12)

        # User Info
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Name: {self.context.get('name', 'N/A')}", ln=True)
        pdf.cell(200, 10, txt=f"User ID: {self.context.get('uid', 'N/A')}", ln=True)
        pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

        pdf.ln(5)

        # Goal
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, txt="🎯 Goal", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=str(self.context.get("goal", "N/A")))

        # Meal Plan
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, txt="🥗 Meal Plan", ln=True)
        pdf.set_font("Arial", size=12)
        meal_plan = self.context.get("meal_plan", [])
        if meal_plan and isinstance(meal_plan, list):
            for day, meal in enumerate(meal_plan, start=1):
                pdf.cell(200, 10, txt=f"Day {day}: {meal}", ln=True)
        else:
            pdf.cell(200, 10, txt="No meal plan available.", ln=True)

        # Workout Plan
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, txt="💪 Workout Plan", ln=True)
        pdf.set_font("Arial", size=12)
        workout = self.context.get("workout_plan", {})
        if workout:
            pdf.multi_cell(0, 10, txt=str(workout))
        else:
            pdf.cell(200, 10, txt="No workout plan available.", ln=True)

        # Save file
        output_path = "wellness_report.pdf"
        try:
            pdf.output(output_path)
            print(f"📄 Report saved to {output_path}")
        except PermissionError:
            print("❌ Error: Could not write PDF. Close any open 'wellness_report.pdf' file and try again.")
