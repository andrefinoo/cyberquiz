from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    password_hash: str
    created_at: str

@dataclass
class Question:
    id: int
    category: str
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    difficulty: int

@dataclass
class Attempt:
    id: int
    user_id: int
    score: int
    correct_count: int
    wrong_count: int
    duration_seconds: int
    created_at: str

@dataclass
class AttemptAnswer:
    id: int
    attempt_id: int
    question_id: int
    user_answer: str
    is_correct: int
