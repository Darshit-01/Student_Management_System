from pydantic import BaseModel,EmailStr
from typing import Optional

class Student(BaseModel):
    id: Optional[int] = None
    name: str
    internship_domain: str
    phone_no: str
    email: EmailStr
    
class Student_Update(BaseModel):
    id: int
    name: Optional[str] = None
    internship_domain: Optional[str] = None
    phone_no: Optional[str] = None
    email: Optional[EmailStr] = None