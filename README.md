# Health & Wellness Planner Agent

Developed by **Muhammad Ubaid Raza**

---

## Overview

This project is an AI-powered Health & Wellness Planner Assistant built using the `openai-agents` SDK integrated with Google Gemini API.  
It helps users set fitness and dietary goals, provides meal plans and workout recommendations, tracks progress, and supports escalation for human assistance.  
Specialized agents handle specific queries related to nutrition, injury, and escalation.

---

## Features

- **Multi-agent Architecture:** Main agent delegates tasks to specialized agents (Nutrition, Injury Support, Escalation).  
- **Context & State Management:** Maintains user session context including goals, diet preferences, workout plans, injuries, and progress logs.  
- **Tool Integration:** Async tools for goal analysis, meal planning, workout recommendation, progress tracking, and scheduling check-ins.  
- **Guardrails:** Input and output validations ensure safe and meaningful interactions.  
- **Lifecycle Hooks:** Custom hooks implemented for detailed logging of agent lifecycle events and tool usage.  
- **Real-time Streaming:** Asynchronous streaming responses with progressive event handling for smooth UX.  
- **Multi-turn Conversations:** Supports ongoing user-agent dialogues with maintained context.

---

## Technologies Used

- Python 3.13+  
- [openai-agents SDK](https://github.com/openai/openai-agents)  
- Google Gemini API  
- AsyncIO for asynchronous programming  
- dotenv for environment variable management  

---

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone <repo-url>
   cd Health-Wellness-Planner-Agent
