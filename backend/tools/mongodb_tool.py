from backend.models.schemas import db
from bson import ObjectId
from datetime import datetime

class MongoDBTool:
    def get_client(self, identifier: str):
        """
        identifier: name, email, or phone
        """
        query = {
            "$or": [
                {"name": identifier},
                {"email": identifier},
                {"phone": identifier}
            ]
        }
        return db.clients.find_one(query)
    
    def get_orders_by_client(self, client_id: str):
        return list(db.orders.find({"client_id": ObjectId(client_id)}))
    
    def get_order_by_id(self, order_id: str):
        return db.orders.find_one({"_id": ObjectId(order_id)})

    def get_payments_by_order(self, order_id: str):
        return list(db.payments.find({"order_id": ObjectId(order_id)}))
    
    def get_courses(self, instructor=None, status=None):
        query = {}
        if instructor:
            query["instructor"] = instructor
        if status:
            query["status"] = status
        return list(db.courses.find(query))
    
    def get_classes(self, status=None, instructor=None):
        query = {}
        if status:
            query["status"] = status
        if instructor:
            query["instructor"] = instructor
        return list(db.classes.find(query))
    
    def get_attendance_by_class(self, class_id: str):
        return list(db.attendance.find({"class_id": ObjectId(class_id)}))
    
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
     results = list(self.db["payments"].aggregate(pipeline))
     return results
    
    def get_payments(self):
     return list(db.payments.find({}))
    
    def get_attendance_percentage_by_class(self, class_id: str):
     """
     Calculates attendance percentage for a given class_id
     """
     total = db.attendance.count_documents({"class_id": ObjectId(class_id)})
     attended = db.attendance.count_documents({"class_id": ObjectId(class_id), "attended": True})

     if total == 0:
        return 0

     return (attended / total) * 100
    
    def get_drop_off_rate(self):
     """
     Calculates drop-off rate: clients with no attendance
     """
     total_clients = db.clients.count_documents({})
     clients_with_attendance = len(
        db.attendance.distinct("client_id")
     )

     if total_clients == 0:
        return 0
    
     drop_off_rate = ((total_clients - clients_with_attendance) / total_clients) * 100
     return drop_off_rate


    
 


