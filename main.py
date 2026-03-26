import sqlite3

# Connect to the database
connection = sqlite3.connect('registration.sqlite')
cursor = connection.cursor()

# Helper function to list any table
def list_table(table):
    cursor.execute(f"SELECT * FROM {table}")
    for row in cursor:
        print(row)

choice = ""

while choice != "QUIT":

    choice = input(
        "\nEnter a choice:\n"
        "1 - Manage Faculty\n"
        "2 - Manage Course\n"
        "3 - Manage Section\n"
        "4 - Manage Student\n"
        "5 - Manage Enrollment\n"
        "6 - Show Student Transcript\n"
        "Type QUIT to exit\n"
    )

    # -------------------------
    # FACULTY (Provided Starter)
    # -------------------------
    if choice == "1":
        action = input("Enter 1 List, 2 Add, 3 Update: ")

        if action == "1":
            print("id, name, email")
            cursor.execute("SELECT * FROM Faculty")
            for row in cursor:
                print(row)

        elif action == "2":
            name = input("Enter name: ")
            email = input("Enter email: ")
            cursor.execute(
                "INSERT INTO Faculty (name, email) VALUES (?, ?)",
                (name, email)
            )
            connection.commit()

        elif action == "3":
            id = int(input("Enter the ID to update: "))
            name = input("Enter name: ")
            email = input("Enter email: ")
            cursor.execute(
                "UPDATE Faculty SET name = ?, email = ? WHERE id = ?",
                (name, email, id)
            )
            connection.commit()

    # -------------------------
    # COURSE (CRU)
    # -------------------------
    elif choice == "2":
        action = input("Enter 1 List, 2 Add, 3 Update: ")

        if action == "1":
            list_table("Course")

        elif action == "2":
            dept = input("Enter department: ")
            number = input("Enter number: ")
            credits = input("Enter credits: ")
            cursor.execute(
                "INSERT INTO Course (Department, Number, Credits) VALUES (?, ?, ?)",
                (dept, number, credits)
            )
            connection.commit()

        elif action == "3":
            id = int(input("Enter ID to update: "))
            dept = input("Enter department: ")
            number = input("Enter number: ")
            credits = input("Enter credits: ")
            cursor.execute(
                "UPDATE Course SET Department=?, Number=?, Credits=? WHERE ID=?",
                (dept, number, credits, id)
            )
            connection.commit()

    # -------------------------
    # SECTION (CRU)
    # -------------------------
    elif choice == "3":
        action = input("Enter 1 List, 2 Add, 3 Update: ")

        if action == "1":
            list_table("Section")

        elif action == "2":
            course_id = int(input("Enter course ID: "))
            faculty_id = int(input("Enter faculty ID: "))
            semester = input("Enter semester: ")
            cursor.execute(
                "INSERT INTO Section (Course_ID, Faculty_ID, Semester) VALUES (?, ?, ?)",
                (course_id, faculty_id, semester)
            )
            connection.commit()

        elif action == "3":
            id = int(input("Enter ID to update: "))
            course_id = int(input("Enter course ID: "))
            faculty_id = int(input("Enter faculty ID: "))
            semester = input("Enter semester: ")
            cursor.execute(
                "UPDATE Section SET Course_ID=?, Faculty_ID=?, Semester=? WHERE ID=?",
                (course_id, faculty_id, semester, id)
            )
            connection.commit()

    # -------------------------
    # STUDENT (CRU)
    # -------------------------
    elif choice == "4":
        action = input("Enter 1 List, 2 Add, 3 Update: ")

        if action == "1":
            list_table("Student")

        elif action == "2":
            name = input("Enter name: ")
            email = input("Enter email: ")
            cursor.execute(
                "INSERT INTO Student (Name, Email) VALUES (?, ?)",
                (name, email)
            )
            connection.commit()

        elif action == "3":
            id = int(input("Enter ID to update: "))
            name = input("Enter name: ")
            email = input("Enter email: ")
            cursor.execute(
                "UPDATE Student SET Name=?, Email=? WHERE ID=?",
                (name, email, id)
            )
            connection.commit()

    # -------------------------
    # ENROLLMENT (CRUD)
    # -------------------------
    elif choice == "5":
        action = input("Enter 1 List, 2 Add, 3 Update, 4 Delete: ")

        if action == "1":
            list_table("Enrollment")

        elif action == "2":
            student_id = int(input("Enter student ID: "))
            section_id = int(input("Enter section ID: "))
            grade = input("Enter grade (or blank): ")
            cursor.execute(
                "INSERT INTO Enrollment (Student_ID, Section_ID, Grade) VALUES (?, ?, ?)",
                (student_id, section_id, grade)
            )
            connection.commit()

        elif action == "3":
            id = int(input("Enter enrollment ID to update: "))
            grade = input("Enter new grade: ")
            cursor.execute(
                "UPDATE Enrollment SET Grade=? WHERE ID=?",
                (grade, id)
            )
            connection.commit()

        elif action == "4":
            id = int(input("Enter enrollment ID to delete: "))
            cursor.execute("DELETE FROM Enrollment WHERE ID=?", (id,))
            connection.commit()

    # -------------------------
    # TRANSCRIPT (JOIN QUERY)
    # -------------------------
    elif choice == "6":
        student_id = int(input("Enter student ID: "))
        cursor.execute("""
            SELECT Course.Department, Course.Number, Course.Credits, Enrollment.Grade
            FROM Enrollment
            INNER JOIN Student ON Student.ID = Enrollment.Student_ID
            INNER JOIN Section ON Section.ID = Enrollment.Section_ID
            INNER JOIN Course ON Course.ID = Section.Course_ID
            WHERE Student_ID = ?
        """, (student_id,))

        print("Dept | Number | Credits | Grade")
        for row in cursor:
            print(row)

# Close connection
connection.close()