import redis

redis_client = redis.Redis(
    host="partner-cloth-pruned-54293.db.redis.io",
    port=16345,
    password="I4pp7MqnfZ023xA2bN2Wf7CarKimADO2" 
)

connection_status =redis_client.ping()

if connection_status:
    print("Connected to Redis!")
else:
    print("The connection to Redis was unsuccessful!")

exists_result = redis_client.exists("other_key")  # Revisar si un key existe
ttl_result = redis_client.ttl("important_key")  # Revisar el time to live de un key

print("Exists:", exists_result)
print("TTL:", ttl_result)