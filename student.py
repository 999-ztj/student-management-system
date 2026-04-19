from file_handler import read_users, get_grades, get_eca, write_users

# Helper Functions

def get_user_data(user_id):
    for user in read_users():
        if user["id"] == user_id:
            return user
    return None

# Main Student Features

def view_profile(user_id):
    user = get_user_data(user_id)
    if user:
        print("\n--- PROFILE ---")
        print("ID:", user["id"])
        print("Name:", user["name"])
        print("Role:", user["role"])
    else:
        print("User not found.")


def view_grades(user_id):
    grades = get_grades(user_id)
    if grades:
        print("\n--- GRADES ---")
        print("Math:", grades["math"])
        print("Science:", grades["science"])
        print("English:", grades["english"])
        print("CS:", grades["cs"])
        print("Stats:", grades["stats"])
    else:
        print("Grades not found.")


def view_eca(user_id):
    eca_list = get_eca(user_id)
    if eca_list:
        print("\n--- ECA ---")
        for activity in eca_list:
            print("Activity:", activity)
    else:
        print("No ECA found.")


def update_profile(user_id):
    users = read_users()

    for user in users:
        if user["id"] == user_id:
            new_name = input("Enter new name: ")
            user["name"] = new_name
            break

    write_users(users)
    print("Profile updated successfully!")


# Student Menu (unchanged)

def student_menu(user_id):
    while True:
        print("\n===== STUDENT MENU =====")
        print("1. View Profile")
        print("2. View Grades")
        print("3. View ECA")
        print("4. Update Profile")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            view_profile(user_id)
        elif choice == "2":
            view_grades(user_id)
        elif choice == "3":
            view_eca(user_id)
        elif choice == "4":
            update_profile(user_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")
