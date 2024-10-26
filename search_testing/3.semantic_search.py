import os
from dotenv import load_dotenv
import weaviate
from weaviate.classes.init import Auth, AdditionalConfig, Timeout

load_dotenv()

#load the environment variables
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("Read Environment variables successfully")

#create the Weaviate client
client = weaviate.connect_to_weaviate_cloud(
    cluster_url = WEAVIATE_CLUSTER_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
    headers={
        "X-OpenAI-Api-Key": OPENAI_API_KEY
    })
print("Connected to Weaviate successfully")
# test the connection and print
print(client.is_ready())
print(client.is_connected())

try:
    #get the books collection
    books = client.collections.get("Book")
    print("Accessed Books collection successfully")

    #perform Semantic Search
    response = books.query.near_text(
        query="fantasy",
        limit=2        
    )

    print()
    for book in response.objects:
        print(book.properties)
        print("--------------------------------------------------")
        print()
except Exception as e:
    print("Error: ", e)
finally:
    print("Semantic search completed")    
    client.close()  