from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
#from langgraph.checkpoint.memory import MemorySaver


class Agent:
    def __init__(self):
        pass
    def set_name_agent(self, name:str) -> None:
        self.name = name
    def set_system_prompt(self, prompt:str) -> None:
        self.system_prompt = prompt
    def set_model(self, model) -> None:
        self.model = model
    def set_tools(self, tools:list) -> None:
        self.tools = tools
    def save_agent_settings(self) -> None:
        #cria o objeto 'agent'
        #memory = MemorySaver()
        agent_settings = create_agent(
            name=self.name,
            model=self.model,
            tools=self.tools,
            #checkpointer=memory,
            system_prompt=self.system_prompt, 
            middleware=[ModelCallLimitMiddleware(run_limit=5, exit_behavior="end")] #
            
        )

        self.agent_settings = agent_settings

    def run_agent(self, user_prompt:str, session:str) -> str:

        config = {"configurable": {"thread_id":session}}
        stream = self.agent_settings.stream_events(
            {"messages":[{"role":"user", "content":user_prompt}]},
            config=config,
            version="v3"
        )
        for kind, item in stream.interleave("messages", "tool_calls"):
            if kind == "messages":
                for token in item.text:
                    print(token, end="", flush=True)
            elif kind == "tool_calls":
                print(f"\nTool call: {item.tool_name}({item.input})")
                for delta in item.output_deltas:
                    print(delta, end="", flush=True)
                print(f"\nTool result: {item.output}")

        return stream.output




