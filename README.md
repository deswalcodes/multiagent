# 🧠 Multi-Agent AI System – Support & Analytics Agents

This project implements a **multi-agent system** using [LangChain](https://www.langchain.com/) , where two agents serve distinct but complementary business roles:

- 🎧 **Support Agent**: Handles client support, course/class info, and order/payment queries.
- 📊 **Dashboard Agent**: Provides analytics and insights for business decision-making.

Backend is powered by **Flask**, **MongoDB**, and **LangChain**; while the frontend is hosted via **Streamlit**.

### 🌐 Hosted Frontend

👉 [Live Demo on Streamlit](https://lcpftnbpmstbnvxreygrsl.streamlit.app/)

---

## 🔧 Features

### 👩‍💼 Support Agent
- Get course/class info (by instructor, status, date)
- Order/payment status by ID or client
- Client info by name/email/phone
- Create new client enquiries and orders
- Multilingual query support (e.g. Hindi)

### 📈 Dashboard Agent
- Revenue & outstanding dues
- Top courses by enrollment
- Attendance %, drop-off rates
- Active vs inactive clients

### 🧠 Memory & Multilingual Support
- Retains conversation history for follow-up queries
- Translates non-English input (e.g., Hindi → English) before execution

---
## 📁 Folder Structure

MULTIAGENT-ASSIGNMENT/
├── backend
│ ├── agents/
│ │ ├── dashboard_agent.py # Analytics Agent
│ │ └── support_agent.py # Support & Service Agent
│ ├── models/
│ │ ├── schemas.py # MongoDB Schemas & Connection
│ │ └── seed_data.py # Initial data for testing
│ ├── tools/
│ │ ├── external_api.py # Simulated client/order creation API
│ │ └── mongodb_tool.py # CRUD & Aggregation Helpers
│ ├── app.py # Main Flask app with API routes
├── frontend.py # Optional Streamlit interface (hosted)
├── requirements.txt # Python dependencies
├── .env # Environment variables (Mongo URI, API keys)
├── screenshots/
│ ├── 1.png, 1.1.png # Example 1: Query + Logs
│ ├── 2.png, 2.2.png # Example 2: Query + Logs
│ ├── 3.png, 3.3.png # Example 3: Query + Logs
│ ├── 4.png, 4.4.png # Example 4: Multilingual + Memory
---



