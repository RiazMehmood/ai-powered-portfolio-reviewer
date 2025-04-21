from fastapi import FastAPI
from pydantic import BaseModel
from services.openai_review import generate_review

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ReviewRequest(BaseModel):
    url: str

@app.post("/review")
async def review_endpoint(request: ReviewRequest):
    try:
        review = await generate_review(request.url)
        return {"review": review}
    except Exception as e:
        return {"error": str(e)}
