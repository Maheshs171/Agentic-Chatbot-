from pinecone import Pinecone
from langchain.tools import tool
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME


# Initialize Pinecone client
pinecone = Pinecone(api_key=PINECONE_API_KEY)
index = pinecone.Index(PINECONE_INDEX_NAME)

@tool
def rag_retrieval_tool(query: str) -> str:
    """
    This tool retrieves relevant information from the vector store based on the user's query.
    Uses Pinecone's internal embedding and reranking models.
    """
    try:
        ranked_results = index.search_records(
            namespace="hr4s", 
            # namespace="mark1", 
            query={
                "inputs": {"text": query},
                "top_k": 7
            },
            rerank={
                "model": "bge-reranker-v2-m3",
                "top_n": 5,
                "rank_fields": ["text"]
            },
            # fields=["category", "text"]
        )

        results = ranked_results.result.hits
        if not results:
            return "Sorry, I couldn't find any relevant information."
        # print("Ranked Results from pinecone ---- :", results)
        
        # processed_results = []
        # try:
        #     for i in range(len(results)):  
        #         m = results[i]["fields"]["text"]
        #         processed_results.append(m)
        #         print(f"Results from Pinecone ::: {m}")
        # except Exception as e:
        #     print(f"Error processing results: {e}")
        #     return "Sorry, I couldn't process the results."
        
        return f"Here’s what I found:\n\n{results}"

    except Exception as e:
        return f"Error retrieving context from Pinecone: {e}"
