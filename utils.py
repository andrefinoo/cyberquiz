"""utils.py

Devi scrivere le funzioni di supporto usate dagli altri file.

Contiene:

- validazione input
- pulizia input utente
- hashing password
- generazione salt, se fai il bonus
- controllo scelta A/B/C/D
- funzioni per stampare titoli/menu
- gestione data e ora
- eventuale logging eventi

Esempi di funzioni utili:

hash_password(password)
check_password(password, hash_salvato)
input_int(messaggio)
input_choice(messaggio, scelte_valide)
current_datetime()
data/questions.json

Devi scrivere almeno 30 domande iniziali in formato JSON.

Devono essere distribuite su almeno 5 categorie.

Categorie possibili:

phishing
password security
network security
SQL injection
log analysis
incident response
crittografia base

Ogni domanda deve avere:

- category
- text
- option_a
- option_b
- option_c
- option_d
- correct_option
- difficulty"""

import re
import os
import json
import hashlib
import secrets
import string
from datetime import datetime

def validate_input_int(messaggio, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(messaggio))
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                print(f"Per favore, inserisci un numero tra {min_val} e {max_val}.")
                continue
            return value
        except ValueError:
            print("Input non valido. Per favore, inserisci un numero intero.")

def validate_input_choice(messaggio, scelte_valide):
    scelte_valide = [scelta.upper() for scelta in scelte_valide]
    while True:
        value = input(messaggio).strip().upper()
        if value in scelte_valide:
            return value
        print(f"Input non valido. Per favore, scegli tra: {', '.join(scelte_valide)}.")

def print_title(titolo):
    print("\n" + "=" * 50)
    print(f"{titolo.center(50)}")
    print("=" * 50 + "\n")

def current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()    

def check_password(password, hash_salvato):
    return hash_password(password) == hash_salvato

def generate_salt(length=16):
    return os.urandom(length).hex()

def sanitize_input(text):
    """Pulisce l'input utente rimuovendo caratteri pericolosi"""
    # Rimuovi caratteri di controllo e potenzialmente pericolosi
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    # Limita lunghezza
    return text.strip()[:500]

def log_event(message, level="INFO"):
    """Logga un evento con timestamp"""
    timestamp = current_datetime()
    log_entry = f"[{timestamp}] {level}: {message}"
    print(log_entry)  # Per ora stampiamo, in futuro potremmo scrivere su file
    return log_entry

def print_menu(title, options):
    """Stampa un menu formattato"""
    print_title(title)
    for key, description in options.items():
        print(f"{key}) {description}")
    print()

def calculate_score(correct_answers, total_questions):
    """Calcola il punteggio percentuale"""
    if total_questions == 0:
        return 0.0
    return round((correct_answers / total_questions) * 100, 2)

def format_time(seconds):
    """Formatta secondi in minuti:secondi"""
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02d}"

def load_questions_from_json(filepath="data/questions.json"):
    """Carica domande da file JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        log_event(f"File {filepath} non trovato", "WARNING")
        return []
    except json.JSONDecodeError as e:
        log_event(f"Errore nel parsing JSON: {e}", "ERROR")
        return []

def save_questions_to_json(questions, filepath="data/questions.json"):
    """Salva domande su file JSON"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        log_event(f"Domande salvate in {filepath}")
        return True
    except Exception as e:
        log_event(f"Errore nel salvataggio: {e}", "ERROR")
        return False

def validate_email(email):
    """Valida un indirizzo email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_random_password(length=12):
    """Genera una password casuale sicura"""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

def hash_password_with_salt(password, salt=None):
    """Hash password con salt per maggiore sicurezza"""
    if salt is None:
        salt = generate_salt()
    salted_password = password + salt
    hash_obj = hashlib.sha256(salted_password.encode())
    return hash_obj.hexdigest(), salt

def check_password_with_salt(password, stored_hash, salt):
    """Verifica password con salt"""
    hash_check, _ = hash_password_with_salt(password, salt)
    return hash_check == stored_hash

