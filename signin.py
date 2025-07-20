from fastapi import Form, HTTPException, APIRouter
from models import fake_users

router = APIRouter()

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user = fake_users.get(username)
    if user and user["password"] == password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
