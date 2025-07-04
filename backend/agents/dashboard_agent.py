from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from backend.tools.mongodb_tool import MongoDBTool
import os
from langchain.memory import ConversationBufferMemory

from dotenv import load_dotenv

load_dotenv()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY")
)

mongo_tool = MongoDBTool()

tools = [
    Tool(
        name="TotalRevenue",
        func=lambda x: sum(p["amount"] for p in mongo_tool.get_payments()),
        description="Returns total revenue from all payments."
    ),
    Tool(
        name="OutstandingPayments",
        func=lambda x: mongo_tool.calculate_pending_dues(client_id=None),
        description="Lists outstanding payments for all clients."
    ),
    Tool(
        name="ActiveInactiveClients",
        func=lambda x: {
            "active": mongo_tool.db.clients.count_documents({"enrolled_services.status": "active"}),
            "inactive": mongo_tool.db.clients.count_documents({"enrolled_services.status": {"$ne": "active"}})
        },
        description="Counts active vs inactive clients."
    ),
    Tool(
        name="TopCourses",
        func=lambda x: [
            {"course_id": s["course_id"], "count": s["count"]}
            for s in mongo_tool.db.clients.aggregate([
                {"$unwind": "$enrolled_services"},
                {"$group": {"_id": "$enrolled_services.course_id", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 3}
            ])
        ],
        description="Lists the top 3 most enrolled courses."
    ),
    Tool(
    name="AttendancePercentageByClass",
    func=lambda class_id: mongo_tool.get_attendance_percentage_by_class(class_id),
    description="Calculates the attendance percentage for a given class ID."
)

]

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    memory = memory,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

def dashboard_agent():
    return agent_executor
