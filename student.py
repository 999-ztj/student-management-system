from file_handler import read_users, get_grades, get_eca, write_users


# ===============================
# Helper Functions
# ===============================

def get_user_data(user_id):
    users = read_file("users.txt")
    for user in users:
        if user[0] == user_id:
            return user
    return None


def get_grades(user_id):
    grades = read_file("grades.txt")
    for g in grades:
        if g[0] == user_id:
            return g
    return None


def get_eca(user_id):
    eca = read_file("eca.txt")
    for e in eca:
        if e[0] == user_id:
            return e
    return None


# ===============================
# Main Student Features
# ===============================

def view_profile(user_id):
    user = get_user_data(user_id)
    if user:
        print("\n--- PROFILE ---")
        print("ID:", user[0])
        print("Name:", user[1])
        print("Role:", user[2])
    else:
        print("User not found.")


def view_grades(user_id):
    grades = get_grades(user_id)
    if grades:
        print("\n--- GRADES ---")
        print("Math:", grades[1])
        print("Science:", grades[2])
        print("English:", grades[3])
        print("CS:", grades[4])
        print("Stats:", grades[5])
    else:
        print("Grades not found.")


def view_eca(user_id):
    eca = get_eca(user_id)
    if eca:
        print("\n--- ECA ---")
        print("Activity:", eca[1])
    else:
        print("No ECA found.")


def update_profile(user_id):
    users = read_file("users.txt")

    for user in users:
        if user[0] == user_id:
            new_name = input("Enter new name: ")
            user[1] = new_name
            break

    write_file("users.txt", users)
    print("Profile updated successfully!")


# ===============================
# Student Menu
# ===============================

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
