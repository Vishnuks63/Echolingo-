import hashlib
import hmac
import os
import random
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ai_service import translation_service
from database import Question, User, get_db

app = FastAPI(title="EchoLingo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class UserLogin(BaseModel):
    email: str
    password: str


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310_000)
    return f"pbkdf2_sha256$310000${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations, salt_hex, digest_hex = stored_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            bytes.fromhex(salt_hex),
            int(iterations),
        )
        return hmac.compare_digest(digest.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


@app.post("/register")
async def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
    )
    db.add(new_user)
    try:
        db.commit()
        return {"message": "Registration successful"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Registration failed")


@app.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful", "username": db_user.username}


@app.get("/questions/{language}/{level}")
async def get_questions(language: str, level: str, db: Session = Depends(get_db)):
    questions = db.query(Question).filter(
        Question.language == language,
        Question.level == level,
    ).all()

    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")

    selected = random.sample(questions, min(5, len(questions)))
    return selected


@app.post("/translate")
async def translate(text: str, target_language: str):
    translated = translation_service.translate(text, target_language)
    if not translated:
        raise HTTPException(status_code=500, detail="Translation failed")
    return {"translated_text": translated}


@app.post("/quiz/score")
async def calculate_score(answers: list, current_score: int):
    return {"score": current_score, "level": "intermediate"}
