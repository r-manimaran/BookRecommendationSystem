import weaviate
import weaviate.classes as wvc
import weaviate.classes.config as wc
from weaviate.classes.init import Auth

#Read config from .env file
import os
from dotenv import load_dotenv
load_dotenv()

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

#check if the client is ready
print(client.is_ready())

#Delete the existing schema if it exists
client.collections.delete(name = "Book") 
print("Existing schema deleted")
print(client.is_connected())

questions = client.collections.create(
    name ="Book",
    vectorizer_config= wvc.config.Configure.Vectorizer.text2vec_openai(model="text-embedding-3-small"),
    generative_config= wvc.config.Configure.Generative.openai(model="gpt-3.5-turbo"),
    properties=[
        wc.Property(name="title", data_type=wc.DataType.TEXT),
        wc.Property(name="isbn10", data_type=wc.DataType.TEXT, skip_vectorization=True),
        wc.Property(name="isbn13", data_type=wc.DataType.TEXT, skip_vectorization=True),
        wc.Property(name="categories", data_type= wc.DataType.TEXT),
        wc.Property(name="thumbnail", data_type=wc.DataType.TEXT, skip_vectorization=True),
        wc.Property(name="description", data_type=wc.DataType.TEXT),      
        wc.Property(name="num_pages", data_type=wc.DataType.INT),
        wc.Property(name="average_rating", data_type=wc.DataType.NUMBER),
        wc.Property(name="published_year", data_type=wc.DataType.INT),
        wc.Property(name="authors", data_type=wc.DataType.TEXT, skip_vectorization=True)
      
    ],
)
print("New schema created")
client.close()