from agents import RunHooks

class CustomRunHooks(RunHooks):
    async def on_start(self, context_wrapper, agent):
        print(f"[CustomRunHooks] on_start called for agent {agent.name}")

    async def on_end(self, context_wrapper, agent, final_output):
        print(f"[CustomRunHooks] on_end called for agent {agent.name} with output: {final_output}")

    async def on_agent_start(self, agent, context_wrapper):
        print(f"[CustomRunHooks] Agent {agent.name} started.")

    async def on_agent_end(self, agent, context_wrapper, output):
        print(f"[CustomRunHooks] Agent {agent.name} ended with output: {output}")

    async def on_tool_start(self, context_wrapper, agent, tool):
        print(f"[CustomRunHooks] Tool {tool.name} started.")

    async def on_tool_end(self, context_wrapper, agent, tool, output):
        print(f"[CustomRunHooks] Tool {tool.name} ended with output: {output}")

    async def on_handoff(self, context_wrapper, agent, source):
        print(f"[CustomRunHooks] on_handoff called from {source.name} to {agent.name}")
