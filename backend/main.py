from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

from database import SessionLocal, Base, engine
from models import Group, Student

from schemas import (
    GroupCreate,
    GroupResponse,
    StudentCreate,
    StudentResponse,
    StudentUpdate,
    GroupStatsResponse,
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Student Management API is working!"}

@app.get("/groups", response_model=list[GroupResponse])
def get_groups(db: Session = Depends(get_db)):
    statement = select(Group).order_by(Group.id)
    return db.scalars(statement).all()

@app.get("/groups/stats", response_model=list[GroupStatsResponse])
def get_group_stats(db: Session = Depends(get_db)):
    statement = (
        select(
            Group.id,
            Group.name,
            func.count(Student.id).label("student_count")
        )
        .outerjoin(Student, Group.id == Student.group_id)
        .group_by(Group.id, Group.name)
        .order_by(Group.id)
    )

    results = db.execute(statement).all()

    return [
        {
            "id": group_id,
            "name": group_name,
            "student_count": student_count
        }
        for group_id, group_name, student_count in results
    ]

@app.post("/groups", response_model=GroupResponse)
def create_group(
    group: GroupCreate,
    db: Session = Depends(get_db)
):
    statement = select(Group).where(Group.name == group.name)
    existing_group = db.scalar(statement)

    if existing_group is not None:
        raise HTTPException(
            status_code=400,
            detail="Group already exists"
        )

    new_group = Group(name=group.name)

    try:
        db.add(new_group)
        db.commit()
        db.refresh(new_group)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create group"
        )

    return new_group

@app.get("/students", response_model=list[StudentResponse])
def get_students(
    search: str | None = None,
    group_id: int | None = None,
    db: Session = Depends(get_db)
):
    statement = (
        select(Student)
        .options(selectinload(Student.group))
    )

    if search:
        statement = statement.where(
            Student.name.ilike(f"%{search}%")
        )

    if group_id is not None:
        statement = statement.where(
            Student.group_id == group_id
        )

    statement = statement.order_by(Student.id)

    return db.scalars(statement).all()

@app.get("/students/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

@app.post("/students", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    selected_group = db.get(Group, student.group_id)

    if selected_group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    new_student = Student(
        name=student.name,
        age=student.age,
        group_id=student.group_id
    )

    try:
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create student"
        )

    return new_student

@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db)
):
    existing_student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if existing_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    existing_student.name = student.name
    existing_student.age = student.age
    selected_group = db.get(Group, student.group_id)

    if selected_group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    existing_student.group_id = student.group_id

    db.commit()
    db.refresh(existing_student)

    return existing_student

@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    existing_student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if existing_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    try:
        db.delete(existing_student)
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to delete student"
        )

    return {"message": "Student deleted successfully"}
