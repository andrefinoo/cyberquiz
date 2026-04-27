import sqlite3

conn = sqlite3.connect("mio_database.db")
cursor = conn.cursor()

def classifica_utenti(cursor):
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

def Percentuale_Correttezza_Categoria():
    ...

def Top10_Domande_Sbagliate():
    ...

def Tempo_Medio_Completamento_Quiz():
    ...

def Andamento_Utente():
    ... 

def EsportazioneCSV():
    ...