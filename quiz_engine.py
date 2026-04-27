import time
import random
import db
from models import Question

def run_quiz(user_id: int):
    """
    Esegue il quiz per l'utente specificato.
    Gestisce la scelta della categoria, il recupero delle domande,
    il ciclo di gioco, il punteggio e il salvataggio dei risultati.
    """
    print("\n=== AVVIO QUIZ ===")
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Recupero le categorie disponibili
    cursor.execute("SELECT DISTINCT category FROM questions")
    categories = [row[0] for row in cursor.fetchall()]
    
    if not categories:
        print("Nessuna domanda presente nel database.")
        conn.close()
        return

    print("Categorie disponibili:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}) {cat}")
    print(f"{len(categories) + 1}) Quiz Casuale (Tutte le categorie)")
    
    cat_choice = input("\nScegli una categoria (inserisci il numero): ")
    selected_category = None
    try:
        cat_idx = int(cat_choice) - 1
        if 0 <= cat_idx < len(categories):
            selected_category = categories[cat_idx]
    except ValueError:
        pass # Se inserisce qualcosa non valido o sceglie "casuale", resta None
    
    num_questions_str = input("Quante domande vuoi affrontare? (Default 5): ")
    try:
        num_questions = int(num_questions_str)
        if num_questions <= 0:
            num_questions = 5
    except ValueError:
        num_questions = 5
        
    if selected_category:
        print(f"\nHai scelto di affrontare {num_questions} domande nella categoria '{selected_category}'.")
    else:
        print(f"\nHai scelto di affrontare {num_questions} domande in modalità casuale.")
    
    # Caricamento domande
    if selected_category:
        cursor.execute("SELECT * FROM questions WHERE category = ?", (selected_category,))
    else:
        cursor.execute("SELECT * FROM questions")
        
    rows = cursor.fetchall()
    
    if not rows:
        print("Non ci sono domande corrispondenti.")
        conn.close()
        return
        
    questions = []
    for r in rows:
        q = Question(
            id=r[0],
            category=r[1],
            text=r[2],
            option_a=r[3],
            option_b=r[4],
            option_c=r[5],
            option_d=r[6],
            correct_option=r[7],
            difficulty=r[8]
        )
        questions.append(q)
        
    # Mescola le domande e prendi il numero richiesto
    random.shuffle(questions)
    questions = questions[:num_questions]
    
    if len(questions) < num_questions:
        print(f"Nota: Sono disponibili solo {len(questions)} domande.")
        
    # Inizializzazione variabili per il quiz
    score = 0
    correct_count = 0
    wrong_count = 0
    answers_given = []
    
    print("\nPremi INVIO per iniziare...")
    input()
    
    start_time = time.time()
    
    # Ciclo di gioco
    for i, q in enumerate(questions, 1):
        print(f"\n--- Domanda {i}/{len(questions)} [Categoria: {q.category} | Difficoltà: {q.difficulty}] ---")
        print(q.text)
        print(f"A) {q.option_a}")
        print(f"B) {q.option_b}")
        print(f"C) {q.option_c}")
        print(f"D) {q.option_d}")
        
        user_answer = ""
        while user_answer not in ['A', 'B', 'C', 'D']:
            user_answer = input("La tua risposta (A/B/C/D): ").strip().upper()
            
        is_correct = 0
        if user_answer == q.correct_option.upper():
            print("✅ Risposta ESATTA!")
            is_correct = 1
            correct_count += 1
            # Calcolo punteggio: 10 punti base moltiplicati per la difficoltà se presente
            diff_multiplier = q.difficulty if q.difficulty and q.difficulty > 0 else 1
            score += 10 * diff_multiplier
        else:
            print(f"❌ Risposta ERRATA! Quella corretta era: {q.correct_option.upper()}")
            wrong_count += 1
            
        answers_given.append({
            'question_id': q.id,
            'user_answer': user_answer,
            'is_correct': is_correct
        })
        
    end_time = time.time()
    duration_seconds = int(end_time - start_time)
    
    print("\n=== RISULTATI QUIZ ===")
    print(f"Punteggio Totale: {score}")
    print(f"Risposte Esatte: {correct_count}")
    print(f"Risposte Errate: {wrong_count}")
    print(f"Tempo impiegato: {duration_seconds} secondi")
    
    # Salvataggio del tentativo nel database
    # Non usiamo db.insert_attempt perché ci serve il lastrowid
    cursor.execute("""
    INSERT INTO attempts (user_id, score, correct_count, wrong_count, duration_seconds)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, score, correct_count, wrong_count, duration_seconds))
    
    attempt_id = cursor.lastrowid
    
    # Salvataggio delle singole risposte date nel database
    for ans in answers_given:
        cursor.execute("""
        INSERT INTO attempt_answers (attempt_id, question_id, user_answer, is_correct)
        VALUES (?, ?, ?, ?)
        """, (attempt_id, ans['question_id'], ans['user_answer'], ans['is_correct']))
        
    conn.commit()
    conn.close()
    
    print("\nIl tuo tentativo e le risposte sono state salvate correttamente!")
