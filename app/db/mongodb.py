from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client["test_vocacional"]

# Colecciones
user_collection = database.get_collection("users")
test_collection = database.get_collection("tests")
result_collection = database.get_collection("results")
answer_collection = database.get_collection("answers")
