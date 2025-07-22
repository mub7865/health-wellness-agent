from agents import RunHooks

class CustomRunHooks(RunHooks):

    async def on_start(self, context_wrapper, agent):
        try:
            print(f"[CustomRunHooks] on_start called for agent {agent.name}")
        except Exception as e:
            print(f"[CustomRunHooks] on_start error: {e}")

    async def on_end(self, context_wrapper, agent, final_output):
        try:
            print(f"[CustomRunHooks] on_end called for agent {agent.name} with output: {final_output}")
        except Exception as e:
            print(f"[CustomRunHooks] on_end error: {e}")

    async def on_agent_start(self, agent, context_wrapper):
        try:
            print(f"[CustomRunHooks] Agent {agent.name} started.")
        except Exception as e:
            print(f"[CustomRunHooks] on_agent_start error: {e}")

    async def on_agent_end(self, agent, context_wrapper, output):
        try:
            print(f"[CustomRunHooks] Agent {agent.name} ended with output: {output}")
        except Exception as e:
            print(f"[CustomRunHooks] on_agent_end error: {e}")

    async def on_tool_start(self, context_wrapper, agent, tool):
        try:
            print(f"[CustomRunHooks] Tool {tool.name} started.")
        except Exception as e:
            print(f"[CustomRunHooks] on_tool_start error: {e}")

    async def on_tool_end(self, context_wrapper, agent, tool, output):
        try:
            print(f"[CustomRunHooks] Tool {tool.name} ended with output: {output}")
        except Exception as e:
            print(f"[CustomRunHooks] on_tool_end error: {e}")

    async def on_handoff(self, context_wrapper, agent, source):
        try:
            print(f"[CustomRunHooks] on_handoff called from {source.name} to {agent.name}")
        except Exception as e:
            print(f"[CustomRunHooks] on_handoff error: {e}")
