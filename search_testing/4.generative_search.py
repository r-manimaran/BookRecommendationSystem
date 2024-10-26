import os
from dotenv import load_dotenv
import weaviate
from weaviate.classes.init import Auth, AdditionalConfig, Timeout

load_dotenv()

#load environment variables from .env
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#create the Weaviate client
client = weaviate.connect_to_weaviate_cloud(
    cluster_url = WEAVIATE_CLUSTER_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
    headers={
        "X-OpenAI-Api-Key": OPENAI_API_KEY
    })
# test the connection and print
print(client.is_ready())
print(client.is_connected())

#get the books collection
books = client.collections.get("Book")

#perform Generative Search
response = books.generate.near_text(
    query="technology, data structures and algorithm, distriuted systems",
    limit = 2,
    single_prompt="Explain why this book might be intresting to someone who likes playing violin, rock climbing, and doing yoga. the book's tile is {title} with a description: {description} and is in the genre:{categories}."
)
print(response.objects[0].generated)
client.close()
