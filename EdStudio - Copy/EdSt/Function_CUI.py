from EdSt.Functions_DB_setup import connect

psword = "dpsbn"


# SIGN IN
def SignIn(userId: int, password):
    con = connect(pswrd=psword)
    cur = con.cursor()
    cur.execute("SELECT Id, Password FROM Student")
    sID = cur.fetchall()
    if (userId, password) in sID:
        con.close()
        return "Student.valid"

    cur.execute("SELECT Id, Password FROM Teacher")
    tID = cur.fetchall()
    if (userId, password) in tID:
        con.close()
        return "Teacher.valid"

    cur.execute("SELECT Id, Password FROM Admin")
    aID = cur.fetchall()
    if (userId, password) in aID:
        con.close()
        return "Admin.valid"

    if ((userId, password) not in sID) and ((userId, password) not in tID):
        con.close()
        return "Error!"
    con.close()


# WELCOME BACK STUDENT
def message_hello_student(StudentUser):
    con = connect(pswrd=psword)
    cur = con.cursor()
    cur.execute("SELECT name from student where id={}".format(StudentUser))
    d = cur.fetchall()
    for i in d:
        name = i[0]
    print("\nWelcome", name + "!")
    con.close()


# VIEW STUDENT PROFILE
def view_studentProfile_student(StudentUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    query = '''SELECT student.id, student.name,grade.id,class.division,
                student.photo,student.gender,
                student.dateofbirth,guardian.name,student.bloodgroup,student.phoneno,student.address,
                student.dateofadmission,guardian.name
                from student 
                inner join studentclass on studentclass.studentid=student.id
                inner join class on class.id=studentclass.classid
                inner join grade on grade.id=class.gradeid
                inner join studguardrelate on studguardrelate.studentid=student.id
                inner join guardian on guardian.id=studguardrelate.guardianid
                where student.id={}'''
    cur.execute(query.format(StudentUser))
    d = cur.fetchall()
    for i in d:
        print("\nAdmission ID", i[0], sep=":        ")
        print("Name", i[1], sep=":                ")
        print("Grade", i[2], sep=":               ")
        print("Division", i[3], sep=":            ")
        print("Photo", i[4], sep=":               ")
        print("Gender", i[5], sep=":              ")
        print("Date of Birth", i[6], sep=":       ")
        print("Guardian Name", i[7], sep=":       ")
        print("Blood group", i[8], sep=":         ")
        print("Phone no.", i[9], sep=":           ")
        print("Address", i[10], sep=":            ")
        print("Date of admission", i[11], sep=":  ", end="\n\n")
    con.close()


# UPDATE USER PROFILE
def edit_profile_all(UserType: str, UserId: int, Field: str, UpdatedValue):
    con = connect(pswrd=psword)
    cur = con.cursor()
    if UserType == 'Student.valid':
        qs = 'UPDATE Student SET {}="{}" WHERE Id={}'.format(Field, UpdatedValue, UserId)
        cur.execute(qs)
        cur.execute('COMMIT')
        cur.execute("SELECT * FROM Student WHERE Id={}".format(UserId))
        sData = cur.fetchone()
        return sData
    elif UserType == 'Teacher.valid':
        qt = 'UPDATE Teacher Set {}="{}" WHERE Id={}'.format(Field, UpdatedValue, UserId)
        cur.execute(qt)
        cur.execute('COMMIT')
        cur.execute("SELECT * FROM Teacher WHERE Id={}".format(UserId))
        tData = cur.fetchone()
        con.close()
        return tData
    elif UserType == 'Admin.valid':
        qa = 'UPDATE Admin Set {}="{}" WHERE Id={}'.format(Field, UpdatedValue, UserId)
        cur.execute(qa)
        cur.execute('COMMIT')
        cur.execute("SELECT * FROM Admin WHERE Id={}".format(UserId))
        aData = cur.fetchone()
        con.close()
        return aData
    else:
        con.close()
        return 'Error!'


# VIEW ANNOUCEMENT STUDENT
def view_announcement_student(StudentUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    import tabulate
    query1 = '''SELECT grade.id from grade
                        inner join class on class.gradeid=grade.id
                        inner join studentclass on studentclass.classid=class.id
                        inner join student on student.id=studentclass.studentid
                        where student.id={}'''
    cur.execute(query1.format(StudentUser))
    d = cur.fetchall()
    for i in d:
        grade_id = i[0]
    query = '''SELECT Teacher.Name, Announcement.SubjectPreview, 
                       Announcement.AnnouncementDate, 
                       Announcement.Attachment
                       FROM Announcement
                       INNER JOIN Teacher ON Teacher.Id = Announcement.TeacherId
                       WHERE announcement.gradeid={}
                       ORDER BY Announcement.GradeId;'''
    cur.execute(query.format(grade_id))
    d = tuple(cur.fetchall())
    header = (('Teacher', 'SubjectPreview', 'Date', 'Attachment'),)
    retrieve = header + d
    table = tabulate.tabulate(retrieve, tablefmt='fancy_grid')
    print(table, end="\n\n")
    con.close()


# VIEW ASSIGNMENT STUDENT
def view_assignment_student(StudentUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    import tabulate
    List = []
    query1 = '''select class.gradeid,student.id
            from student
            inner join studentclass on studentclass.studentid=student.id
            inner join class on class.id=studentclass.classid
            where student.id={}'''
    cur.execute(query1.format(StudentUser))
    d = cur.fetchall()
    List.append(d[0][0])
    for i in List:
        class_int = int(i)
    query2 = '''SELECT Subject.SubName, Teacher.Name, Assignment.Topic, 
            Assignment.StartDate, Assignment.DueDate, Assignment.Attachment
            FROM Assignment
            INNER JOIN Teacher ON Teacher.Id = Assignment.TeacherId
            INNER JOIN Subject ON Subject.Id = Assignment.SubjectId
            WHERE Assignment.gradeid={}'''
    cur.execute(query2.format(class_int))
    d = tuple(cur.fetchall())
    header = (('Subject', 'Teacher', 'Topic', 'StartDate', 'DueDate', 'Attachment'),)
    retrieve = header + d
    table = tabulate.tabulate(retrieve, tablefmt='fancy_grid')
    print(table, end="\n\n")
    con.close()


# VIEW TEST RESULT STUDENT
def view_testResult_student(StudentUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    import tabulate
    print('''1.UNIT TEST 1
2.QUARTERLY EXAMINATION
3.HALF YEARLY EXAMINATION
4.UNIT TEST 2
5.ANNUAL EXAMINATION''')
    exam = int(input('Select exam: '))
    query = '''SELECT subject.subname,
                    marks.marksscored
                    from student
                    inner join marks on marks.studentid=student.id
                    inner join exam on exam.id=marks.examid
                    inner join subject on subject.id=exam.subjectid
                    inner join examgroup on examgroup.id=exam.groupid
                    where student.id={} && examgroup.id={}'''
    if exam == 1:
        cur.execute(query.format(StudentUser, 101))
        d = tuple(cur.fetchall())
        header = (('SUBJECT', 'MARKS'),)
        retrieve = header + d
        table = tabulate.tabulate(retrieve, tablefmt="fancy_grid")
        print(table, end="\n\n")
    if exam == 2:
        cur.execute(query.format(StudentUser, 103))
        d = tuple(cur.fetchall())
        header = (('SUBJECT', 'MARKS'),)
        retrieve = header + d
        table = tabulate.tabulate(retrieve, tablefmt="fancy_grid")
        print(table, end="\n\n")
    if exam == 3:
        cur.execute(query.format(StudentUser, 104))
        d = tuple(cur.fetchall())
        header = (('SUBJECT', 'MARKS'),)
        retrieve = header + d
        table = tabulate.tabulate(retrieve, tablefmt="fancy_grid")
        print(table, end="\n\n")
    if exam == 4:
        cur.execute(query.format(StudentUser, 102))
        d = tuple(cur.fetchall())
        header = (('SUBJECT', 'MARKS'),)
        retrieve = header + d
        table = tabulate.tabulate(retrieve, tablefmt="fancy_grid")
        print(table, end="\n\n")
    if exam == 5:
        cur.execute(query.format(StudentUser, 105))
        d = tuple(cur.fetchall())
        header = (('SUBJECT', 'MARKS'),)
        retrieve = header + d
        table = tabulate.tabulate(retrieve, tablefmt="fancy_grid")
        print(table, end="\n\n")
    con.close()


# WELCOME BACK TEACHER
def message_hello_teacher(TeacherUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    cur.execute("SELECT name from teacher where id={}".format(TeacherUser))
    d = cur.fetchall()
    for i in d:
        name = i[0]
    print("\nWelcome", name + "!")
    con.close()


# VIEW TEACHER PROFILE
def view_teacherProfile_teacher(TeacherUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    query = '''SELECT Teacher.id, Teacher.name,subject.SubName,
                   Teacher.photo,Teacher.coordinator,
                   Teacher.dateofbirth,Teacher.EdQualifications,
                   Teacher.phoneno,Teacher.status
                   from teacher
                   inner join teachersubject on teachersubject.teacherid=Teacher.id
                   inner join subject on subject.id=teachersubject.Subjectid
                   where Teacher.id={}'''.format(TeacherUser)
    cur.execute(query)
    d = cur.fetchall()
    for i in d:
        print("\nID", i[0], sep=":                 ")
        print("Name", i[1], sep=":               ")
        print("Subject", i[2], sep=":            ")
        print("Photo", i[3], sep=":              ")
        print("Coordinator", i[4], sep=":        ")
        print("D.O.B", i[5], sep=":              ")
        print("EdQualifications", i[6], sep=":   ")
        print("Contact number", i[7], sep=":    ")
        print("Status", i[8], sep=":            ", end='\n\n')
    con.close()


# IS COORDINATOR CHECK
def check_coordinator_teacher(TeacherUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    query2 = '''SELECT coordinator from teacher where Id={}'''
    cur.execute(query2.format(TeacherUser))
    d = cur.fetchall()
    for j in d:
        coordinator = j[0]
        if coordinator == 'T':
            con.close()
            return True
    con.close()
    return False


# VIEW ANNOUNCEMENT TEACHER
def view_announcements_teacher(TeacherUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    import tabulate
    query1 = '''SELECT grade.id from grade
                    inner join class on class.gradeid=grade.id
                    inner join teachersubjectclass on teachersubjectclass.classid=class.id
                    inner join teachersubject on teachersubject.subjectid=teachersubjectclass.teachersubjectid
                    inner join teacher on Teacher.id=teachersubject.teacherid
                    where Teacher.id={}'''
    cur.execute(query1.format(TeacherUser))
    d = cur.fetchall()
    if d == []:
        print("Annnouncements Data Not Found.", end="\n\n")
        return None
    for i in d:
        grade_id = i[0]
        query2 = '''SELECT Announcement.Id, Teacher.Name, Announcement.SubjectPreview, 
                    Announcement.AnnouncementDate, 
                    Announcement.Attachment
                    FROM Announcement
                    INNER JOIN Teacher ON Teacher.Id = Announcement.TeacherId
                    WHERE announcement.gradeid={}
                    ORDER BY Announcement.GradeId;'''
    cur.execute(query2.format(grade_id))
    d = tuple(cur.fetchall())
    header = (('S.No', 'Teacher', 'SubjectPreview', 'Date', 'Attachment'),)
    retrieve = header + d
    table = tabulate.tabulate(retrieve, tablefmt='fancy_grid')
    print(table, end="\n\n")
    con.close()


# ADD ANNOUNCEMENT TEACHER
def add_announcement_teacher(TeacherUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    query1 = '''SELECT grade.id from grade
                inner join class on class.gradeid=grade.id
                inner join teachersubjectclass on teachersubjectclass.classid=class.id
                inner join teachersubject on teachersubject.subjectid=teachersubjectclass.teachersubjectid
                inner join teacher on Teacher.id=teachersubject.teacherid
                where Teacher.id={}'''
    cur.execute(query1.format(TeacherUser))
    d = cur.fetchall()
    for i in d:
        grade_id = i[0]
    query2 = '''SELECT COUNT(*) from announcement'''
    cur.execute(query2)
    d = cur.fetchall()
    for i in d:
        length = i[0]
    sn_no = length + 1
    query3 = '''SELECT CURDATE()'''
    cur.execute(query3)
    d = cur.fetchall()
    for i in d:
        date = i[0]
    sub_preview = input("Enter subject:")
    attachment = input("Enter attachment:")
    query4 = '''INSERT INTO announcement VALUES({},{},{},'{}','{}','{}')'''
    cur.execute(query4.format(sn_no, grade_id, TeacherUser, date, sub_preview, attachment))
    con.commit()
    print("Successfully added", end="\n\n")
    con.close()


# DELETE ANNOUNCEMENT TEACHER
def del_announcement_teacher(TeacherUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    query1 = '''SELECT grade.Id from grade
                        inner join class on class.gradeid=grade.Id
                        inner join teachersubjectclass on teachersubjectclass.classid=class.Id
                        inner join teachersubject on teachersubject.subjectid=teachersubjectclass.teachersubjectid
                        inner join teacher on Teacher.Id=teachersubject.teacherid
                        where Teacher.Id={}'''
    cur.execute(query1.format(TeacherUser))
    d1 = cur.fetchall()
    for i in d1:
        grade_id = i[0]
        query2 = '''SELECT coordinator from teacher where Id={}'''
        cur.execute(query2.format(TeacherUser))
        d2 = cur.fetchall()
    for j in d2:
        coordinator = j[0]
        if coordinator == 'T':
            Id = int(input("Enter Announcement ID to be deleted:"))
            query3 = '''SELECT gradeid from announcement where Id={}'''
            cur.execute(query3.format(Id))
            d3 = cur.fetchall()
            for k in d3:
                g = k[0]
            if grade_id == g:
                query4 = '''DELETE FROM announcement WHERE Id={}'''
                cur.execute(query4.format(Id))
                con.commit()
                print("Deletion complete", end="\n\n")
            else:
                print("Unable to carry out deletion", end="\n\n")
        else:
            print("Unable to carry out deletion.", end="\n\n")
    con.close()


# VIEW ASSIGNMENT TEACHER
def view_assignment_teacher(TeacherUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    import tabulate
    query = '''SELECT subject.id from subject
            inner join teachersubject on teachersubject.subjectid=subject.id
            inner join teacher on Teacher.id=teachersubject.teacherid
            WHERE Teacher.id={}'''
    cur.execute(query.format(TeacherUser))
    d = cur.fetchall()
    for i in d:
        subject_id = i[0]
    query2 = '''SELECT Assignment.Id, Subject.SubName, Teacher.Name, Assignment.Topic, 
            Assignment.StartDate, Assignment.DueDate, Assignment.Attachment
            FROM Assignment
            INNER JOIN Teacher ON Teacher.Id = Assignment.TeacherId
            INNER JOIN Subject ON Subject.Id = Assignment.SubjectId
            WHERE Assignment.subjectid={}'''
    cur.execute(query2.format(subject_id))
    d = tuple(cur.fetchall())
    header = (('S.No.','Subject', 'Teacher', 'Topic', 'StartDate', 'DueDate', 'Attachment'),)
    retrieve = header + d
    table = tabulate.tabulate(retrieve, tablefmt='fancy_grid')
    print(table, end="\n\n")
    con.close()


# ADD ASSIGNMENT TEACHER
def add_assignment_teacher(TeacherUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    query1 = '''SELECT subject.id from subject
                inner join teachersubject on teachersubject.subjectid=subject.id
                inner join teacher on Teacher.id=teachersubject.teacherid
                WHERE Teacher.id={}'''
    cur.execute(query1.format(TeacherUser))
    d1 = cur.fetchall()
    query2 = '''SELECT MAX(id) from assignment'''
    cur.execute(query2)
    d = cur.fetchall()
    for i in d:
        length = i[0]
    sn_no = length + 1
    grade = int(input("Enter grade:"))
    if len(d1) > 1:
        print("""
        Subject Ids:
        +----+------------------+
        | Id | Subject Name     |
        +----+------------------+
        |  1 | Mathematics 1    |
        |  2 | Science          |
        |  3 | Social Science   |
        |  4 | English 1        |
        |  5 | Physics          |
        |  6 | Chemistry        |
        |  7 | Mathematics 2    |
        |  8 | English 2        |
        |  9 | Computer Science |
        | 10 | Biology          |
        +----+------------------+""")
        subject_id = int(input("Enter subject Id:"))
    else:
        for i in d1:
            subject_id = i[0]
    topic = input("Enter topic:")
    start_date = input("Enter start date:")
    due_date = input("Enter due date:")
    attachment = input("Enter attachment:")
    query3 = '''INSERT INTO assignment values({},{},{},{},'{}','{}','{}','{}')'''
    cur.execute(query3.format(sn_no, TeacherUser, grade, subject_id, topic, start_date, due_date, attachment))
    con.commit()
    print("Successfully added", end="\n\n")
    con.close()


# DELETE ASSIGNMENT TEACHER
def del_assignment_teacher(TeacherUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    query1 = '''SELECT subject.id from subject
                    inner join teachersubject on teachersubject.subjectid=subject.id
                    inner join teacher on Teacher.id=teachersubject.teacherid
                    WHERE Teacher.id={}'''
    cur.execute(query1.format(TeacherUser))
    d = cur.fetchall()
    for i in d:
        subject_id = i[0]
    cur.execute("SELECT COUNT(*) FROM assignment")
    d = cur.fetchall()
    for i in d:
        p = i[0]
    assignment_id = int(input("Enter assignment no:"))
    if assignment_id <= p:
        query = '''delete from assignment where id={}'''
        cur.execute(query.format(assignment_id, subject_id))
        con.commit()
        print("Successfully deleted!", end="\n\n")
    else:
        print("Invalid assignment number", end="\n\n")
    con.close()


# ADD TEST RESULT TEACHER
def add_testResult_teacher(TeacherUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    query1 = "select subjectid from teachersubject where teacherid={}".format(TeacherUser)
    cur.execute(query1)
    [subject_id] = cur.fetchall()
    for i in subject_id:
        query2 = "select id, subname from subject where id={}".format(i)
        cur.execute(query2)
        [(Id, Subjects)] = cur.fetchall()
        print("Subjects:")
        print(str(Id) + '.', Subjects)
        subject = int(input("Enter subject ID: "))
    print('''\nExaminations:
        1. Annual Examination      
        2. Half-Yearly Examination 
        3. Pre-Board 1             
        4. Pre-Board 2             
        5. Quarterly Examination   
        6. Unit Test 1             
        7. Unit Test 2             
        8. Weekly Test''')
    examgroup = int(input("Select exam name:"))
    if examgroup == 1:
        examgroup = 105
    elif examgroup == 2:
        examgroup = 104
    elif examgroup == 3:
        examgroup = 106
    elif examgroup == 4:
        examgroup = 107
    elif examgroup == 5:
        examgroup = 103
    elif examgroup == 6:
        examgroup = 101
    elif examgroup == 7:
        examgroup = 102
    elif examgroup == 8:
        examgroup = 100
    student_id = int(input("Enter Student ID: "))
    query3 = """Select gradeid from class
    Inner join studentclass on studentclass.classid=class.id
    Where studentclass.studentid={};""".format(student_id)
    cur.execute(query3)
    [(grade,)] = cur.fetchall()
    query4 = "SELECT id FROM exam where gradeid={} && subjectid={} && groupid={};".format(grade, subject, examgroup)
    cur.execute(query4)
    [(exam_id,)] = cur.fetchall()
    marks = int(input("Enter marks scored: "))
    query5 = "SELECT max(id) from marks;"
    cur.execute(query5)
    [(s_no,)] = cur.fetchall()
    s_no = int(s_no) + 1
    query6 = "INSERT INTO marks values({},{},{},{});".format(s_no, student_id, exam_id, marks)
    cur.execute(query6)
    con.commit()
    print("Successfully added", end="\n\n")
    con.close()


# VIEW TEST RESULT TEACHER
def view_testResult_teacher(TeacherUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    import tabulate
    query1 = "select subjectid from teachersubject where teacherid={}".format(TeacherUser)
    cur.execute(query1)
    [subject_id] = cur.fetchall()
    for i in subject_id:
        query2 = "select id, subname from subject where id={}".format(i)
        cur.execute(query2)
        [(Id, Subjects)] = cur.fetchall()
        print("Subjects:")
        print(str(Id) + '.', Subjects)
        subject = int(input("Enter subject ID: "))
    print('''\nExaminations:
        1. Annual Examination
        2. Half-Yearly Examination
        3. Pre-Board 1
        4. Pre-Board 2
        5. Quarterly Examination
        6. Unit Test 1
        7. Unit Test 2
        8. Weekly Test''')
    examgroup = int(input("Select exam name:"))
    if examgroup == 1:
        examgroup = 105
    elif examgroup == 2:
        examgroup = 104
    elif examgroup == 3:
        examgroup = 106
    elif examgroup == 4:
        examgroup = 107
    elif examgroup == 5:
        examgroup = 103
    elif examgroup == 6:
        examgroup = 101
    elif examgroup == 7:
        examgroup = 102
    elif examgroup == 8:
        examgroup = 100
    query = '''SELECT student.id, student.name, exam.gradeid, examgroup.type, subject.subname, 
    marks.marksscored, exam.maxmark FROM exam INNER JOIN examgroup ON examgroup.id = exam.groupid 
    INNER JOIN subject ON subject.id=exam.subjectid 
    INNER JOIN marks ON marks.examid = exam.id 
    INNER JOIN student ON student.id = marks.studentid 
    WHERE exam.subjectid={} && exam.groupid={}
    ORDER BY student.name, exam.gradeid, examgroup.type, subject.subname asc;'''.format(subject, examgroup)

    cur.execute(query)
    header = (('Student ID', 'Student Name', 'Class', 'Exam Name', 'Subject', 'Marks', 'Total Marks'),)
    d = tuple(cur.fetchall())
    num_of_rows = cur.rowcount
    if num_of_rows == 0:
        print("Data Not Found.\n")
    else:
        retrieve = header + d
        table = tabulate.tabulate(retrieve, tablefmt='fancy_grid')
        print(table, end='\n\n')
    con.close()


# VIEW STUDENT DETAILS TEACHER
def view_studentDetails_teacher(TeacherUser: int):
    con = connect(pswrd=psword)
    cur = con.cursor()
    import tabulate
    counter = 0
    query1 = '''SELECT grade.id,class.division
               FROM grade
               inner join class on class.gradeid=grade.id
               inner join teachersubjectclass on teachersubjectclass.classid=class.id
               inner join teachersubject on teachersubject.subjectid=teachersubjectclass.teachersubjectid
               inner join teacher on Teacher.id=teachersubject.teacherid
               where Teacher.id={}'''
    cur.execute(query1.format(TeacherUser))
    d = cur.fetchall()
    class_ = int(input("Enter class:"))
    division_ = input("Enter division")
    division_upper = division_.upper()
    for i in d:
        if i[0] == class_ and i[1] == division_upper:
            query = '''SELECT student.id, student.name,grade.id,class.division,
                        student.photo,student.gender,
                        student.dateofbirth,student.bloodgroup,student.phoneno,student.address,
                        student.dateofadmission,student.password
                        from student 
                        inner join studentclass on studentclass.studentid=student.id
                        inner join class on class.id=studentclass.classid
                        inner join grade on grade.id=class.gradeid
                        WHERE grade.id={} && class.division='{}'
                        order by student.id'''

            cur.execute(query.format(class_, division_upper))
            header = (('ID', 'Name', 'Class', 'section', 'Photo', 'Gender', 'D.O.B', 'Blood Group', 'Ph.No', 'Address',
                       'Date of admission', 'Password'),)
            d = tuple(cur.fetchall())
            retrieve = header + d
            table = tabulate.tabulate(retrieve, tablefmt='fancy_grid')
            print(table, end="\n\n")
            counter += 1
        else:
            pass
    if counter == 0:
        print("INVALID CLASS/DIVISION", end="\n\n")
    con.close()


# ADD TEST RESULT ADMIN
def add_testResult_admin():
    con = connect(pswrd=psword)
    cur = con.cursor()
    print('''Subjects:
        0. MATHEMATICS 1
        1. SCIENCE
        2. SOCIAL SCIENCE
        3. ENGLISH 1
        4. PHYSICS
        5. CHEMISTRY
        6. MATHEMATICS 2
        7. ENGLISH 2
        8. COMPUTER SCIENCE
        9. BIOLOGY''')
    subject = int(input("Enter subject: ")) + 1
    print('''\nExaminations:
        1. Annual Examination      
        2. Half-Yearly Examination 
        3. Pre-Board 1             
        4. Pre-Board 2             
        5. Quarterly Examination   
        6. Unit Test 1             
        7. Unit Test 2             
        8. Weekly Test''')
    examgroup = int(input("Select exam name:"))
    if examgroup == 1:
        examgroup = 105
    elif examgroup == 2:
        examgroup = 104
    elif examgroup == 3:
        examgroup = 106
    elif examgroup == 4:
        examgroup = 107
    elif examgroup == 5:
        examgroup = 103
    elif examgroup == 6:
        examgroup = 101
    elif examgroup == 7:
        examgroup = 102
    elif examgroup == 8:
        examgroup = 100
    student_id = int(input("Enter Student ID: "))
    q1 = """Select gradeid from class
    Inner join studentclass on studentclass.classid=class.id
    Where studentclass.studentid={};""".format(student_id)
    cur.execute(q1)
    grade = cur.fetchall()
    q2 = "SELECT id FROM exam where gradeid={} && subjectid={} && groupid={};".format(grade,
                                                                                      subject, examgroup)
    cur.execute(q2)
    exam_id = int(cur.fetchall())
    marks = int(input("Enter marks scored: "))
    q3 = "SELECT max(id) from marks;"
    cur.execute(q3)
    s_no = cur.fetchall() + 1
    cur.execute("INSERT INTO marks values({},{},{},{})".format(s_no,
                                                               student_id,
                                                               exam_id,
                                                               marks))
    con.commit()
    print("Successfully added", end="\n\n")
    con.close()


# VIEW ANNOUNCEMENTS ADMIN
def view_announcements_admin():
    con = connect(pswrd=psword)
    cur = con.cursor()
    import tabulate
    query = '''SELECT Announcement.Id, Teacher.Name, Announcement.SubjectPreview, 
                Announcement.AnnouncementDate, 
                Announcement.Attachment
                FROM Announcement
                INNER JOIN Teacher ON Teacher.Id = Announcement.TeacherId
                ORDER BY Announcement.GradeId;'''
    cur.execute(query)
    d = tuple(cur.fetchall())
    header = (('Sn.No', 'Teacher', 'SubjectPreview', 'Date', 'Attachment'),)
    retrieve = header + d
    table = tabulate.tabulate(retrieve, tablefmt='fancy_grid')
    print(table, end="\n\n")
    con.close()


# VIEWING TEACHER DETAILS ADMIN
def view_teacherDetails_admin():
    con = connect(pswrd=psword)
    cur = con.cursor()
    import tabulate
    cur.execute("Select * from teacher")
    header = (("ID", "Name", "Photo", "Ph.No", "D.O.B", "Coordinator", "Ed Qualifications", "Status", "Password"),)
    d = tuple(cur.fetchall())
    retrieve = header + d
    table = tabulate.tabulate(retrieve, tablefmt="fancy_grid")
    print(table, end="\n\n")
    con.close()


# ADDING TEACHER DETAILS ADMIN
def add_teacherDetails_admin():
    con = connect(pswrd=psword)
    cur = con.cursor()
    teacher_id = int(input("Enter teacher id:"))
    name = input("Enter teacher name:")
    photo = input("Enter photo jpg extension:")
    ph_no = int(input("Enter phone number:"))
    date_of_birth = input("Enter date of birth:")
    coordinator = input("Enter coordinator:")
    qualifications = input("Enter ed qualifications:")
    status = input("Enter status:")
    password = input("Enter password:")
    query = "INSERT INTO teacher values({},'{}','{}',{},'{}','{}','{}','{}','{}')"
    cur.execute(query.format(teacher_id, name, photo, ph_no,
                             date_of_birth, coordinator, qualifications,
                             status, password))
    con.commit()
    print("Successfully added", end="\n\n")
    con.close()


# EDIT TEACHER PROFILE ADMIN
def edit_teacherProfile():
    con = connect(pswrd=psword)
    cur = con.cursor()
    teacher_id = int(input("Enter teacher id to update:"))
    print('''What would you like to update:
        1. Name
        2. Photo
        3.Phone Number
        4. Date Of Birth
        5. Is a Co-ordinator?
        6. Educational Qualifications
        7. Status
        8. Password''')
    n = int(input("Enter selection:"))
    if n == 1:
        name = input("Enter teacher name:")
        cur.execute("UPDATE teacher SET name='{}' WHERE id={}".format(name, teacher_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    if n == 2:
        photo = input("Enter photo jpg extension:")
        cur.execute("UPDATE teacher SET photo='{}' WHERE id={}".format(photo, teacher_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    if n == 3:
        ph_no = input("Enter phone number:")
        cur.execute("UPDATE teacher SET phoneno='{}' WHERE id={}".format(ph_no, teacher_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    if n == 4:
        date_of_birth = input("Enter date of birth:")
        cur.execute("UPDATE teacher SET DateOfBirth='{}' WHERE id={}".format(date_of_birth, teacher_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    if n == 5:
        coordinator = input("Enter coordinator:")
        cur.execute("UPDATE teacher SET coordinator='{}' WHERE id={}".format(coordinator, teacher_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    if n == 6:
        EdQualifications = int(input("Enter EdQualifications::"))
        cur.execute("UPDATE teacher SET EdQualifications={} WHERE id={}".format(EdQualifications, teacher_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    if n == 7:
        status = input("Enter status:")
        cur.execute("UPDATE teacher SET status'{}' WHERE id={}".format(status, teacher_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    if n == 8:
        password = input("Enter password:")
        cur.execute("UPDATE teacher SET password='{}' WHERE id={}".format(password, teacher_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    con.close()


# DELETE TEACHER PROFILE ADMIN
def del_teacherProfile():
    con = connect(pswrd=psword)
    cur = con.cursor()
    teacher_id = int(input("Enter Teacher ID:"))
    confirm = input("CONFIRM DELETION(Y/N):").upper()
    if confirm == 'Y':
        cur.execute("DELETE from teacher where id={}".format(teacher_id))
        print("Deletion successful", end="\n\n")
    elif confirm == 'N':
        print("Deletion halted", end="\n\n")
    else:
        print("INVALID OPTION", end="\n\n")
    con.close()


# VIEW STUDENT DETAILS ADMIN
def view_studentDetails_admin():
    con = connect(pswrd=psword)
    cur = con.cursor()
    import tabulate
    query = '''SELECT student.id, student.name,grade.id,class.division,
            student.photo,student.gender,
            student.dateofbirth,student.bloodgroup,student.phoneno,student.address,
            student.dateofadmission,student.password
            from student 
            inner join studentclass on studentclass.studentid=student.id
            inner join class on class.id=studentclass.classid
            inner join grade on grade.id=class.gradeid
            order by student.id'''

    cur.execute(query)
    header = (('ID', 'Name', 'Class', 'section', 'Photo', 'Gender', 'D.O.B', 'Blood Group', 'Ph.No', 'Address',
               'Date of admission', 'Password'),)
    d = tuple(cur.fetchall())
    retrieve = header + d
    table = tabulate.tabulate(retrieve, tablefmt='fancy_grid')
    print(table, end="\n\n")
    con.close()


# ADD STUDENT DETAILS ADMIN
def add_studentDetails_admin():
    con = connect(pswrd=psword)
    cur = con.cursor()
    student_id = int(input("Enter student id:"))
    name = input("Enter student name:")
    class_ = int(input("Enter class: "))
    division = input("Enter division: ")
    photo = input("Enter photo (.jpg extension):")
    gender = input("Enter gender:(M/F):")
    date_of_birth = input("Enter date of birth:")
    blood_group = input("Enter blood group:")
    ph_no = int(input("Enter phone number:"))
    address = input("Enter address:")
    date_of_admission = input("Enter date of admission:")
    password = input("Enter password:")
    q1 = "INSERT INTO student values({},'{}','{}','{}','{}','{}',{},'{}','{}','{}')"
    cur.execute(q1.format(student_id, name, photo,
                          gender, date_of_birth,
                          blood_group, ph_no, address,
                          date_of_admission, password))
    con.commit()
    q2 = "SELECT Id FROM class where GradeId={} && Division='{}'".format(class_, division)
    cur.execute(q2)
    class_id = cur.fetchall()
    q3 = "INSERT INTO studentclass VALUES({}, {})".format(student_id, class_id)
    cur.execute(q3)
    con.commit()
    print("Successfully added", end="\n\n")
    con.close()


# EDIT STUDENT PROFILE ADMIN
def edit_studentProfile_admin():
    con = connect(pswrd=psword)
    cur = con.cursor()
    student_id = int(input("Enter student id:"))
    print('''What would you like to update?
    1. Name
    2. Photo
    3. Gender
    4. Date Of Birth
    5. Blood Group
    6. Phone Number
    7. Address
    8. Password''')
    n = int(input("Enter selection: "))
    if n == 1:
        name = input("Enter student name:")
        cur.execute("UPDATE student SET name='{}' WHERE id={}".format(name, student_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    if n == 2:
        photo = input("Enter photo jpg extension:")
        cur.execute("UPDATE student SET photo='{}' WHERE id={}".format(photo, student_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    if n == 3:
        gender = input("Enter gender(M/F):")
        cur.execute("UPDATE student SET gender='{}' WHERE id={}".format(gender, student_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    if n == 4:
        date_of_birth = input("Enter date of birth:")
        cur.execute("UPDATE student SET DateOfBirth='{}' WHERE id={}".format(date_of_birth, student_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    if n == 5:
        blood_group = input("Enter bloodgroup:")
        cur.execute("UPDATE student SET bloodGroup='{}' WHERE id={}".format(blood_group, student_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    if n == 6:
        ph_no = int(input("Enter phone number:"))
        cur.execute("UPDATE student SET phoneno={} WHERE id={}".format(ph_no, student_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    if n == 7:
        address = input("Enter address:")
        cur.execute("UPDATE student SET address='{}' WHERE id={}".format(address, student_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    if n == 8:
        password = input("Enter password:")
        cur.execute("UPDATE student SET password='{}' WHERE id={}".format(password, student_id))
        con.commit()
        print("Successfully edited", end="\n\n")
    con.close()


# DELETE STUDENT PROFILE ADMIN
def del_studentProfile_admin():
    con = connect(pswrd=psword)
    cur = con.cursor()
    student_id = int(input("Enter student ID:"))
    confirm = input("CONFIRM DELETION(Y/N):").upper()
    if confirm == 'Y':
        cur.execute("DELETE from student where id={}".format(student_id))
        print("Deletion successful", end="\n\n")
    elif confirm == 'N':
        print("Deletion halted", end="\n\n")
    else:
        print("INVALID OPTION", end="\n\n")
    con.close()


# VIEW TEST RESULT ADMIN
def view_testResult_admin():
    con = connect(pswrd=psword)
    cur = con.cursor()
    print('''Subjects:
        0. MATHEMATICS 1
        1. SCIENCE
        2. SOCIAL SCIENCE
        3. ENGLISH 1
        4. PHYSICS
        5. CHEMISTRY
        6. MATHEMATICS 2
        7. ENGLISH 2
        8. COMPUTER SCIENCE
        9. BIOLOGY''')
    subject = int(input("Enter subject: ")) + 1
    print('''\nExaminations:
        1. Annual Examination      
        2. Half-Yearly Examination 
        3. Pre-Board 1             
        4. Pre-Board 2             
        5. Quarterly Examination   
        6. Unit Test 1             
        7. Unit Test 2             
        8. Weekly Test''')
    examgroup = int(input("Select exam name:"))
    import tabulate
    if examgroup == 1:
        examgroup = 105
    elif examgroup == 2:
        examgroup = 104
    elif examgroup == 3:
        examgroup = 106
    elif examgroup == 4:
        examgroup = 107
    elif examgroup == 5:
        examgroup = 103
    elif examgroup == 6:
        examgroup = 101
    elif examgroup == 7:
        examgroup = 102
    elif examgroup == 8:
        examgroup = 100
    query = '''SELECT student.id, student.name, exam.gradeid, examgroup.type, subject.subname, 
    marks.marksscored, exam.maxmark FROM exam INNER JOIN examgroup ON examgroup.id = exam.groupid 
    INNER JOIN subject ON subject.id=exam.subjectid 
    INNER JOIN marks ON marks.examid = exam.id 
    INNER JOIN student ON student.id = marks.studentid 
    WHERE exam.subjectid={} && marks.examid={}
    ORDER BY student.name, exam.gradeid, examgroup.type, subject.subname asc;'''.format(subject, examgroup)

    cur.execute(query)
    header = (('Student ID', 'Student Name', 'Class', 'Exam Name', 'Subject', 'Marks', 'Total Marks'),)
    d = tuple(cur.fetchall())
    num_of_rows = cur.rowcount
    if num_of_rows == 0:
        print("Data Not Found.\n")
    else:
        retrieve = header + d
        table = tabulate.tabulate(retrieve, tablefmt='fancy_grid')
        print(table, end='\n\n')
    con.close()


# VIEW CLASSES ADMIN
def view_classes_admin():
    con = connect(pswrd=psword)
    cur = con.cursor()
    import tabulate
    query = '''SELECT grade.id,class.division
            from grade
            inner join class on class.gradeid=grade.id'''
    cur.execute(query)
    d = tuple(cur.fetchall())
    header = (('Class', 'Division'),)
    retrieve = header + d
    table = tabulate.tabulate(retrieve, tablefmt="fancy_grid")
    print(table, end="\n\n")
    con.close()


# ADD CLASS ADMIN
def add_class_admin():
    con = connect(pswrd=psword)
    cur = con.cursor()
    query1 = '''Select count(*) from class'''
    cur.execute(query1)
    d = cur.fetchall()
    Id = d + 1
    grade_id = int(input("Enter Grade: "))
    division = input("Enter Division:")
    query = '''INSERT INTO class values({},{},'{}')'''
    cur.execute(query.format(Id, grade_id, division))
    con.commit()
    print("Successfully added", end="\n\n")
    con.close()


# VIEW ASSIGNMENT ADMIN
def view_assignment_admin():
    con = connect(pswrd=psword)
    cur = con.cursor()
    import tabulate
    query = '''SELECT Assignment.Id, Assignment.GradeId, Subject.SubName, Teacher.Name, Assignment.Topic, Assignment.StartDate, 
    Assignment.DueDate, Assignment.Attachment 
    FROM Assignment
    INNER JOIN Teacher ON Teacher.Id = Assignment.TeacherId 
    INNER JOIN Subject ON Subject.Id = Assignment.SubjectId 
    ORDER BY Assignment.GradeId; '''
    cur.execute(query)
    header = (("Sn.No.", "Grade", "Subject", "Teacher", "Topic", "StartDate", "DueDate", "Attachment"),)
    d = tuple(cur.fetchall())
    retrieve = header + d
    table = tabulate.tabulate(retrieve, tablefmt="fancy_grid")
    print(table, end="\n\n")
    con.close()
