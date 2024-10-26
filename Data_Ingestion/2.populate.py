#Read the .csv file and populate the Weaviate Collection in the Weaviate Cluster
# File path: c:\Maran\StudyMaterials\Git\BookRecommendationSystem\Data_Ingestion\2.populate_collection.py
# Content:
import pandas as pd
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

#Read the .csv file
df = pd.read_csv("books.csv")
# convert only isbn13 to string
df['isbn13'] = df['isbn13'].astype(str)
df['num_pages'] = df['num_pages'].astype(str)
df['published_year']=df['published_year'].astype(str)
df['average_rating']=df['average_rating'].astype(str)

# Handle potential NaN values
df = df.fillna("")

#Convert the dataframe to a list of dictionaries
books = df.to_dict(orient="records")

#Populate the Weaviate Collection
for book in books:
    try:
        print("Populating collection with book: ", book["title"])
        # Get properties from the book
        properties = {
            "title": book["title"],
            "isbn10": book["isbn10"],
            "isbn13": book["isbn13"],
            "categories": book["categories"],
            "thumbnail": book["thumbnail"],
            "description": book["description"],
            "num_pages": book["num_pages"],
            "average_rating": book["average_rating"],
            "published_year": book["published_year"],
            "authors": book["authors"]
        }
        
        # print(properties)    
        # Add the book to the Weaviate Collection
        uuid = client.collections.get("Book").data.insert(properties)
        print("Book added with uuid: ", uuid)
    except Exception as e:
        print("Error adding book: ", book["title"])
        print(e)
        continue

print("Collection populated")
client.close()