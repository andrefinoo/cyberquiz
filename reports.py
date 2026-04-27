import sqlite3
import csv


def classifica_utenti(cursor):
    conn = sqlite3.connect("cyberquiz.db")
    cursor = conn.cursor()

    query = """
    SELECT users.username, AVG(attempts.score)
    FROM users
    JOIN attempts ON users.id = attempts.user_id
    GROUP BY users.username
    ORDER BY AVG(attempts.score) DESC
    """
    cursor.execute(query)
    risultati = cursor.fetchall()

    print("--- CLASSIFICA UTENTI ---")
    for utente in risultati:
        # Formattiamo a 2 cifre decimali
        print(f"Utente: {utente[0]:<15} | Media: {utente[1]:.2f}")
    
    return risultati
classifica_utenti()

# 3. Chiudi la connessione quando hai finito
# conn.close()  # Removed as conn is not defined here 
    

def Percentuale_Correttezza_Categoria():
    conn = sqlite3.connect("cyberquiz.db")
    cursor = conn.cursor()
    query = """
    SELECT questions.category, 
       CAST(SUM(CASE WHEN attempt_answers.is_correct = 1 THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100 AS percentage
    FROM questions
    JOIN attempt_answers ON questions.id = attempt_answers.question_id
    GROUP BY questions.category
    ORDER BY percentage DESC;
    """
    cursor.execute(query)
    risultati = cursor.fetchall()
    
    print("--- PercentUALE CORRETTEZZA PER CATEGORIA ---")
    for categoria in risultati:
        print(f"Categoria: {categoria[0]:<20} | Correttezza: {categoria[1]:.2f}%")
    
    conn.close()
    return risultati


def Top10_Domande_Sbagliate():
    conn = sqlite3.connect("cyberquiz.db")
    cursor = conn.cursor()

    query = """
    SELECT 
        questions.text, 
        COUNT(attempt_answers.id) AS sbagliate
    FROM questions
    JOIN attempt_answers ON questions.id = attempt_answers.question_id
    WHERE attempt_answers.is_correct = 0
    GROUP BY questions.id, questions.text
    ORDER BY sbagliate DESC
    LIMIT 10;
    """
    cursor.execute(query)
    risultati = cursor.fetchall()

    print("\n--- TOP 10 DOMANDE PIÙ SBAGLIATE ---")
    print("{:<60} {:<10}".format("DOMANDA", "Errori"))
    print("-" * 70)

    for domanda, conteggio in risultati:
        # Tronca la domanda se è troppo lunga da visualizzare bene
        testo_corto = (domanda[:57] + '...') if len(domanda) > 60 else domanda
        print(f"{testo_corto:<60} {conteggio:<10}")
    
    conn.close()


def Tempo_Medio_Completamento_Quiz():
    conn = sqlite3.connect("cyberquiz.db")
    cursor = conn.cursor()
    
    query = """
    SELECT 
        users.username, 
        AVG(attempts.duration_seconds) AS tempo_medio
    FROM users
    JOIN attempts ON users.id = attempts.user_id
    GROUP BY users.username
    ORDER BY tempo_medio DESC
    LIMIT 10;
    """
    cursor.execute(query)
    risultati = cursor.fetchall()
    
    print("\n--- TEMPO MEDIO DI COMPLETAMENTO (TOP 10) ---")
    print("{:<15} {:<15}".format("Utente", "Tempo (s)"))
    print("-" * 30)
    
    for username, tempo in risultati:
        print(f"{username:<15} {tempo:.1f}")
    
    conn.close()
    return risultati


def Andamento_Utente():
    conn = sqlite3.connect("cyberquiz.db")
    cursor = conn.cursor()
    
    query = """
    SELECT 
        users.username, 
        AVG(attempts.duration_seconds) AS tempo_medio
    FROM users
    JOIN attempts ON users.id = attempts.user_id
    GROUP BY users.username
    ORDER BY tempo_medio DESC
    LIMIT 10;
    """
    cursor.execute(query)
    risultati = cursor.fetchall()
    
    print("\n--- TEMPO MEDIO DI COMPLETAMENTO (TOP 10) ---")
    print("{:<15} {:<15}".format("Utente", "Tempo (s)"))
    print("-" * 30)
    
    for username, tempo in risultati:
        print(f"{username:<15} {tempo:.1f}")
    
    conn.close()
    return risultati
    

def EsportazioneCSV():
    conn = sqlite3.connect('cyberquiz.db')
    cursor = conn.cursor()

    # 1. Prendi TUTTE le domande, con la risposta esatta e la categoria
    query = """
    SELECT 
        questions.category, 
        questions.text AS domanda, 
        CASE 
            WHEN attempt_answers.is_correct = 1 THEN 'Corretta'
            ELSE 'Sbagliata'
        END AS risultato,
        attempt_answers.user_answer AS risposta_utente,
        attempts.score AS punteggio,
        attempts.duration_seconds AS tempo_secondi,
        attempts.created_at AS data_ora
    FROM questions
    JOIN attempt_answers ON questions.id = attempt_answers.question_id
    JOIN attempts ON attempt_answers.attempt_id = attempts.id
    ORDER BY attempts.created_at DESC;
    """

    cursor.execute(query)
    risultati = cursor.fetchall()

    # 2. Apri il file CSV in modalità scrittura ('w')
    with open('report_domande_cybersecurity.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Scrivi la riga di intestazione
        writer.writerow([
            "Categoria",
            "Domanda",
            "Risultato",
            "Risposta Utente",
            "Punteggio",
            "Tempo (s)",
            "Data/Ora"
        ])
        
        # Scrivi tutte le righe estratte dal database
        writer.writerows(risultati)

    print("\n✅ Report CSV creato con successo!")
    print("File salvato come: report_domande_cybersecurity.csv")

    conn.close()