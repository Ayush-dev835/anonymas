from bson.objectid import ObjectId

class WatchTracking:
    def __init__(self, course_id: ObjectId, isChapter: bool, chapter_id: ObjectId, current_timestamp: int):
        self.course_id = course_id
        self.isChapter = isChapter
        self.chapter_id = chapter_id if isChapter else None
        self.current_timestamp = current_timestamp