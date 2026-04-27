import sqlite3

DB_NAME = "cyberquiz.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


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


def execute_query(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def fetch_one(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return dict(row)


def fetch_all(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# =========================
# UTENTI
# =========================

def insert_user(username, password_hash):
    execute_query("""
    INSERT INTO users (username, password_hash)
    VALUES (?, ?)
    """, (username, password_hash))


def find_user_by_username(username):
    return fetch_one("""
    SELECT *
    FROM users
    WHERE username = ?
    """, (username,))


# =========================
# DOMANDE
# =========================

def add_question(category, text, options, correct_option, difficulty):
    execute_query("""
    INSERT INTO questions (
        category, text,
        option_a, option_b, option_c, option_d,
        correct_option, difficulty
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        category,
        text,
        options[0],
        options[1],
        options[2],
        options[3],
        correct_option,
        difficulty
    ))


def insert_question(category, text, option_a, option_b, option_c, option_d, correct_option, difficulty):
    add_question(
        category,
        text,
        [option_a, option_b, option_c, option_d],
        correct_option,
        difficulty
    )


def edit_question(question_id, category, text, option_a, option_b, option_c, option_d, correct_option, difficulty):
    execute_query("""
    UPDATE questions
    SET category = ?,
        text = ?,
        option_a = ?,
        option_b = ?,
        option_c = ?,
        option_d = ?,
        correct_option = ?,
        difficulty = ?
    WHERE id = ?
    """, (
        category,
        text,
        option_a,
        option_b,
        option_c,
        option_d,
        correct_option,
        difficulty,
        question_id
    ))


def update_question(question_id, category, text, option_a, option_b, option_c, option_d, correct_option, difficulty):
    edit_question(
        question_id,
        category,
        text,
        option_a,
        option_b,
        option_c,
        option_d,
        correct_option,
        difficulty
    )


def delete_question(question_id):
    execute_query("""
    DELETE FROM questions
    WHERE id = ?
    """, (question_id,))


def get_question_by_id(question_id):
    return fetch_one("""
    SELECT *
    FROM questions
    WHERE id = ?
    """, (question_id,))


def get_all_questions():
    return fetch_all("""
    SELECT *
    FROM questions
    ORDER BY id
    """)


def get_questions_by_category(category):
    return fetch_all("""
    SELECT *
    FROM questions
    WHERE category = ?
    ORDER BY id
    """, (category,))


# =========================
# TENTATIVI QUIZ
# =========================

def insert_attempt(user_id, score, correct_count, wrong_count, duration_seconds):
    execute_query("""
    INSERT INTO attempts (
        user_id, score, correct_count, wrong_count, duration_seconds
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        score,
        correct_count,
        wrong_count,
        duration_seconds
    ))


def insert_attempt_answer(attempt_id, question_id, user_answer, is_correct):
    execute_query("""
    INSERT INTO attempt_answers (
        attempt_id, question_id, user_answer, is_correct
    )
    VALUES (?, ?, ?, ?)
    """, (
        attempt_id,
        question_id,
        user_answer,
        is_correct
    ))

def import_questions(questions):
    conn = get_connection()
    cursor = conn.cursor()

    for q in questions:
        cursor.execute("""
        INSERT INTO questions (
            category, text,
            option_a, option_b, option_c, option_d,
            correct_option, difficulty
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            q["category"],
            q["text"],
            q["option_a"],
            q["option_b"],
            q["option_c"],
            q["option_d"],
            q["correct_option"],
            q["difficulty"]
        ))

    conn.commit()
    conn.close()