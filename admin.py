import db
import json
import os

def admin_menu():

    while True:
        print("\nAdmin Menu: ")
        print("1: Add_question")
        print("2: Edit question")
        print("3: Delete question")
        print("4: List questions by category")
        print("5: Import from JSON")
        print("6: Export to JSON")
    
        choise = input("Choose an option: ")

        match choise:
            case "0":
                print("Exiting admin menu.")
                break
            case "1":
                add_question()
            case "2":
                edit_question()
            case "3":
                delete_question()
            case "4":
                list_questions_by_category()
            case "5":
                import_from_json()
            case "6":
                export_to_json()
            case _:
                print("Invalid choice. Please try again.")


def add_question():
    question_category = input("Enter question category: ")
    question_text = input("Enter question text: ")
    options = ["A", "B", "C", "D"]
    options_text = []
    for option in options:
        option_text = input(f"Enter option {option}: ")
        options_text.append(option_text)
    correct_option = input("Enter correct option (A, B, C, D): ")
    if correct_option not in options:
        print("Invalid correct option. Question not added.")
        return
    try:
        question_difficulty = int(input("Enter question difficulty (1-5): "))
    except ValueError:
        print("Invalid input for difficulty. Question not added.")
        return
    if 1 <= question_difficulty <= 5:
        db.add_question(question_category, question_text, options_text, correct_option, question_difficulty) 
        print("Question added successfully.")
    else:
        print("Invalid difficulty level. Question not added.") 
           

def edit_question():
    # Chiediamo l'ID della domanda da modificare
    try:
        question_id = int(input("Enter question ID to edit: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    # Cerchiamo la domanda nel database tramite db.py
    question = db.get_question_by_id(question_id)

    # Se non esiste, usciamo
    if not question:
        print("Question not found.")
        return

    # Mostriamo i dati attuali all'utente
    print(f"\nCurrent data:")
    print(f"Category: {question['category']}")
    print(f"Text: {question['text']}")
    print(f"Option A: {question['option_a']}")
    print(f"Option B: {question['option_b']}")
    print(f"Option C: {question['option_c']}")
    print(f"Option D: {question['option_d']}")
    print(f"Correct option: {question['correct_option']}")
    print(f"Difficulty: {question['difficulty']}")
    print("(Press ENTER to keep current value)\n")

    # Per ogni campo, se l'utente preme invio manteniamo il valore vecchio
    category = input(f"New category [{question['category']}]: ")
    category = category if category != "" else question['category']

    text = input(f"New text [{question['text']}]: ")
    text = text if text != "" else question['text']

    option_a = input(f"New option A [{question['option_a']}]: ")
    option_a = option_a if option_a != "" else question['option_a']

    option_b = input(f"New option B [{question['option_b']}]: ")
    option_b = option_b if option_b != "" else question['option_b']

    option_c = input(f"New option C [{question['option_c']}]: ")
    option_c = option_c if option_c != "" else question['option_c']

    option_d = input(f"New option D [{question['option_d']}]: ")
    option_d = option_d if option_d != "" else question['option_d']

    # Validiamo la correct_option
    correct_option = input(f"New correct option [{question['correct_option']}]: ").upper()
    if correct_option == "":
        correct_option = question['correct_option']
    elif correct_option not in ["A", "B", "C", "D"]:
        print("Invalid correct option. Edit cancelled.")
        return

    # Validiamo la difficoltà
    difficulty_input = input(f"New difficulty [{question['difficulty']}]: ")
    if difficulty_input == "":
        difficulty = question['difficulty']
    else:
        try:
            difficulty = int(difficulty_input)
            if not 1 <= difficulty <= 5:
                print("Invalid difficulty. Edit cancelled.")
                return
        except ValueError:
            print("Invalid input for difficulty. Edit cancelled.")
            return

    # Salviamo le modifiche nel database
    db.edit_question(question_id, category, text, option_a, 
                     option_b, option_c, option_d, 
                     correct_option, difficulty)
    print("Question updated successfully.")

def delete_question():
    # Chiediamo l'ID della domanda da eliminare
    try:
        question_id = int(input("Enter question ID to delete: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    # Verifichiamo che la domanda esista
    question = db.get_question_by_id(question_id)
    if not question:
        print("Question not found.")
        return

    # Chiediamo conferma prima di eliminare
    confirm = input(f"Are you sure you want to delete question {question_id}? (y/n): ")
    if confirm.lower() != "y":
        print("Deletion cancelled.")
        return

    # Eliminiamo la domanda dal database
    db.delete_question(question_id)
    print("Question deleted successfully.")

def list_questions_by_category():
    # Chiediamo la categoria da visualizzare
    category = input("Enter category to list (or ENTER for all): ")

    # Recuperiamo le domande dal database
    if category == "":
        questions = db.get_all_questions()
    else:
        questions = db.get_questions_by_category(category)

    # Se non ci sono domande, lo diciamo
    if not questions:
        print("No questions found.")
        return

    # Stampiamo le domande in formato tabella
    print(f"\n{'ID':<5} {'Category':<20} {'Difficulty':<12} {'Text'}")
    print("-" * 70)
    for q in questions:
        print(f"{q['id']:<5} {q['category']:<20} {q['difficulty']:<12} {q['text'][:40]}")

def import_from_json():
    # Chiediamo il percorso del file JSON
    filepath = input("Enter JSON file path: ")

    # Verifichiamo che il file esista
    if not os.path.exists(filepath):
        print("File not found.")
        return

    # Leggiamo il file JSON
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            questions = json.load(f)
    except json.JSONDecodeError:
        print("Invalid JSON file.")
        return

    # Importiamo ogni domanda nel database
    imported = 0
    for q in questions:
        try:
            db.add_question(
                q["category"],
                q["text"],
                [q["option_a"], q["option_b"], q["option_c"], q["option_d"]],
                q["correct_option"],
                q["difficulty"]
            )
            imported += 1
        except KeyError as e:
            print(f"Skipping question: missing field {e}")

    print(f"Import complete. {imported}/{len(questions)} questions imported.")

def export_to_json():
    # Recuperiamo tutte le domande dal database
    questions = db.get_all_questions()

    if not questions:
        print("No questions to export.")
        return

    # Chiediamo il percorso dove salvare il file
    filepath = input("Enter output file path (e.g. data/export.json): ")

    # Convertiamo i dati in formato JSON e salviamo
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=4, ensure_ascii=False)
        print(f"Export complete. {len(questions)} questions saved to {filepath}.")
    except OSError:
        print("Error writing file. Check the path and permissions.")




