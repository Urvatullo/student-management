from pydantic import BaseModel, ConfigDict


class GroupCreate(BaseModel):
    name: str


class GroupResponse(GroupCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class StudentCreate(BaseModel):
    name: str
    age: int
    group_id: int


class StudentUpdate(StudentCreate):
    pass


class StudentResponse(StudentCreate):
    id: int
    group: GroupResponse

    model_config = ConfigDict(from_attributes=True)

class GroupStatsResponse(BaseModel):
    id: int
    name: str
    student_count: int