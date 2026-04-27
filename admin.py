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
        print("Invalid difficulty level. Question not added.") #ciao
           

    

def edit_question():
    ...

def delete_question():
    ...

def list_questions_by_category():
    ...

def import_from_json():
    ...

def export_to_json():
    ...




