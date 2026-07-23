from dotenv import load_dotenv
from langgraph.graph import StateGraph, MessagesState
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from tools import query_knowledge_base, search_for_product_recommendations


load_dotenv()


SYSTEM_PROMPT = """
# Purpose 
You are a customer service chatbot for a flower shop company. You can help the customer achieve the goals listed below.

# Goals
1. Answer questions the user might have relating to serivces offered
2. Recommend products to the user based on their preferences

# Tone
Helpful and friendly. Use cute flower related emojis to keep things lighthearted.
"""


chat_template = ChatPromptTemplate.from_messages(
    [
        ('system', SYSTEM_PROMPT),
        ('placeholder', "{messages}")
    ]
)


# llm = ChatOpenAI(model="gpt-4o")
llm = ChatOpenAI(
    model="mistral-medium-latest",
    base_url="https://api.mistral.ai/v1",
    # api_key="lm-studio" // API key is added in .env file
)

tools = [query_knowledge_base, search_for_product_recommendations]
llm_with_prompt = chat_template | llm.bind_tools(tools)

def call_agent(message_state: MessagesState):
    """
    Calls the agent with the current message state and returns the response."""
    response = llm_with_prompt.invoke(message_state)
    return {
        "messages": [response]
    }

def is_there_tool_calls(state: MessagesState):
    """
    Checks if the last message in the state contains a tool call.
    """
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return 'tool_node'
    else:
        return '__end__'



graph = StateGraph(MessagesState)   # Initialize with state type

graph.add_node('agent', call_agent) # Node 'agent' runs `call_agent`

tool_node = ToolNode(tools)
graph.add_node('tool_node', tool_node)  # Node 'tool_node' runs the tools

graph.add_conditional_edges(
    "agent",
    is_there_tool_calls
)
graph.add_edge('tool_node', 'agent')    # After tool calls, go back to agent for further processing

graph.set_entry_point('agent') 

app = graph.compile()   # Finalizes the graph into an executable
