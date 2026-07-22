from langgraph.graph import StateGraph, MessagesState


def call_agent(message_state: MessagesState):
    print(message_state)
    example_message = "world"
    return {
        "messages": [example_message, example_message]
    }


graph = StateGraph(MessagesState)   # Initialize with state type

graph.add_node('agent', call_agent) # Node 'agent' runs `call_agent`

graph.add_edge('agent', '__end__')  # After 'agent', terminate

graph.set_entry_point('agent')  # Start at 'agent'

app = graph.compile()   # Finalizes the graph into an executable

updated_message = app.invoke( {"messages": "Hello"} )   # Trigger execution

print(updated_message)