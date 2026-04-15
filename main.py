from auth import login

username, role = login()

if role == "admin":
    print("Welcome Admin")
elif role == "student":
    print("Welcome Student")
else:
    print("Invalid login")