from backend.models.schemas import db
from bson import ObjectId
from datetime import datetime

class MongoDBTool:
    def __init__(self):
        self.db = db

    def get_client(self, identifier: str):
        query = {
            "$or": [
                {"name": identifier},
                {"email": identifier},
                {"phone": identifier}
            ]
        }
        return self.db.clients.find_one(query)
    
    def get_orders_by_client(self, client_id: str):
        return list(self.db.orders.find({"client_id": ObjectId(client_id)}))
    
    def get_order_by_id(self, order_id: str):
        return self.db.orders.find_one({"_id": ObjectId(order_id)})

    def get_payments_by_order(self, order_id: str):
        return list(self.db.payments.find({"order_id": ObjectId(order_id)}))
    
    def get_courses(self, instructor=None, status=None):
        query = {}
        if instructor:
            query["instructor"] = instructor
        if status:
            query["status"] = status
        return list(self.db.courses.find(query))
    
    def get_classes(self, status=None, instructor=None):
        query = {}
        if status:
            query["status"] = status
        if instructor:
            query["instructor"] = instructor
        return list(self.db.classes.find(query))
    
    def get_attendance_by_class(self, class_id: str):
        return list(self.db.attendance.find({"class_id": ObjectId(class_id)}))
    
    def calculate_pending_dues(self, client_id: str):
        orders = self.get_orders_by_client(client_id)
        pending = [order for order in orders if order["status"] == "pending"]
        return pending
    
    def get_payments_for_month(self, year, month):
        pipeline = [
            {
                "$match": {
                    "$expr": {
                        "$and": [
                            {"$eq": [{"$year": "$date"}, year]},
                            {"$eq": [{"$month": "$date"}, month]}
                        ]
                    }
                }
            }
        ]
        results = list(self.db.payments.aggregate(pipeline))
        return results
    
    def get_payments(self):
        return list(self.db.payments.find({}))
    
    def get_attendance_percentage_by_class(self, class_id: str):
        total = self.db.attendance.count_documents({"class_id": ObjectId(class_id)})
        attended = self.db.attendance.count_documents({"class_id": ObjectId(class_id), "attended": True})

        if total == 0:
            return 0

        return (attended / total) * 100
    
    def get_drop_off_rate(self):
        total_clients = self.db.clients.count_documents({})
        clients_with_attendance = len(self.db.attendance.distinct("client_id"))

        if total_clients == 0:
            return 0
        
        drop_off_rate = ((total_clients - clients_with_attendance) / total_clients) * 100
        return drop_off_rate
