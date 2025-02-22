from pymongo import MongoClient
from configs_and_constants.constants import CollectionNames, Roles

def init_roles(db: MongoClient):
    if len(list(db.get_collection(CollectionNames.roles.value).find())):
        print("Roles are already initialized")
        return
    roles = []
    for role in [
        Roles.admin.value,
        Roles.learner.value,
        Roles.mentor.value,
        Roles.operational_team.value,
    ]:
        roles.append({"role": role})
    db.get_collection(CollectionNames.roles.value).insert_many(roles)
