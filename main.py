import sys
from auth import login, logout, current_user


def admin_menu():
    try:
        from admin import add_student, view_all_students, update_student, delete_student, search_student
    except ImportError:
        print("admin.py not ready yet.")
        return

    while True:
        print("\n── Admin Menu ─────────────────")
        print("1. Add student")
        print("2. View all students")
        print("3. Update student")
        print("4. Delete student")
        print("5. Search student")
        print("0. Logout")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            search_student()
        elif choice == "0":
            break
        else:
            print("Invalid option.")


def student_menu():
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
            view_profile()
        elif choice == "2":
            view_grades()
        elif choice == "3":
            view_eca()
        elif choice == "4":
            update_profile()
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
        student_menu()
    else:
        print(f"Unknown role: {user.role}")

    logout()


if __name__ == "__main__":
    main()