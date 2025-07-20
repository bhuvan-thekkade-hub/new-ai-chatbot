import sys
# print(sys.path)

from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from maschemas import Message, InterviewRequest, InterviewFeedback
from utils import evaluate_response, generate_feedback
from signin import router as signin_router  # Import router FIRST
import os

# ✅ Create the app BEFORE using it
app = FastAPI()

# ✅ Then include the router
app.include_router(signin_router)

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../interviewbot/interviewbot")), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    # Serve the main interview.html page
    return FileResponse(os.path.join(os.path.dirname(__file__), "../interviewbot/interviewbot/interview.html"))

@app.get("/interview", response_class=HTMLResponse)
def interview_page():
    return FileResponse(os.path.join(os.path.dirname(__file__), "../interviewbot/interviewbot/interview.html"))

@app.get("/contact")
def handle_contact(msg: Message):
    print(f"Received message from {msg.name} ({msg.email}): {msg.message}")
    return {"message": "Your message has been received!"}

@app.post("/score", response_model=list[InterviewFeedback])
def score_interview(data: InterviewRequest):
    print(f"Evaluating interview for role: {data.role}")
    feedback = []
    for ans in data.responses:
        score = evaluate_response(ans.answer)
        fb = generate_feedback(ans.answer)
        feedback.append(InterviewFeedback(
            question=ans.question,
            score=score,
            feedback=fb
        ))
    return feedback
