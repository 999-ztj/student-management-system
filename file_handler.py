def read_passwords():
    with open("passwords.txt", "r") as file:
        return file.readlines()


def read_users():
    with open("users.txt", "r") as file:
        return file.readlines()