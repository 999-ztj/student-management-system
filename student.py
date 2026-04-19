from file_handler import read_users, get_grades, get_eca, write_users


# ===============================
# Helper Functions
# ===============================

def get_user_data(user_id):
    for user in read_users():
        if user["id"] == user_id:
            return user
    return None


# ===============================
# Main Student Features
# ===============================

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
        subjects = ["math", "science", "english", "cs", "stats"]
        marks = []
        for s in subjects:
            print(f"{s.capitalize()}: {grades[s]}")
            try:
                marks.append(float(grades[s]))
            except ValueError:
                pass
        if marks:
            avg = sum(marks) / len(marks)
            print(f"Average: {avg:.2f}")
            print("Status:", "PASS" if avg >= 50 else "AT RISK")
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
    from file_handler import read_passwords, write_passwords
    users = read_users()

    for user in users:
        if user["id"] == user_id:
            print(f"\n  Current Name: {user['name']}")
            print(f"  Current Username: {user['username']}")
            print("\n  What would you like to update?")
            print("  1. Name")
            print("  2. Username")
            print("  3. Both")

            while True:
                try:
                    choice = int(input("  Enter choice (1-3): "))
                    if choice in [1, 2, 3]:
                        break
                    print("  Enter 1, 2, or 3.")
                except ValueError:
                    print("  Invalid input.")

            if choice in [1, 3]:
                new_name = input("  Enter new name: ").strip()
                if new_name:
                    user["name"] = new_name

            if choice in [2, 3]:
                new_username = input("  Enter new username: ").strip()
                if new_username:
                    # Update username in passwords.txt too
                    old_username = user["username"]
                    passwords = read_passwords()
                    for p in passwords:
                        if p["username"] == old_username:
                            p["username"] = new_username
                            break
                    write_passwords(passwords)
                    user["username"] = new_username

            break

    write_users(users)
    print("  Profile updated successfully!")


# ===============================
# Student Menu (unchanged)
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
