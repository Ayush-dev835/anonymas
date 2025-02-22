from repository.chapter_repository import ChapterRepository
from entities.chapter import Chapter


class ChapterService:
    def __init__(self, chapter_repository: ChapterRepository):
        self.chapter_repository = chapter_repository

    def create_cheapter(self, data):
        validation_error, chapter = Chapter.validate(data)

        if validation_error:
            return validation_error, None
        chapter = chapter.serialize()

        return self.chapter_repository.create_chapter(chapter)

    def get_chapter(self, course_id):
        return self.chapter_repository.get_chapter(course_id)

    
    #
    def delete_chapter(self, chapter_id):
        return self.chapter_repository.delete_chapter(chapter_id)