USERS_FILE = "users.txt"
PASSWORDS_FILE = "passwords.txt"
GRADES_FILE = "grades.txt"
ECA_FILE = "eca.txt"


# ── Users ──────────────────────────────────────────────────────────────────

def read_users():
    users = []
    try:
        with open(USERS_FILE, "r") as f:
            lines = f.readlines()
        for line in lines[1:]:
            parts = line.strip().split(",")
            if len(parts) == 4:
                users.append({
                    "id": parts[0],
                    "name": parts[1],
                    "role": parts[2],
                    "username": parts[3]
                })
    except FileNotFoundError:
        print("Error: users.txt not found.")
    return users


def write_users(users):
    try:
        with open(USERS_FILE, "w") as f:
            f.write("id,name,role,username\n")
            for u in users:
                f.write(f"{u['id']},{u['name']},{u['role']},{u['username']}\n")
    except Exception as e:
        print(f"Error writing users: {e}")


def get_user_by_username(username):
    for user in read_users():
        if user["username"] == username:
            return user
    return None


def get_user_by_id(user_id):
    for user in read_users():
        if user["id"] == user_id:
            return user
    return None


def add_user(user_id, name, role, username):
    users = read_users()
    if any(u["id"] == user_id for u in users):
        return False
    users.append({"id": user_id, "name": name, "role": role, "username": username})
    write_users(users)
    return True


# ── Passwords ──────────────────────────────────────────────────────────────

def read_passwords():
    passwords = []
    try:
        with open(PASSWORDS_FILE, "r") as f:
            lines = f.readlines()
        for line in lines[1:]:
            parts = line.strip().split(",")
            if len(parts) == 2:
                passwords.append({"username": parts[0], "password": parts[1]})
    except FileNotFoundError:
        print("Error: passwords.txt not found.")
    return passwords


def write_passwords(passwords):
    try:
        with open(PASSWORDS_FILE, "w") as f:
            f.write("username,password\n")
            for p in passwords:
                f.write(f"{p['username']},{p['password']}\n")
    except Exception as e:
        print(f"Error writing passwords: {e}")


def check_password(username, password):
    for entry in read_passwords():
        if entry["username"] == username and entry["password"] == password:
            return True
    return False


def add_password(username, password):
    passwords = read_passwords()
    passwords.append({"username": username, "password": password})
    write_passwords(passwords)


# ── Grades ─────────────────────────────────────────────────────────────────

def read_grades():
    grades = []
    try:
        with open(GRADES_FILE, "r") as f:
            lines = f.readlines()
        for line in lines[1:]:
            parts = line.strip().split(",")
            if len(parts) == 6:
                grades.append({
                    "id": parts[0], "math": parts[1], "science": parts[2],
                    "english": parts[3], "cs": parts[4], "stats": parts[5]
                })
    except FileNotFoundError:
        print("Error: grades.txt not found.")
    return grades


def get_grades(student_id):
    for g in read_grades():
        if g["id"] == student_id:
            return g
    return None


def write_grades(grades):
    try:
        with open(GRADES_FILE, "w") as f:
            f.write("id,math,science,english,cs,stats\n")
            for g in grades:
                f.write(f"{g['id']},{g['math']},{g['science']},{g['english']},{g['cs']},{g['stats']}\n")
    except Exception as e:
        print(f"Error writing grades: {e}")


# ── ECA ────────────────────────────────────────────────────────────────────

def read_eca():
    eca = []
    try:
        with open(ECA_FILE, "r") as f:
            lines = f.readlines()
        for line in lines[1:]:
            parts = line.strip().split(",")
            if len(parts) == 2:
                eca.append({"id": parts[0], "activity": parts[1]})
    except FileNotFoundError:
        print("Error: eca.txt not found.")
    return eca


def get_eca(student_id):
    return [e["activity"] for e in read_eca() if e["id"] == student_id]


def write_eca(eca):
    try:
        with open(ECA_FILE, "w") as f:
            f.write("id,activity\n")
            for e in eca:
                f.write(f"{e['id']},{e['activity']}\n")
    except Exception as e:
        print(f"Error writing ECA: {e}")
