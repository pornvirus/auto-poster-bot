import motor.motor_asyncio, os

MONGO_DB_URI = os.environ['MONGO_DB_URI']
up = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI)['channelautopostbot']['user']

async def add_user(id, medias='', limit='off'):
    await up.insert_one({'id': id, 'medias': medias, 'limit': limit})

async def get_user(id):
    return await up.find_one({'id': id})

async def is_user_exist(id):
    return True if await up.find_one({'id': id}) else False

async def add_media(id, file_id):
    await up.update_one({'id': id}, {'$set': {'medias': file_id}})

async def remove_all_media(id):
    await up.update_one({'id': id}, {'$set': {'medias': ''}})

async def limit_on(id):
    await up.update_one({'id': id}, {'$set': {'limit': 'on'}})

async def limit_off(id):
    await up.update_one({'id': id}, {'$set': {'limit': 'off'}})