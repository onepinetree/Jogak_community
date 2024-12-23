import asyncio
from concurrent.futures import ThreadPoolExecutor
from firebase import startups
import numpy as np
from openai import OpenAI
import os

API_KEY = os.getenv('API_KEY')

client = OpenAI(api_key=API_KEY)

def get_embeddings(text: str, model: str = "text-embedding-ada-002") -> list:
    for _ in range(3):
        try:
            return client.embeddings.create(input=text, model=model).data[0].embedding
        except:
            continue
    return []

def cosine_similarity(vec1: list, vec2: list, normalize: bool = True) -> float:
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    if normalize:
        return np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return np.dot(vec1, vec2) / (norm1 * norm2)

async def fetch_embedding(executor, text, model="text-embedding-ada-002"):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, get_embeddings, text, model)

async def calculate_similarity(executor, embedding1, embedding2):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, cosine_similarity, embedding1, embedding2, True)

async def calculate_similarities(user_orenge):
    executor = ThreadPoolExecutor()
    try:
        # Step 1: Fetch embeddings concurrently
        embeddings_tasks = {startup: fetch_embedding(executor, startup) for startup, explanation in startups.items()}
        embeddings = {startup: await task for startup, task in embeddings_tasks.items()}

        orenge_embedding = await fetch_embedding(executor, user_orenge)

        # Step 2: Calculate similarities concurrently
        similarity_tasks = {
            startup: calculate_similarity(executor, orenge_embedding, embedding)
            for startup, embedding in embeddings.items()
        }
        similarities = {startup: await task for startup, task in similarity_tasks.items()}

        # Step 3: Sort results by similarity
        sorted_similarities = dict(sorted(similarities.items(), key=lambda item: item[1], reverse=True))
        return sorted_similarities

    finally:
        executor.shutdown()

def get_sorted_similarities(user_jogak):
    result = asyncio.run(calculate_similarities(user_jogak))
    updated_dict = {key: startups.get(key, result[key]) for key in result}
    return updated_dict

