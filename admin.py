import pandas as pd
import os
from file_handler import add_password, read_passwords, write_passwords, read_grades, write_grades, read_eca, write_eca, get_eca

def admin_control():
    # Welcome

    def PrintLogo():
        print("""
      ░██████╗████████╗██╗░░░██╗██████╗░███████╗███╗░░██╗████████╗
      ██╔════╝╚══██╔══╝██║░░░██║██╔══██╗██╔════╝████╗░██║╚══██╔══╝
      ╚█████╗░░░░██║░░░██║░░░██║██║░░██║█████╗░░██╔██╗██║░░░██║░░░
      ░╚═══██╗░░░██║░░░██║░░░██║██║░░██║██╔══╝░░██║╚████║░░░██║░░░
      ██████╔╝░░░██║░░░╚██████╔╝██████╔╝███████╗██║░╚███║░░░██║░░░
      ╚═════╝░░░░╚═╝░░░░╚═════╝░╚═════╝░╚══════╝╚═╝░░╚══╝░░░╚═╝░░░
        """)

    W = 75

    def Rule(Char="═", Width=W):
        return Char * Width

    def Box_Top(Width=W):
        return "╔" + "═" * (Width - 2) + "╗"

    def Box_Mid(Width=W):
        return "╠" + "═" * (Width - 2) + "╣"

    def Box_Bot(Width=W):
        return "╚" + "═" * (Width - 2) + "╝"

    def Box_Row(Text, Width=W):
        Inner = Width - 4
        return "║  " + Text.ljust(Inner) + "  ║"

    def Section_Header(Title, Width=W):
        Inner = Width - 4
        Line = Title.center(Inner)
        print("╔" + "═" * (Width - 2) + "╗")
        print("║  " + Line + "  ║")
        print("╚" + "═" * (Width - 2) + "╝")

    def Divider(Width=W):
        print("─" * Width)

    print()
    print(Rule())
    PrintLogo()
    print("  S T U D E N T   M A N A G E M E N T   S Y S T E M".center(W))
    print(Rule())

    # CLASS
    class Learner:
        def __init__(self, V_ID, V_Name, V_Role, V_Username):
            self.__ID = V_ID
            self.__Name = V_Name
            self.__Role = V_Role
            self.__Username = V_Username

        def DisplayDetails(self):
            Divider()
            print(f"  {'ID':<18}  {self.__ID}")
            print(f"  {'Name':<18}  {self.__Name}")
            print(f"  {'Role':<18}  {self.__Role}")
            print(f"  {'Username':<18}  {self.__Username}")
            Divider()


    # MAIN

    Stop = False

    # LOAD OR CREATE DATAFRAME
    if os.path.exists("users.txt"):
        DF = pd.read_csv("users.txt", sep=",")
    else:
        DF = pd.DataFrame(columns=['id', 'name', 'role', 'username'])

    while Stop == False:
        print()
        print(Box_Top())
        print(Box_Row(""))
        print(Box_Row("A D M I N   P A N E L".center(W - 4)))
        print(Box_Row(""))
        print(Box_Mid())
        print(Box_Row("  1.  Add User                       6.  Manage Grades"))
        print(Box_Row("  2.  Display All Users               7.  Manage ECA"))
        print(Box_Row("  3.  Search User                     8.  Analytics Dashboard"))
        print(Box_Row("  4.  Update User                     9.  Exit"))
        print(Box_Row("  5.  Delete User"))
        print(Box_Row(""))
        print(Box_Bot())

        while True:
            try:
                Choice = int(input("\n  Enter your choice (1-9)  >>  "))
                if 1 <= Choice <= 9:
                    break
                else:
                    print("  Please enter a number between 1 and 9.")
            except ValueError:
                print("  Invalid input. Please enter a number.")

        if Choice == 1:  # ADD
            print()
            Section_Header("ADD NEW USER")

            V_ID = input("  Enter ID:  ")
            while V_ID in DF['id'].astype(str).values:
                print("  Error: ID already exists.")
                V_ID = input("  Enter a unique ID:  ")

            V_Name = input("  Enter Name:  ")
            V_Username = input("  Enter Username:  ")
            V_Password = input("  Enter Password:  ")

            print()
            print("  1.  Student")
            print("  2.  Admin")

            while True:
                try:
                    RoleChoice = int(input("  Enter Role (1 or 2)  >>  "))
                    if RoleChoice == 1:
                        V_Role = "student"
                        break
                    elif RoleChoice == 2:
                        V_Role = "admin"
                        break
                    else:
                        print("  Please enter 1 or 2.")
                except ValueError:
                    print("  Invalid input.")

            NewUser = Learner(V_ID, V_Name, V_Role, V_Username)

            New_Row = pd.DataFrame([{
                'id': V_ID,
                'name': V_Name,
                'role': V_Role,
                'username': V_Username
            }])

            DF = pd.concat([DF, New_Row], ignore_index=True)
            DF.to_csv("users.txt", sep=",", index=False)
            add_password(V_Username, V_Password)

            print("\n  User added successfully.")
            NewUser.DisplayDetails()

        elif Choice == 2:  # DISPLAY
            print()
            Section_Header("ALL USERS")
            if DF.empty:
                print("\n  No records found.")
            else:
                print()
                print(DF[['id', 'name', 'role', 'username']].to_string(index=False))
            print()
            print(Rule())

        elif Choice == 3:  # SEARCH
            print()
            Section_Header("SEARCH USER")
            Search_ID = input("  Enter ID to Search  >>  ")

            Result = DF[DF['id'].astype(str) == Search_ID]

            if Result.empty:
                print(f"\n  No user found with ID: {Search_ID}")
            else:
                print("\n  User found.")
                for Index, row in Result.iterrows():
                    Temp = Learner(row['id'], row['name'], row['role'], row['username'])
                    Temp.DisplayDetails()

        elif Choice == 4:  # UPDATE
            print()
            Section_Header("UPDATE USER")
            Update_ID = input("  Enter ID to Update  >>  ")

            Result = DF[DF['id'].astype(str) == Update_ID]

            if Result.empty:
                print(f"\n  No user found with ID: {Update_ID}")
            else:
                Current = Result.iloc[0]

                print("\n  Choose field to update:\n")
                print(Box_Top())
                print(Box_Row(""))
                print(Box_Row("  U P D A T E   F I E L D S".center(W - 4)))
                print(Box_Row(""))
                print(Box_Mid())
                print(Box_Row(f"  1.  Name       [ {Current['name']} ]"))
                print(Box_Row(f"  2.  Role       [ {Current['role']} ]"))
                print(Box_Row(f"  3.  Username   [ {Current['username']} ]"))
                print(Box_Row(f"  4.  Update All Fields"))
                print(Box_Row(""))
                print(Box_Bot())

                while True:
                    try:
                        Field = int(input("\n  Enter choice (1-4) >> "))
                        if 1 <= Field <= 4:
                            break
                        else:
                            print("  Enter 1-4 only.")
                    except:
                        print("  Invalid input.")

                Divider()

                New_Name = Current['name']
                New_Role = Current['role']
                New_Username = Current['username']

                if Field == 1 or Field == 4:
                    val = input(f"  Name [{Current['name']}]: ")
                    if val:
                        New_Name = val

                if Field == 2 or Field == 4:
                    print("\n  1. Student\n  2. Admin")
                    while True:
                        try:
                            r = int(input("  Choose role: "))
                            if r == 1:
                                New_Role = "student"
                                break
                            elif r == 2:
                                New_Role = "admin"
                                break
                            else:
                                print("  Enter 1 or 2.")
                        except:
                            print("  Invalid input.")

                if Field == 3 or Field == 4:
                    val = input(f"  Username [{Current['username']}]: ")
                    if val:
                        New_Username = val

                DF.loc[DF['id'].astype(str) == Update_ID,
                       ['name', 'role', 'username']] = [New_Name, New_Role, New_Username]

                DF.to_csv("users.txt", sep=",", index=False)
                print("\n  User updated successfully.")

        elif Choice == 5:  # DELETE
            print()
            Section_Header("DELETE USER")
            Delete_ID = input("  Enter ID to Delete >> ")

            if Delete_ID not in DF['id'].astype(str).values:
                print(f"\n  No user found with ID: {Delete_ID}")
            else:
                Confirm = input("  Confirm delete (Y/N): ")

                if Confirm.lower() == "y":
                    DF = DF[DF['id'].astype(str) != Delete_ID]
                    DF.to_csv("users.txt", sep=",", index=False)
                    print("\n  User deleted.")
                else:
                    print("\n  Cancelled.")

        elif Choice == 6:  # MANAGE GRADES
            print()
            Section_Header("MANAGE GRADES")
            grades = read_grades()
            if not grades:
                print("\n  No grade records found.")
            else:
                print(f"\n  {'ID':<10} {'Math':>6} {'Science':>8} {'English':>8} {'CS':>6} {'Stats':>6}")
                Divider()
                for g in grades:
                    print(f"  {g['id']:<10} {g['math']:>6} {g['science']:>8} {g['english']:>8} {g['cs']:>6} {g['stats']:>6}")

            print("\n  Options:")
            print("  1. Add grades for a student")
            print("  2. Update grades for a student")
            while True:
                try:
                    GradeChoice = int(input("  Enter choice (1-2) >> "))
                    if GradeChoice in [1, 2]:
                        break
                    print("  Enter 1 or 2.")
                except ValueError:
                    print("  Invalid input.")

            G_ID = input("  Enter Student ID: ").strip()

            try:
                math_v    = float(input("  Math mark: "))
                science_v = float(input("  Science mark: "))
                english_v = float(input("  English mark: "))
                cs_v      = float(input("  CS mark: "))
                stats_v   = float(input("  Stats mark: "))
            except ValueError:
                print("  Invalid mark entered. Must be a number.")
            else:
                existing = [g for g in grades if g["id"] != G_ID]
                existing.append({"id": G_ID, "math": math_v, "science": science_v,
                                  "english": english_v, "cs": cs_v, "stats": stats_v})
                write_grades(existing)
                print("  Grades saved successfully.")

        elif Choice == 7:  # MANAGE ECA
            print()
            Section_Header("MANAGE ECA")
            eca_records = read_eca()
            if not eca_records:
                print("\n  No ECA records found.")
            else:
                print(f"\n  {'ID':<10} {'Activity'}")
                Divider()
                for e in eca_records:
                    print(f"  {e['id']:<10} {e['activity']}")

            print("\n  Options:")
            print("  1. Add ECA activity for a student")
            print("  2. Delete all ECA for a student")
            while True:
                try:
                    ECAChoice = int(input("  Enter choice (1-2) >> "))
                    if ECAChoice in [1, 2]:
                        break
                    print("  Enter 1 or 2.")
                except ValueError:
                    print("  Invalid input.")

            E_ID = input("  Enter Student ID: ").strip()

            if ECAChoice == 1:
                activity = input("  Enter activity name: ").strip()
                eca_records.append({"id": E_ID, "activity": activity})
                write_eca(eca_records)
                print("  ECA activity added.")
            elif ECAChoice == 2:
                updated = [e for e in eca_records if e["id"] != E_ID]
                write_eca(updated)
                print("  ECA records for student deleted.")

        elif Choice == 8:  # ANALYTICS
            try:
                from analytics import analytics_menu
                analytics_menu()
            except ImportError:
                print("  analytics.py not available.")

        elif Choice == 9:
            Stop = True

        if not Stop:
            Repeat = input("\n  Return to menu? (Y/N): ")
            if Repeat.lower() == "n":
                Stop = True

    print()
    print(Rule())
    print("  Thank you for using the system.".center(W))
    print(Rule())
