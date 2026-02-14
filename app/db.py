from typing import List, Optional, Dict
from app.models import User, Course, Enrollment

class InMemoryDB:
    def __init__(self):
        self.users: List[User] = []
        self.courses: List[Course] = []
        self.enrollments: List[Enrollment] = []

    def get_user(self, user_id: int) -> Optional[User]:
        return next((u for u in self.users if u.id == user_id), None)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return next((u for u in self.users if u.email == email), None)

    def get_course(self, course_id: int) -> Optional[Course]:
        return next((c for c in self.courses if c.id == course_id), None)
    
    def get_course_by_code(self, code: str) -> Optional[Course]:
        return next((c for c in self.courses if c.code == code), None)

    def get_enrollment(self, enrollment_id: int) -> Optional[Enrollment]:
        return next((e for e in self.enrollments if e.id == enrollment_id), None)

    def get_student_enrollments(self, student_id: int) -> List[Enrollment]:
        return [e for e in self.enrollments if e.user_id == student_id]

    def get_course_enrollments(self, course_id: int) -> List[Enrollment]:
        return [e for e in self.enrollments if e.course_id == course_id]

    def is_enrolled(self, user_id: int, course_id: int) -> bool:
        return any(e.user_id == user_id and e.course_id == course_id for e in self.enrollments)

db = InMemoryDB()
