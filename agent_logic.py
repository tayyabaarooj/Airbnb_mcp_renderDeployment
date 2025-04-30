from praisonaiagents import MCP, Agent

from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="llama3")
 

def search_airbnb(query):
    agent =Agent(
    instructions="""You help book apartments on airbnb""",
    llm=llm,
    tools=MCP("npx @openbnb/mcp-server-airbnb --ignore-robots-txt")
    )
    result=agent.start(query)
    return f"## Airbnd search results \n\n{result}"


if __name__=="__main__":
    print(search_airbnb("2-bedroom apartment in New York for 1 may 2025"))
