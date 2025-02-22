from entities.category import Category
from repository.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def create_category(self, data):

        validataion_error, category = Category.validate(data)

        if validataion_error:
            return validataion_error, None
        category = category.serialize()

        return self.category_repository.create_category(category)

    def get_all_categories(self):
        return self.category_repository.get_all_categories()
    
    #
    def delete_category(self, category_id):
        return self.category_repository.delete_category(category_id)
    
