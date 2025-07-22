from fpdf import FPDF
from datetime import datetime
import os
from typing import Dict, Any, List
from textwrap import fill
import re

class PDFReportGenerator:
    def __init__(self, context_dict: Dict[str, Any]):
        self.context = context_dict

    def generate_report(self, output_path: str = "wellness_report.pdf"):
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

        def break_long_words(text, max_word_length=40):
            # Insert spaces into long words to allow wrapping
            def breaker(match):
                word = match.group(0)
                return ' '.join([word[i:i+max_word_length] for i in range(0, len(word), max_word_length)])
            return re.sub(r'\S{' + str(max_word_length+1) + r',}', breaker, text)

        def safe_multicell(text, width=90):
            try:
                s = str(text)
                s = break_long_words(s)
                wrapped = fill(s, width=width)
                pdf.multi_cell(0, 10, txt=wrapped)
            except Exception:
                pass  # Skip this line if it still fails

        def safe_line(text, ln=True):
            try:
                s = str(text)
                s = break_long_words(s)
                pdf.cell(200, 10, txt=fill(s, width=120), ln=ln)
            except Exception:
                pass

        sections = [
            ("Goal", self.context.get("goal")),
            ("Diet Preferences", self.context.get("diet_preferences")),
            ("Meal Plan", self.context.get("meal_plan")),
            ("Workout Plan", self.context.get("workout_plan")),
            ("Injury Notes", self.context.get("injury_notes")),
            ("Handoff Logs", self.context.get("handoff_logs")),
            ("Progress Logs", self.context.get("progress_logs")),
            ("Conversation Summary", self.context.get("messages")),
        ]

        for title, data in sections:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, txt=title, ln=True)
            pdf.set_font("Arial", size=12)

            if not data:
                pdf.cell(200, 10, txt=f"No {title.lower()} available.", ln=True)
                continue

            if title == "Meal Plan" and isinstance(data, list):
                for i, meal in enumerate(data, 1):
                    safe_line(f"Day {i}: {meal}")
            elif title == "Workout Plan":
                if isinstance(data, dict) and "schedule" in data:
                    for i, item in enumerate(data["schedule"], 1):
                        safe_line(f"Day {i}: {item}")
                else:
                    safe_multicell(data)
            elif title == "Progress Logs":
                for log in data:
                    if isinstance(log, dict):
                        log_text = ", ".join(f"{k}: {v}" for k, v in log.items())
                    else:
                        log_text = str(log)
                    safe_multicell(f"- {log_text}")
            elif title == "Conversation Summary":
                for msg in data:
                    if isinstance(msg, dict):
                        role = msg.get("role", "user")
                        content = msg.get("content", "")
                        safe_multicell(f"{role.title()}: {content}")
                    else:
                        safe_multicell(str(msg))
            elif isinstance(data, list):
                for item in data:
                    safe_multicell(f"- {item}")
            elif isinstance(data, dict):
                for k, v in data.items():
                    safe_multicell(f"{k}: {v}")
            else:
                safe_multicell(data)

        try:
            pdf.output(output_path)
            print(f"📄 Report saved to {output_path}")
        except PermissionError:
            print("❌ Error: Could not write PDF. Close any open 'wellness_report.pdf' file and try again.")
        except Exception as e:
            print(f"❌ Error: Could not write PDF. {e}")
