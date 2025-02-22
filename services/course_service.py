from entities.course import Course
from repository.course_repository import CourseRepository


class CourseService:
    def __init__(self, course_repository: CourseRepository):
        self.course_repository = course_repository

    def create_course(self, data):
        validattion_error, course = Course.validate(data)
        if validattion_error:
            return validattion_error, None
        course = course.serialize()
        return self.course_repository.create(course)

    def get_admin_courses(self, skip: int, limit: int):
        return self.course_repository.get_admin_courses(skip, limit)

    def get_mentor_courses(self, author_id: str, skip: int, limit: int):
        return self.course_repository.get_mentor_courses(author_id, skip, limit)

    def get_learner_courses(self, user_id: str, skip: int, limit: int):
        return self.course_repository.get_learner_courses(user_id, skip, limit)

    def get_all_courses(self, skip: int, limit: int):
        return self.course_repository.get_all_courses(skip, limit)

    def update_course(self, course_id: str, updates: dict):
        return self.course_repository.update(course_id, updates)

    def delete_course_by_id(self, course_id: str):

        return self.course_repository.delete(course_id)

    def get_course_by_id(self, course_id: str):
        return self.course_repository.get_course_by_id(course_id)

    def get_courses_by_category(self, category_id: str, skip: int, limit: int):
        return self.course_repository.get_courses_by_category(category_id, skip, limit)
    
    def update_publish_status(self, course_id: str, is_published: bool):
        return self.course_repository.update_publish_status(course_id, is_published)



    

   