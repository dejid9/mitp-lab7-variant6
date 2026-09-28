"""Модели SQLAlchemy для демонстрации ORM слоя базы данных."""

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List


class Base(DeclarativeBase):
    pass


class StudentModel(Base):
    __tablename__ = "orm_students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    group_name: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    enrollments: Mapped[List["EnrollmentModel"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )


class CourseModel(Base):
    __tablename__ = "orm_courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hours: Mapped[int] = mapped_column(Integer, nullable=False)

    enrollments: Mapped[List["EnrollmentModel"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )


class EnrollmentModel(Base):
    __tablename__ = "orm_enrollments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("orm_students.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("orm_courses.id"))
    grade: Mapped[int] = mapped_column(Integer, nullable=False)

    student: Mapped[StudentModel] = relationship(back_populates="enrollments")
    course: Mapped[CourseModel] = relationship(back_populates="enrollments")
