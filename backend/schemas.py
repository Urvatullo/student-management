from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    age: int
    group: str

class StudentUpdate(BaseModel):
    name: str
    age: int
    group: str