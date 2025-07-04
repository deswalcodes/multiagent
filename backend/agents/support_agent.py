from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from backend.tools.mongodb_tool import MongoDBTool
from backend.tools.external_api import ExternalAPI
import os
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# set up LLM
llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY")
)

# initialize tools
mongo_tool = MongoDBTool()
external_api = ExternalAPI()

tools = [
    Tool(
        name="FindClassesThisWeek",
        func=lambda x: mongo_tool.get_classes(),
        description="Lists all classes scheduled in the coming week."
    ),
    Tool(
        name="CheckOrderPaymentStatus",
        func=lambda order_id: mongo_tool.get_order_by_id(order_id),
        description="Checks an order by its ID and returns its payment status."
    ),
    Tool(
    name="CreateNewOrder",
    func=lambda client_name: external_api.create_order(
        mongo_tool.get_client(client_name)["_id"], 
        "Yoga Beginner", 
        1500
    ),
    description="Creates a new order for a client with a Yoga Beginner class and price 1500."
)
,
    Tool(
        name="CreateClientEnquiry",
        func=lambda name: external_api.create_client_enquiry(name, "test@example.com", "1234567890"),
        description="Creates a client enquiry given a name, with test email and phone."
    ),
    Tool(
        name="CreateClientEnquiry",
        func=lambda name: external_api.create_client_enquiry(name, "test@example.com", "1234567890"),
        description="Creates a client enquiry given a name, with test email and phone."
    ),
    Tool(
    name="RecallLastUserQuery",
    func=lambda x: memory.chat_memory.messages[-1].content if memory.buffer else "No history available.",
    description="Recalls the last user question from conversation memory."
)

]

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True
)

def support_agent():
    return agent_executor
