"""db.py

Devi scrivere tutto ciò che riguarda il database SQLite.

Contiene:

- connessione al database cyberquiz.db
- creazione delle tabelle se non esistono
- funzioni per eseguire query
- funzioni per inserire utenti
- funzioni per cercare utenti
- funzioni per inserire domande
- funzioni per modificare/eliminare domande
- funzioni per salvare tentativi
- funzioni per salvare risposte date

Tabelle da creare:

users
questions
attempts
attempt_answers
models.py

Devi scrivere le classi/modelli dei dati.

Contiene classi come:

User
Question
Attempt
AttemptAnswer

Serve per rappresentare in Python i dati principali.

Esempio concettuale:

User:
- id
- username
- password_hash
- created_at

Question:
- id
- category
- text
- option_a
- option_b
- option_c
- option_d
- correct_option
- difficulty"""

import sqlite3

DB_NAME = "cyberquiz.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        category TEXT NOT NULL,
        text TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_option TEXT NOT NULL,
        difficulty INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        correct_count INTEGER NOT NULL,
        wrong_count INTEGER NOT NULL,
        duration_seconds INTEGER,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attempt_answers (
        id INTEGER PRIMARY KEY,
        attempt_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        user_answer TEXT NOT NULL,
        is_correct INTEGER NOT NULL,
        FOREIGN KEY (attempt_id) REFERENCES attempts(id),
        FOREIGN KEY (question_id) REFERENCES questions(id)
    )
    """)

    conn.commit()
    conn.close()

"""
- funzioni per eseguire query
- funzioni per inserire utenti
- funzioni per cercare utenti
- funzioni per inserire domande
- funzioni per modificare/eliminare domande
- funzioni per salvare tentativi
- funzioni per salvare risposte date"""

def execute_query(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def insert_user(username, password_hash):
    execute_query("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))

def find_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def insert_question(category, text, option_a, option_b, option_c, option_d, correct_option, difficulty):
    execute_query("""
    INSERT INTO questions (category, text, option_a, option_b, option_c, option_d, correct_option, difficulty)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (category, text, option_a, option_b, option_c, option_d, correct_option, difficulty))

def update_question(question_id, category, text, option_a, option_b, option_c, option_d, correct_option, difficulty):
    execute_query("""
    UPDATE questions
    SET category = ?, text = ?, option_a = ?, option_b = ?, option_c = ?, option_d = ?, correct_option = ?, difficulty = ?
    WHERE id = ?
    """, (category, text, option_a, option_b, option_c, option_d, correct_option, difficulty, question_id))

def delete_question(question_id):
    execute_query("DELETE FROM questions WHERE id = ?", (question_id,))

def insert_attempt(user_id, score, correct_count, wrong_count, duration_seconds):
    execute_query("""
    INSERT INTO attempts (user_id, score, correct_count, wrong_count, duration_seconds)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, score, correct_count, wrong_count, duration_seconds))

def insert_attempt_answer(attempt_id, question_id, user_answer, is_correct):
    execute_query("""
    INSERT INTO attempt_answers (attempt_id, question_id, user_answer, is_correct)
    VALUES (?, ?, ?, ?)
    """, (attempt_id, question_id, user_answer, is_correct))

