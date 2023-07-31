import redis, os
rdb = redis.Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], username=os.environ['REDIS_USER'], password=os.environ['REDIS_PASS'])

rdb.set("global_api_access", int(True))
rdb.set("ai_endpoints", int(True))
rdb.set("item_creation", int(True))
rdb.set("user_creation", int(True))