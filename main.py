import sys
from auth import login, logout, current_user


def admin_menu():
    try:
        from admin import admin_control
    except ImportError:
        print("admin.py not ready yet.")
        return
    admin_control()


def student_menu(user_id):
    try:
        from student import view_profile, view_grades, view_eca, update_profile
    except ImportError:
        print("student.py not ready yet.")
        return

    while True:
        print("\n── Student Menu ───────────────")
        print("1. View profile")
        print("2. View grades")
        print("3. View ECA activities")
        print("4. Update profile")
        print("0. Logout")

        choice = input("Choose: ").strip()

        if choice == "1":
            view_profile(user_id)
        elif choice == "2":
            view_grades(user_id)
        elif choice == "3":
            view_eca(user_id)
        elif choice == "4":
            update_profile(user_id)
        elif choice == "0":
            break
        else:
            print("Invalid option.")


def main():
    user = login()

    if user is None:
        print("Exiting.")
        sys.exit()

    if user.is_admin():
        admin_menu()
    elif user.is_student():
        student_menu(user.user_id)
    else:
        print(f"Unknown role: {user.role}")

    logout()


if __name__ == "__main__":
    main()
