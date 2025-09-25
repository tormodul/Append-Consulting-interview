import os
import httpx
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from typing import List, Dict

app = FastAPI(title="LLM Tools API")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# URL of the Consultant API service
CONSULTANT_API_URL = "http://consultant-api:8000/consultants"

# API Endpoint
@app.get("/available-consultants/summary")
async def get_consultant_summary(my_availability_percent: int, required_skill: str):
    """
    Fetches consultant data, filters it, and returns an LLM-generated summary.
    """
    
    try:
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(CONSULTANT_API_URL)
            response.raise_for_status()  
            all_consultants = response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Could not connect to Consultant API: {e}")
    
    available_consultants = [
        c for c in all_consultants
        if (100 - c["load_percent"]) >= my_availability_percent and required_skill.lower() in c["skills"]
    ]

    if not available_consultants:
        return {"summary": f"No consultants found with at least {my_availability_percent}% availability and the skill '{required_skill}'."}

    prompt = f"""
    Based on the following data about {len(available_consultants)} available consultants, please generate a brief, human-readable summary.
    The user is looking for consultants with at least {my_availability_percent}% availability and the skill '{required_skill}'.

    Data:
    {available_consultants}

    The summary must start by stating the correct number of consultants found, which is {len(available_consultants)}. Then, list each one with their name and their availability.
    Be concise and professional.
    """

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes data concisely."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=150,
        )
        summary_text = completion.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with LLM service: {e}")

    return {"summary": summary_text}