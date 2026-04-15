from file_handler import read_passwords, read_users

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    passwords = read_passwords()

    for line in passwords:
        u, p = line.strip().split(",")

        if u == username and p == password:
            users = read_users()

            for user_line in users:
                u_name, name, role = user_line.strip().split(",")

                if u_name == username:
                    return username, role

    return None, None