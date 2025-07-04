import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr, Field
from pydantic import GetCoreSchemaHandler

from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from pydantic_core import core_schema
load_dotenv()

mongodb_uri = os.getenv("MONGODB_URI")

client = MongoClient(mongodb_uri)
db = client["multiagent_db"]




class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema()
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class EnrolledService(BaseModel):
    course_id: PyObjectId
    status: str


class Client(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    email: EmailStr
    phone: str
    enrolled_services: List[EnrolledService]
    created_at: datetime


class Order(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    client_id: PyObjectId
    service_name: str
    amount: float
    status: str
    created_at: datetime


class Payment(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    order_id: PyObjectId
    amount: float
    payment_date: datetime
    method: str


class Course(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    title: str
    description: str
    instructor: str
    status: str
    start_date: datetime
    end_date: datetime


class Class(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    course_id: PyObjectId
    date: datetime
    instructor: str
    status: str
    capacity: int


class Attendance(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    class_id: PyObjectId
    client_id: PyObjectId
    attended: bool
