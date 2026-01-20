from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import chromadb
import ollama
from pydantic import BaseModel

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")

@app.get("/")
def read_root():
    return FileResponse('static/index.html')

@app.post("/query")
def query(query: str):
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    context = results["documents"][0][0] if results["documents"] else ""

    prompt=f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer clearly and concisely:"
    
    import os
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    print(f"Connecting to Ollama at: {host}")
    client = ollama.Client(host=host)
    response = client.generate(model="tinyllama", prompt=prompt)

    return {"answer": response["response"]}

class GenerateRequest(BaseModel):
    context: str
    question: str

@app.post("/generate")
def generate(request: GenerateRequest):
    import os
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    client = ollama.Client(host=host)
    
    prompt = f"Context:\n{request.context}\n\nQuestion: {request.question}\n\nAnswer clearly and concisely:"
    print(f"Generating with prompt len: {len(prompt)}")
    response = client.generate(model="tinyllama", prompt=prompt)
    print(f"Ollama response: {response}")
    return {"response": response["response"]}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)