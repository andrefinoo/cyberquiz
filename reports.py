import csv
import db


def classifica_utenti():
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT users.username, AVG(attempts.score)
    FROM users
    JOIN attempts ON users.id = attempts.user_id
    GROUP BY users.id
    ORDER BY AVG(attempts.score) DESC
    LIMIT 5
    """)

    risultati = cursor.fetchall()
    conn.close()

    print("\n--- TOP 5 UTENTI PER MEDIA PUNTEGGIO ---")

    if not risultati:
        print("Nessun dato disponibile.")
        return

    for username, media in risultati:
        print(f"{username}: {media:.2f}")


def correttezza_per_categoria():
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT questions.category,
           COUNT(*) AS totale,
           SUM(attempt_answers.is_correct) AS corrette,
           ROUND(SUM(attempt_answers.is_correct) * 100.0 / COUNT(*), 2) AS percentuale
    FROM questions
    JOIN attempt_answers ON questions.id = attempt_answers.question_id
    GROUP BY questions.category
    ORDER BY percentuale DESC
    """)

    risultati = cursor.fetchall()
    conn.close()

    print("\n--- CORRETTEZZA PER CATEGORIA ---")

    if not risultati:
        print("Nessun dato disponibile.")
        return

    for categoria, totale, corrette, percentuale in risultati:
        print(f"{categoria}: {percentuale}% ({corrette}/{totale})")


def domande_piu_sbagliate():
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT questions.id, questions.text, COUNT(*) AS errori
    FROM questions
    JOIN attempt_answers ON questions.id = attempt_answers.question_id
    WHERE attempt_answers.is_correct = 0
    GROUP BY questions.id
    ORDER BY errori DESC
    LIMIT 10
    """)

    risultati = cursor.fetchall()
    conn.close()

    print("\n--- TOP 10 DOMANDE PIÙ SBAGLIATE ---")

    if not risultati:
        print("Nessun dato disponibile.")
        return

    for question_id, testo, errori in risultati:
        print(f"ID {question_id} - {errori} errori - {testo}")


def tempo_medio_quiz():
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT AVG(duration_seconds)
    FROM attempts
    """)

    risultato = cursor.fetchone()
    conn.close()

    print("\n--- TEMPO MEDIO QUIZ ---")

    if risultato[0] is None:
        print("Nessun dato disponibile.")
        return

    print(f"Tempo medio: {risultato[0]:.2f} secondi")


def andamento_utente(user_id):
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT score, correct_count, wrong_count, duration_seconds, created_at
    FROM attempts
    WHERE user_id = ?
    ORDER BY created_at DESC
    LIMIT 5
    """, (user_id,))

    risultati = cursor.fetchall()
    conn.close()

    print("\n--- ULTIMI 5 TENTATIVI ---")

    if not risultati:
        print("Nessun tentativo trovato.")
        return

    for score, corrette, errate, tempo, data in risultati:
        print(f"{data} | Score: {score} | Corrette: {corrette} | Errate: {errate} | Tempo: {tempo}s")


def esporta_csv():
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT users.username, attempts.score, attempts.correct_count,
           attempts.wrong_count, attempts.duration_seconds, attempts.created_at
    FROM attempts
    JOIN users ON users.id = attempts.user_id
    ORDER BY attempts.created_at DESC
    """)

    risultati = cursor.fetchall()
    conn.close()

    if not risultati:
        print("Nessun dato da esportare.")
        return

    with open("report_quiz.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Score", "Corrette", "Errate", "Tempo", "Data"])
        writer.writerows(risultati)

    print("File report_quiz.csv creato correttamente.")


def report_globali():
    classifica_utenti()
    correttezza_per_categoria()
    domande_piu_sbagliate()
    tempo_medio_quiz()