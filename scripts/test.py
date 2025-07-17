import weaviate
from weaviate.classes.init import Auth

client = weaviate.connect_to_local(
    host="172.29.215.160",  # Use a string to specify the host
    port=8080,
    grpc_port=50051,
    auth_credentials=Auth.api_key("1132a82169967f0e9daf61c9a7a6b79d")
)

print(client.is_ready())

client.close()
