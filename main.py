import asyncio
import os
from typing import Dict
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles # Optional, if you have a CSS/JS folder
# 1. Load Environment Variables
load_dotenv()
BASE_URL = os.getenv("BASE_URL") 
API_KEY = os.getenv("API_KEY") 
MODEL_NAME = os.getenv("MODEL_NAME") 

# 2. FastAPI Initialization
app = FastAPI(title="AI LinkedIn Post Generator API")

# 3. Pydantic Schemas
class PostRequest(BaseModel):
    """Input from the user"""
    topic: str
    language: str | None = None

class TopicClassification(BaseModel):
    """Internal schema for the router"""
    category: str = Field(description="The category of the topic, exactly 'technology' or 'general'")

class FinalOutput(BaseModel):
    """The structured output returned to the user"""
    topic_name: str = Field(description="The main topic of the text with grammatical correct form")
    topic_class: str = Field(description="which topic is selected by the agent either general or technology")
    topic_confidence: float = Field(description="how much confidence the agent has in its topic selection classification")
    post: str = Field(description="final output formatted for LinkedIn with icons and emoji and suggestions")
    translation_confidence: float = Field(description="Confidence score for language detection, between 0 and 1")

# 4. LangChain Components
# Set request_timeout to prevent hanging connections
llm = ChatOpenAI(
    model=MODEL_NAME, 
    temperature=0.7,
    base_url=BASE_URL, 
    api_key=API_KEY,
    max_retries=2
)

# Binding Pydantic models to create structured workers
structured_router = llm.with_structured_output(TopicClassification)
structured_writer = llm.with_structured_output(FinalOutput)

# 5. Specialized Prompts
router_prompt = ChatPromptTemplate.from_template(
    "Classify the following topic as 'technology' or 'general'. Topic: {topic}"
)

tech_template = """You are a Technology Expert. 
Analyze the topic: "{topic}".
1. {language_instruction} and correct the topic name grammatically.
2. Classify as 'technology'.
3. Write a 2-4 paragraph LinkedIn post in the required language.
4. Use industry terms, professional icons, and emojis.
5. Provide a strategic engagement question at the end."""

general_template = """You are a Professional Content Creator. 
Analyze the topic: "{topic}".
1. {language_instruction} and correct the topic name grammatically.
2. Classify as 'general'.
3. Write a 2-4 paragraph LinkedIn post in the required language.
4. Use relatable icons, emojis, and a thoughtful call-to-action (CTA) at the end."""

# 6. Chain Definitions
router_chain = router_prompt | structured_router
tech_writer = ChatPromptTemplate.from_template(tech_template) | structured_writer
general_writer = ChatPromptTemplate.from_template(general_template) | structured_writer

# 7. FastAPI Endpoint with Conditional Routing Logic
@app.post("/generate", response_model=FinalOutput)
async def generate_post(request: PostRequest):
    try:
        # Step 1: Route the topic using the structured router
        classification = await router_chain.ainvoke({"topic": request.topic})
        
        # Log for debugging in your terminal
        print(f"--- Routing Decision ---")
        print(f"Topic: {request.topic}")
        print(f"Language: {request.language}")
        print(f"Decision: {classification.category}")

        # Set language instruction
        language_instruction = f"Write the post in {request.language}" if request.language else "Detect the input language and write the post in that language"

        # Step 2: Conditional Handover logic
        # Using a more robust check for 'technology'
        if "technology" in classification.category.lower():
            result = await tech_writer.ainvoke({"topic": request.topic, "language_instruction": language_instruction})
        else:
            result = await general_writer.ainvoke({"topic": request.topic, "language_instruction": language_instruction})
            
        return result
        
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))



# ... (keep your existing Pydantic models and chains) ...

# Add this endpoint to serve the UI
@app.get("/", response_class=FileResponse)
async def read_index():
    return "index.html"

# 8. Server Execution
if __name__ == "__main__":
    import uvicorn
    # Use 127.0.0.1 for local testing
    uvicorn.run(app, host="127.0.0.1", port=8000)