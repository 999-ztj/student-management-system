from file_handler import check_password, get_user_by_username


class User:
    def __init__(self, user_id, name, role, username):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.username = username

    def is_admin(self):
        return self.role == "admin"

    def is_student(self):
        return self.role == "student"

    def __str__(self):
        return f"{self.name} ({self.role})"

class Student(User):
    def get_grades(self):
        from file_handler import get_grades
        return get_grades(self.user_id)

class Admin(User):
    def greet(self):
        return f"Admin {self.name} logged in."



# holds whoever is logged in right now
current_user = None


def login():
    print("\n" + "=" * 40)
    print("   Student Management System")
    print("=" * 40)

    attempts = 0
    while attempts < 3:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if not username or not password:
            print("Username and password cannot be empty.\n")
            continue

        if check_password(username, password):
            user_data = get_user_by_username(username)

            if user_data is None:
                print("Account not found in user records. Contact admin.\n")
                return None

            global current_user
            current_user = User(
                user_id=user_data["id"],
                name=user_data["name"],
                role=user_data["role"],
                username=username
            )

            print(f"\nWelcome, {current_user.name}!")
            return current_user

        else:
            attempts += 1
            remaining = 3 - attempts
            if remaining > 0:
                print(f"Incorrect username or password. {remaining} attempt(s) left.\n")
            else:
                print("Too many failed attempts. Exiting.\n")

    return None


def logout():
    global current_user
    current_user = None
    print("Logged out successfully.")