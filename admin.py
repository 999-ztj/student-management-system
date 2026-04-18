import pandas as pd
import os

# ====================== WELCOME LOGO ======================

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
    def __init__(self, V_Roll_No, V_Student_ID, V_Full_Name, V_Address, V_Year, V_Program, V_Group, V_Phone, V_DOB):
        self.__Roll       = V_Roll_No
        self.__Student_ID = V_Student_ID
        self.__Name       = V_Full_Name
        self.__Address    = V_Address
        self.__Year       = V_Year
        self.__Program    = V_Program
        self.__Group      = V_Group
        self.__Phone      = V_Phone
        self.__DOB        = V_DOB

    def DisplayDetails(self):
        Divider()
        print(f"  {'Roll No':<18}  {self.__Roll}")
        print(f"  {'Student ID':<18}  {self.__Student_ID}")
        print(f"  {'Name':<18}  {self.__Name}")
        print(f"  {'Address':<18}  {self.__Address}")
        print(f"  {'Year':<18}  {self.__Year}")
        print(f"  {'Program':<18}  {self.__Program}")
        print(f"  {'Group':<18}  {self.__Group}")
        print(f"  {'Phone':<18}  {self.__Phone}")
        print(f"  {'Date of Birth':<18}  {self.__DOB}")
        Divider()


# MAIN

Stop = False

# LOAD OR CREATE DATAFRAME
if os.path.exists("students.csv"):
    DF = pd.read_csv("students.csv")
    # Add Student_ID column if it doesn't exist (for backward compatibility)
    if 'Student_ID' not in DF.columns:
        DF.insert(1, 'Student_ID', '')
        DF.to_csv("students.csv", index=False)
else:
    DF = pd.DataFrame(columns=['Roll_No', 'Student_ID', 'Name', 'Address', 'Year', 'Program', 'Group', 'Phone', 'DOB'])

while Stop == False:
    print()
    print(Box_Top())
    print(Box_Row(""))
    print(Box_Row("A D M I N   P A N E L".center(W - 4)))
    print(Box_Row(""))
    print(Box_Mid())
    print(Box_Row("  1.  Add Record                     4.  Update Records"))
    print(Box_Row("  2.  Display All Records             5.  Delete Records"))
    print(Box_Row("  3.  Search Records                  6.  Exit"))
    print(Box_Row(""))
    print(Box_Bot())

    # SAFE INPUT FOR CHOICE
    while True:
        try:
            Choice = int(input("\n  Enter your choice (1-6)  >>  "))
            if 1 <= Choice <= 6:
                break
            else:
                print("  Please enter a number between 1 and 6.")
        except ValueError:
            print("  Invalid input. Please enter a number.")

    if Choice == 1:  # ADD STUDENT
        print()
        Section_Header("ADD NEW STUDENT")

        print("  1.  Auto Generate Roll Number  (Recommended)")
        print("  2.  Enter Roll Number Manually")
        RollChoice = input("  Enter 1 or 2  >>  ")

        while RollChoice != "1" and RollChoice != "2":
            print("  Invalid input. Enter only 1 or 2.")
            RollChoice = input("  Enter 1 or 2  >>  ")

        if RollChoice == "1":
            if DF.empty:
                V_Roll_No = "STU001"
            else:
                Last_Roll = DF['Roll_No'].str.replace("STU", "").astype(int).max()
                V_Roll_No = f"STU{Last_Roll + 1:03d}"
            print(f"  Generated Roll Number:  {V_Roll_No}")
        else:
            V_Roll_No = input("  Enter Roll Number:  ")
            while V_Roll_No in DF['Roll_No'].astype(str).values:
                print("  Error: Roll Number already exists.")
                V_Roll_No = input("  Enter a unique Roll Number:  ")

        V_Student_ID = input("  Enter Student ID:  ")
        while V_Student_ID in DF['Student_ID'].astype(str).values:
            print("  Error: Student ID already exists.")
            V_Student_ID = input("  Enter a unique Student ID:  ")

        V_Full_Name = input("  Enter Full Name:  ")
        V_Address   = input("  Enter Address:  ")
        V_Year      = input("  Enter Year:  ")
        V_Program   = input("  Enter Program:  ")
        V_Group     = input("  Enter Group:  ")
        V_Phone     = input("  Enter Phone Number:  ")
        V_DOB       = input("  Enter Date of Birth (YYYY-MM-DD):  ")

        NewStudent = Learner(V_Roll_No, V_Student_ID, V_Full_Name, V_Address, V_Year, V_Program, V_Group, V_Phone, V_DOB)

        New_Row = pd.DataFrame([{
            'Roll_No':     V_Roll_No,
            'Student_ID':  V_Student_ID,
            'Name':        V_Full_Name,
            'Address':     V_Address,
            'Year':        V_Year,
            'Program':     V_Program,
            'Group':       V_Group,
            'Phone':       V_Phone,
            'DOB':         V_DOB
        }])

        DF = pd.concat([DF, New_Row], ignore_index=True)
        DF.to_csv("students.csv", index=False)

        print("\n  Student added successfully.")
        NewStudent.DisplayDetails()

    elif Choice == 2:  # DISPLAY ALL
        print()
        Section_Header("ALL STUDENTS")
        if DF.empty:
            print("\n  No student records found.")
        else:
            print()
            print(DF.to_string(index=False))
        print()
        print(Rule())

    elif Choice == 3:  # SEARCH
        print()
        Section_Header("SEARCH STUDENT")
        Search_Roll = input("  Enter Roll Number to Search  >>  ")

        Result = DF[DF['Roll_No'].astype(str) == Search_Roll]

        if Result.empty:
            print(f"\n  No student found with Roll No: {Search_Roll}")
        else:
            print("\n  Student record found.")
            for Index, row in Result.iterrows():
                Temp_Student = Learner(row['Roll_No'], row['Student_ID'], row['Name'], row['Address'],
                                       row['Year'], row['Program'], row['Group'],
                                       row['Phone'], row['DOB'])
                Temp_Student.DisplayDetails()

    elif Choice == 4:  # UPDATE
        print()
        Section_Header("UPDATE STUDENT")
        Update_Roll = input("  Enter Roll Number to Update  >>  ")

        Result = DF[DF['Roll_No'].astype(str) == Update_Roll]
        if Result.empty:
            print(f"\n  No student found with Roll No: {Update_Roll}")
        else:
            Current = Result.iloc[0]

            print("\n  Student found. Choose which field to update:\n")
            print(Box_Top())
            print(Box_Row(""))
            print(Box_Row("  U P D A T E   F I E L D S".center(W - 4)))
            print(Box_Row(""))
            print(Box_Mid())
            print(Box_Row(f"  1.  Student ID     [ {Current['Student_ID']} ]"))
            print(Box_Row(f"  2.  Full Name      [ {Current['Name']} ]"))
            print(Box_Row(f"  3.  Address        [ {Current['Address']} ]"))
            print(Box_Row(f"  4.  Year           [ {Current['Year']} ]"))
            print(Box_Row(f"  5.  Program        [ {Current['Program']} ]"))
            print(Box_Row(f"  6.  Group          [ {Current['Group']} ]"))
            print(Box_Row(f"  7.  Phone          [ {Current['Phone']} ]"))
            print(Box_Row(f"  8.  Date of Birth  [ {Current['DOB']} ]"))
            print(Box_Row(f"  9.  Update All Fields"))
            print(Box_Row(""))
            print(Box_Bot())

            while True:
                try:
                    Field_Choice = int(input("\n  Enter your choice (1-9)  >>  "))
                    if 1 <= Field_Choice <= 9:
                        break
                    else:
                        print("  Please enter a number between 1 and 9.")
                except ValueError:
                    print("  Invalid input. Please enter a number.")

            Divider()

            New_Student_ID = Current['Student_ID']
            New_Name       = Current['Name']
            New_Address    = Current['Address']
            New_Year       = Current['Year']
            New_Program    = Current['Program']
            New_Group      = Current['Group']
            New_Phone      = Current['Phone']
            New_DOB        = Current['DOB']

            if Field_Choice == 1 or Field_Choice == 9:
                Entered_ID = input(f"  Student ID     [{Current['Student_ID']}]:  ")
                if Entered_ID and Entered_ID != Current['Student_ID']:
                    while Entered_ID in DF['Student_ID'].astype(str).values:
                        print("  Error: Student ID already exists.")
                        Entered_ID = input(f"  Student ID     [{Current['Student_ID']}]:  ")
                    New_Student_ID = Entered_ID
                elif Entered_ID:
                    New_Student_ID = Entered_ID

            if Field_Choice == 2 or Field_Choice == 9:
                Entered_Name = input(f"  Full Name      [{Current['Name']}]:  ")
                if Entered_Name:
                    New_Name = Entered_Name

            if Field_Choice == 3 or Field_Choice == 9:
                Entered_Address = input(f"  Address        [{Current['Address']}]:  ")
                if Entered_Address:
                    New_Address = Entered_Address

            if Field_Choice == 4 or Field_Choice == 9:
                Entered_Year = input(f"  Year           [{Current['Year']}]:  ")
                if Entered_Year:
                    New_Year = Entered_Year

            if Field_Choice == 5 or Field_Choice == 9:
                Entered_Program = input(f"  Program        [{Current['Program']}]:  ")
                if Entered_Program:
                    New_Program = Entered_Program

            if Field_Choice == 6 or Field_Choice == 9:
                Entered_Group = input(f"  Group          [{Current['Group']}]:  ")
                if Entered_Group:
                    New_Group = Entered_Group

            if Field_Choice == 7 or Field_Choice == 9:
                Entered_Phone = input(f"  Phone          [{Current['Phone']}]:  ")
                if Entered_Phone:
                    New_Phone = Entered_Phone

            if Field_Choice == 8 or Field_Choice == 9:
                Entered_DOB = input(f"  Date of Birth  [{Current['DOB']}]:  ")
                if Entered_DOB:
                    New_DOB = Entered_DOB

            DF.loc[DF['Roll_No'].astype(str) == Update_Roll,
            ['Student_ID', 'Name', 'Address', 'Year', 'Program', 'Group', 'Phone', 'DOB']] = \
                [New_Student_ID, New_Name, New_Address, New_Year, New_Program, New_Group, New_Phone, New_DOB]

            DF.to_csv("students.csv", index=False)
            print("\n  Student details updated successfully.")

    elif Choice == 5:  # DELETE
        print()
        Section_Header("DELETE STUDENT")
        Delete_Roll = input("  Enter Roll Number to Delete  >>  ")

        if Delete_Roll not in DF['Roll_No'].astype(str).values:
            print(f"\n  No student found with Roll No: {Delete_Roll}")
        else:
            Confirm = input("  Are you sure you want to delete this student? (Y / N):  ")
            while Confirm.lower() != "y" and Confirm.lower() != "n":
                print("  Invalid input. Enter Y or N only.")
                Confirm = input("  Are you sure? (Y / N):  ")

            if Confirm.lower() == "y":
                DF = DF[DF['Roll_No'].astype(str) != Delete_Roll]
                DF.to_csv("students.csv", index=False)
                print(f"\n  Student {Delete_Roll} has been deleted.")
            else:
                print("\n  Delete cancelled.")

    elif Choice == 6:
        Stop = True

    if Stop == False:
        Repeat = input("\n  Press Y to return to the main menu or N to exit  >>  ")
        while Repeat.lower() != "y" and Repeat.lower() != "n":
            print("  Invalid input. Enter Y or N only.")
            Repeat = input("  Press Y to return to the main menu or N to exit  >>  ")

        if Repeat.lower() == "n":
            Stop = True

print()
print(Rule())
print("  Thank you for using the Student Management System.".center(W))
print(Rule())
print()
