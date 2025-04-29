from flask import Flask, request, jsonify
from langchain.agents import initialize_agent, AgentType
from langchain_community.llms import Ollama
from langchain.tools import Tool
from praisonaiagents import MCP

# Initialize Flask app
app = Flask(__name__)

# Set up the LLM
llm = Ollama(model="llama3")

# Set up the MCP Airbnb tool
mcp_tool = MCP("npx @openbnb/mcp-server-airbnb --ignore-robots-txt")

# Wrap MCP tool in LangChain-compatible format
tools = [
    Tool(
        name="AirbnbSearchTool",
        func=mcp_tool,
        description="Use this tool to search for apartments on Airbnb"
    )
]

# Initialize LangChain Agent
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Define Flask route
@app.route("/search", methods=["POST"])
def search_airbnb():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400
    
    try:
        result = agent_executor.run(query)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
