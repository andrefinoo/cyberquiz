import sqlite3

import db
import utils
import quiz_engine
import reports
import admin


def registrati():
    """
    Registra un nuovo utente nel database.
    """
    print("\n=== REGISTRAZIONE ===")

    username = input("Scegli username: ").strip()
    password = input("Scegli password: ").strip()

    if username == "" or password == "":
        print("Username e password non possono essere vuoti.")
        return

    password_hash = utils.hash_password(password)

    try:
        db.insert_user(username, password_hash)
        print("Registrazione completata.")
    except sqlite3.IntegrityError:
        print("Username già esistente.")


def login():
    """
    Effettua il login dell'utente.
    Se il login va bene, restituisce l'id dell'utente.
    Se il login fallisce, restituisce None.
    """
    print("\n=== LOGIN ===")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = db.find_user_by_username(username)

    if user is None:
        print("Utente non trovato.")
        return None

    user_id = user["id"]
    username_db = user["username"]
    password_hash = user["password_hash"]

    if utils.check_password(password, password_hash):
        print(f"Login effettuato. Benvenuto {username_db}!")
        return user_id
    else:
        print("Password errata.")
        return None


def main():
    """
    Menu principale del programma.
    """
    db.create_tables()

    logged_user_id = None

    print("Database pronto. Benvenuto in CyberQuiz!")

    while True:
        print("\n=== CYBERQUIZ LAB ===")
        print("1) Login")
        print("2) Registrati")
        print("3) Avvia Quiz")
        print("4) Report personali")
        print("5) Report globali")
        print("6) Admin")
        print("0) Esci")

        scelta = input("Scegli un'opzione: ").strip()

        match scelta:
            case "1":
                logged_user_id = login()

            case "2":
                registrati()

            case "3":
                if logged_user_id is None:
                    print("Devi fare login prima di avviare un quiz.")
                else:
                    quiz_engine.run_quiz(logged_user_id)

            case "4":
                if logged_user_id is None:
                    print("Devi fare login per vedere i report personali.")
                else:
                    reports.andamento_utente(logged_user_id)

            case "5":
                reports.report_globali()

            case "6":
                admin.admin_menu()

            case "0":
                print("Uscita dal programma.")
                break

            case _:
                print("Scelta non valida. Riprova.")


if __name__ == "__main__":
    main()