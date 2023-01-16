import mysql.connector as conn
import EdSt.Function_CUI as cui

# main program loop
while True:
    user = int(input("User ID: "))  # User Id
    Password = input("Password: ")  # Password
    SignIn = cui.SignIn(user, Password)  # Signing in. Checking user access.

    # Student User
    if SignIn == 'Student.valid':
        cui.message_hello_student(user)
        while True:
            # Dashboard Menu
            print("""\n\tDashboard
            1. Profile
            2. Announcement
            3. Assignment
            4. Marks
            5. Log Out""")
            try:
                student_menu = int(input("Enter Menu Selection: "))  # Dashboard menu
                try:
                    # if Student User chooses 'Profile'
                    if student_menu == 1:
                        # Displaying student profile info
                        s_Profile = cui.view_studentProfile_student(user)

                        while True:
                            # Profile Menu
                            print("1. Change Password?\n"
                                  "2. Back to Dashboard")
                            student_profile_menu = int(input("Enter menu Selection: "))

                            # if Student User chooses 'Change Password?'
                            if student_profile_menu == 1:
                                old_password = input("Enter old passward: ")  # Accept old password

                                # Compare user entered password with original password (Check access)
                                if old_password == Password:
                                    new_password = input("Enter new password: ")
                                    new_password_confirm = input("Confirm new password: ")
                                    if new_password == new_password_confirm:
                                        cui.edit_profile_all(SignIn, user, 'Password', new_password_confirm)
                                        print("Password succefully changed!")
                                    else:
                                        print("Error! The passwords do not match!")
                                else:
                                    print("Error! Incorrect password!")
                            elif student_profile_menu == 2:
                                break
                            else:
                                print("Invalid selection. Try again.")
                    elif student_menu == 2:
                        print("Announcements")
                        cui.view_announcement_student(user)
                    elif student_menu == 3:
                        print("Assignments")
                        cui.view_assignment_student(user)
                    elif student_menu == 4:
                        print("Marks")
                        cui.view_testResult_student(user)
                    elif student_menu == 5:
                        print("\nLogging Out...")
                        print("Logged Out!\n")
                        break
                    else:
                        print("Invalid selection. Try again.")
                except conn.errors.DataError:
                    print("Error! Invalid input!")
            except ValueError:
                print("Invalid input. Try again.")

    elif SignIn == 'Teacher.valid':
        cui.message_hello_teacher(user)
        while True:
            print("""
            \tDashboard
            1. Profile
            2. Announcement
            3. Assignment
            4. Marks
            5. Student Details
            6. Log Out""")
            try:
                teacher_menu = int(input("Enter Menu Selection: "))  # Dashboard menu
                try:
                    if teacher_menu == 1:
                        # Displaying teacher profile info
                        t_Profile = cui.view_teacherProfile_teacher(user)
                        print(t_Profile)

                        while True:
                            # Profile Menu
                            print("1. Change Password?\n"
                                  "2. Back to Dashboard")
                            teacher_profile_menu = int(input("Enter Menu Selection: "))

                            # if Teacher User chooses 'Change Password?'
                            if teacher_profile_menu == 1:
                                old_password = input("Enter old passward: ")  # Accept old password

                                # Compare user entered password with original password (Check access)
                                if old_password == Password:
                                    new_password = input("Enter new password: ")
                                    new_password_confirm = input("Confirm new password: ")
                                    if new_password == new_password_confirm:
                                        cui.edit_profile_all(SignIn, user, 'Password', new_password_confirm)
                                        print("Password succefully changed!")
                                    else:
                                        print("Error! The passwords do not match!")

                                else:
                                    print("Error! Incorrect password!")
                            elif teacher_profile_menu == 2:
                                break

                            else:
                                print("Invalid selection. Try again.")
                    elif teacher_menu == 2:
                        coordinator = cui.check_coordinator_teacher(user)

                        # if Teacher is Coordinator
                        if coordinator is True:
                            while True:
                                teacher_menu_2 = """
                                    Announcements
                                    1) View announcements
                                    2) Add announcement
                                    3) Delete announcement
                                    4) Return to Dashboard"""
                                print(teacher_menu_2)
                                teacher_announcements_menu = int(input("Enter selection: "))
                                if teacher_announcements_menu == 1:
                                    print("Announcements")
                                    cui.view_announcements_teacher(user)
                                elif teacher_announcements_menu == 2:
                                    cui.add_announcement_teacher(user)
                                elif teacher_announcements_menu == 3:
                                    cui.del_announcement_teacher(user)
                                elif teacher_announcements_menu == 4:
                                    break
                                else:
                                    print("Invalid selection. Try again.")
                        else:
                            cui.view_announcements_teacher(user)

                    elif teacher_menu == 3:
                        while True:
                            teacher_menu_3 = """
                                Assignments
                                1) View assignments
                                2) Add assignment
                                3) Delete assignment
                                4) Return to Dashboard"""
                            print(teacher_menu_3)
                            teacher_assignments_menu = int(input("Enter selection: "))
                            if teacher_assignments_menu == 1:
                                print("Assignments")
                                cui.view_assignment_teacher(user)
                            elif teacher_assignments_menu == 2:
                                cui.add_assignment_teacher(user)
                            elif teacher_assignments_menu == 3:
                                cui.del_assignment_teacher(user)
                            elif teacher_assignments_menu == 4:
                                break
                            else:
                                print("Invalid selection. Try again.")
                    elif teacher_menu == 4:
                        while True:
                            teacher_menu_4 = """
                                Marks
                                1) View student marks
                                2) Add student marks
                                3) Return to Dashboard"""
                            print(teacher_menu_4)
                            teacher_marks_menu = int(input("Enter selection: "))
                            if teacher_marks_menu == 1:
                                print("Marks")
                                cui.view_testResult_teacher(user)
                            elif teacher_marks_menu == 2:
                                cui.add_testResult_teacher(user)
                            elif teacher_marks_menu == 3:
                                break
                            else:
                                print("Invalid selection. Try again.")
                    elif teacher_menu == 5:
                        cui.view_studentDetails_teacher(user)
                    elif teacher_menu == 6:
                        print("\nLogging Out...")
                        print("Logged Out!\n")
                        break
                    else:
                        print("Invalid selection. Try again.")
                except conn.errors.DataError:
                    print("Error! Invalid input!")
            except ValueError:
                print("Invalid input. Try again.")

    elif SignIn == 'Admin.valid':
        while True:
            print("""
            \tDASHBOARD
            1. Announcement
            2. Assignment
            3. Teacher Details
            4. Student Details
            5. Marks
            6. Classes
            7. Change Password
            8. Log Out
            """)
            try:
                admin_menu = int(input("Enter Menu Selection: "))
                try:
                    if admin_menu == 1:
                        while True:
                            admin_menu_1 = """
                            Announcements
                            1) View announcements
                            2) Add announcement
                            3) Delete announcement
                            4) Return to Dashboard"""
                            print(admin_menu_1)
                            admin_announcements_menu = int(input("Enter selection: "))
                            if admin_announcements_menu == 1:
                                cui.view_announcements_admin()
                            elif admin_announcements_menu == 2:
                                cui.add_announcement_teacher(12)
                            elif admin_announcements_menu == 3:
                                cui.del_announcement_teacher(12)
                            elif admin_announcements_menu == 4:
                                break
                            else:
                                print("Invalid selection. Try again.")
                    elif admin_menu == 2:
                        while True:
                            admin_menu_2 = """
                            Assignments
                            1) View assignments
                            2) Add assignment
                            3) Delete assignment
                            4) Return to Dashboard"""
                            print(admin_menu_2)
                            admin_assignments_menu = int(input("Enter selection: "))
                            if admin_assignments_menu == 1:
                                cui.view_assignment_admin()
                            elif admin_assignments_menu == 2:
                                cui.add_assignment_teacher(12)
                            elif admin_assignments_menu == 3:
                                cui.del_assignment_teacher(12)
                            elif admin_assignments_menu == 4:
                                break
                            else:
                                print("Invalid selection. Try again.")
                    elif admin_menu == 3:
                        while True:
                            admin_menu_3 = """
                            Teacher Details
                            1) View Teacher Details
                            2) Add Teacher
                            3) Edit Teacher details
                            4) Remove Teacher
                            5) Return to Dashboard"""
                            print(admin_menu_3)
                            admin_teacherDetails_menu = int(input("Enter selection: "))
                            if admin_teacherDetails_menu == 1:
                                cui.view_teacherDetails_admin()
                            elif admin_teacherDetails_menu == 2:
                                cui.add_teacherDetails_admin()
                            elif admin_teacherDetails_menu == 3:
                                cui.edit_teacherProfile()
                            elif admin_teacherDetails_menu == 4:
                                cui.del_teacherProfile()
                            elif admin_teacherDetails_menu == 5:
                                break
                            else:
                                print("Invalid selection. Try again.")
                    elif admin_menu == 4:
                        while True:
                            admin_menu_4 = """
                            Student Details
                            1) View Student Details
                            2) Add Student
                            3) Edit Student details
                            4) Remove Student
                            5) Return to Dashboard"""
                            print(admin_menu_4)
                            admin_studentDetails_menu = int(input("Enter selection: "))
                            if admin_studentDetails_menu == 1:
                                cui.view_studentDetails_admin()
                            elif admin_studentDetails_menu == 2:
                                cui.add_studentDetails_admin()
                            elif admin_studentDetails_menu == 3:
                                cui.edit_studentProfile_admin()
                            elif admin_studentDetails_menu == 4:
                                cui.del_studentProfile_admin()
                            elif admin_studentDetails_menu == 5:
                                break
                            else:
                                print("Invalid selection. Try again.")
                    elif admin_menu == 5:
                        cui.view_testResult_admin()
                    elif admin_menu == 6:
                        while True:
                            admin_menu_6 = """
                            Classes
                            1) View Classes
                            2) Add a Class
                            3) Remove Class
                            4) Return to Dashboard"""
                            print(admin_menu_6)
                            admin_classes_menu = int(input("Enter selection: "))
                            if admin_classes_menu == 1:
                                cui.view_classes_admin()
                            elif admin_classes_menu == 2:
                                cui.add_class_admin()
                            elif admin_classes_menu == 3:
                                print("Delete Classes")
                            elif admin_classes_menu == 4:
                                break
                            else:
                                print("Invalid selection. Try again.")
                    elif admin_menu == 7:
                        old_password = input("Enter old passward: ")  # Accept old password

                        # Compare user entered password with original password (Check access)
                        if old_password == Password:
                            new_password = input("Enter new password: ")
                            new_password_confirm = input("Confirm new password: ")
                            if new_password == new_password_confirm:
                                cui.edit_profile_all(SignIn, user, 'Password', new_password)
                                print("Password succefully changed!")
                            else:
                                print("Error! The passwords do not match!")

                        else:
                            print("Error! Incorrect password!")
                    elif admin_menu == 8:
                        print("\nLogging Out...")
                        print("Logged Out!\n")
                        break
                    else:
                        print("Invalid selection. Try again.")
                except conn.errors.DataError:
                    print("Error! Invalid input!")
            except ValueError:
                print("Invalid input. Try again.")

    elif SignIn == 'Error!':
        print('Error! Exit program?\n(n/y)')
        Exit = input()
        if Exit.lower() in ('y', 'yes'):
            exit(0)

    else:
        print("Error!")
        print('Exit the program?\n(n/y)')
        Exit = input()
        if Exit.lower() in ('y', 'yes'):
            exit(0)

    print('Exit the program?\n(n/y)')
    Exit = input()
    if Exit.lower() in ('y', 'yes'):
        exit(0)
