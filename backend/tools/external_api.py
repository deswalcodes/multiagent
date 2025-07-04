from backend.models.schemas import db
from bson import ObjectId
from datetime import datetime

class ExternalAPI:
    def create_client_enquiry(self, name: str, email: str, phone: str):
        """
        Simulate an enquiry creation by inserting a new client with status 'enquiry'
        """
        client = {
            "name": name,
            "email": email,
            "phone": phone,
            "enrolled_services": [],
            "created_at": datetime.now()
        }
        result = db.clients.insert_one(client)
        return str(result.inserted_id)
    
    def create_order(self, client_id: str, service_name: str, amount: float):
        """
        Simulate creating an order
        """
        order = {
            "client_id": ObjectId(client_id),
            "service_name": service_name,
            "amount": amount,
            "status": "pending", 
            "created_at": datetime.now()
        }
        result = db.orders.insert_one(order)
        return str(result.inserted_id)
