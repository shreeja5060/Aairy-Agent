import chromadb
from sentence_transformers import SentenceTransformer
import os
import time

# Setup
VAULT_PATH = "D:\\Aairy_brain"
DB_PATH = "D:\\aairy-rag\\db"

# Initialize
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection("aairy_memory")

def index_vault():
    """Read all MD files and index into ChromaDB"""
    print("Indexing Obsidian vault...")
    
    for root, dirs, files in os.walk(VAULT_PATH):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Convert to vector and store
                embedding = model.encode(content).tolist()
                collection.upsert(
                    documents=[content],
                    embeddings=[embedding],
                    ids=[filepath],
                    metadatas=[{"file": file, "path": filepath}]
                )
                print(f" Indexed: {file}")
    
    print("Vault indexing complete!")

def search_memory(query, n_results=3):
    """Search vault by meaning"""
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results

def main():
    # Index vault
    index_vault()
    
    print("\n Aairy RAG Memory Ready!")
    print("Type your question to search Aairy's memory")
    print("Type 'quit' to exit\n")
    
    while True:
        query = input("Search memory: ")
        if query.lower() == 'quit':
            break
            
        results = search_memory(query)
        
        print("\n Relevant memories found:")
        for i, doc in enumerate(results['documents'][0]):
            file = results['metadatas'][0][i]['file']
            print(f"\n--- {file} ---")
            print(doc[:500])
            print("...")
        print("\n")

if __name__ == "__main__":
    main()