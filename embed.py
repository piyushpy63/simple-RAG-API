import chromadb

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("docs")

with open("django.txt", "r") as f:
    text = f.read()

collection.add(documents=[text], ids=["django"])

print("Embedding stored in Chroma")
