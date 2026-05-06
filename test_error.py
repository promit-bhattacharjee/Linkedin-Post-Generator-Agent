import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

load_dotenv()
BASE_URL = os.getenv("BASE_URL") 
API_KEY = os.getenv("API_KEY") 
MODEL_NAME = os.getenv("MODEL_NAME")

print("BASE_URL:", BASE_URL)
print("MODEL_NAME:", MODEL_NAME)

class TopicClassification(BaseModel):
    category: str = Field(description="The category of the topic, exactly 'technology' or 'general'")

try:
    llm = ChatOpenAI(
        model=MODEL_NAME, 
        temperature=0.7,
        base_url=BASE_URL, 
        api_key=API_KEY,
        max_retries=2
    )
    structured_router = llm.with_structured_output(TopicClassification)
    res = structured_router.invoke("AI in Healthcare")
    print("Success:", res)
except Exception as e:
    print(f"Error: {e}")
