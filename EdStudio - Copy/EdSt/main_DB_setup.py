import Functions_DB_setup as db_s

pswrd = input("Enter the database password: ")



# Creating EdStudio Database
db_s.createDatabase('EdStudio', pswrd)

# Creating Admin Table
db_s.createParentTable('Admin', pswrd,
                       ('Id int not null unique primary key',
                        'Password varchar(20) default("admin")'))

# Creating Student Table
db_s.createParentTable('Student', pswrd,
                       ('Id int not null unique primary key',
                        'Name varchar(80) not null',
                        'Photo blob default("https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1")',
                        'Gender char(1)',
                        'DateOfBirth date not null',
                        'BloodGroup char(3)',
                        'PhoneNo varchar(10) not null',
                        'Address blob not null',
                        'DateOfAdmission date not null',
                        'Password varchar(20) default("edstudio")'))

# Creating Guardian Table
db_s.createParentTable('Guardian', pswrd,
                       ('Id int not null unique primary key',
                        'Name varchar(80) not null',
                        'Photo blob default("https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1")',
                        'PhoneNo varchar(10) not null unique',
                        'Address blob not null',
                        'EmailAddress varchar(80) unique'))

# Creating StudentGuardianRealtionship Table
db_s.createParentTable('Relationship', pswrd,
                       ('Id int not null unique primary key',
                        'Type varchar(45) not null unique'))

# Creatiing Teacher Table
db_s.createParentTable('Teacher', pswrd,
                       ('Id int not null unique primary key',
                        'Name varchar(80) not null',
                        'Photo blob default("https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1")',
                        'PhoneNo varchar(10) not null',
                        'DateOfBirth date not null',
                        "Coordinator char(1) not null default('F')",
                        'EdQualifications varchar(255)',
                        "Status char(8) not null default('EMPLOYEE')",
                        'Password varchar(20) default(NULL)'))

# Creating Subject Table
db_s.createParentTable('Subject', pswrd,
                       ('Id int not null unique primary key',
                        'SubName varchar(25) not null unique'))

# Creating Grade Table
db_s.createParentTable('Grade', pswrd,
                       ('Id int not null unique primary key',))

# Creating ExamGroup Table
db_s.createParentTable('ExamGroup', pswrd,
                       ('Id int not null unique primary key',
                        'Type varchar(60) not null unique'))

# Creating Class Table
db_s.createChildTable('Class', pswrd,
                      ('Id int not null unique primary key',
                       'GradeId int not null',
                       'Division char(1) not null'),
                      (('GradeId', 'Grade', 'Id'),))

# Creating Exam Table
db_s.createChildTable('Exam', pswrd,
                      ('Id int not null unique primary key',
                       'GroupId int not null',
                       'SubjectId int not null',
                       'GradeId int not null',
                       'Date date not null',
                       'Maxmark decimal(5,2) unsigned'),
                      (('GroupId', 'ExamGroup', 'Id'),
                       ('SubjectId', 'Subject', 'Id'),
                       ('GradeId', 'Grade', 'Id')))

# Creating StudentGuardianRelationship Table
db_s.createChildTable('StudGuardRelate', pswrd,
                      ('StudentId int not null',
                       'GuardianId int not null',
                       'RelationshipId int'),
                      (('StudentId', 'Student', 'Id'),
                       ('GuardianId', 'Guardian', 'Id'),
                       ('RelationshipId', 'Relationship', 'Id')))

# Creating TeacherSubject Table
db_s.createChildTable('TeacherSubject', pswrd,
                      ('Id int not null unique primary key',
                       'TeacherId int not null',
                       'SubjectId int not null'),
                      (('TeacherId', 'Teacher', 'Id'),
                       ('SubjectId', 'Subject', 'Id')))

# Creating StudentClass Table
db_s.createChildTable('StudentClass', pswrd,
                      ('StudentId int not null',
                       'ClassId int not null'),
                      (('StudentId', 'Student', 'Id'),
                       ('ClassId', 'Class', 'Id')))

# Creating TeacherSubjectClass Table
db_s.createChildTable('TeacherSubjectClass', pswrd,
                      ('TeacherSubjectId int not null',
                       'ClassId int not null'),
                      (('TeacherSubjectId', 'TeacherSubject', 'Id'),
                       ('ClassId', 'Class', 'Id')))

# Creating Marks Table
db_s.createChildTable('Marks', pswrd,
                      ('Id int unique not null primary key',
                       'StudentId int not null',
                       'ExamId int not null',
                       'MarksScored decimal(5,2)'),
                      (('StudentId', 'Student', 'Id'),
                       ('ExamId', 'Exam', 'Id')))

# Creating Assignment Table
db_s.createChildTable('Assignment', pswrd,
                      ('Id int not null unique primary key',
                       'TeacherId int not null',
                       'GradeId int not null',
                       'SubjectId int not null',
                       'Topic varchar(100) not null',
                       'StartDate date not null',
                       'DueDate date not null',
                       'Attachment blob'),
                      (('TeacherId', 'Teacher', 'Id'),
                       ('SubjectId', 'Subject', 'Id')))

# Creating Announcement Table
db_s.createChildTable('Announcement', pswrd,
                      ('Id int not null unique primary key',
                       'GradeId int not null',
                       'TeacherId int not null',
                       'AnnouncementDate date not null',
                       'SubjectPreview varchar(255) default(null)',
                       'Attachment blob default(null)'),
                      (('TeacherId', 'Teacher', 'Id'),
                       ('GradeId', 'Grade', 'Id')))

# Admin Table Values
db_s.InsertTbValues('Admin', pswrd,
                    ((10, 'admin'),
                     (11, 'admin')))

# Student Table Values
# 1-10
db_s.InsertTbValues('Student', pswrd,
                    ((11001, 'SName01',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2004-01-01', 'O+', 9876543201, 'Address1', '2018-01-01', 'edstudio'),
                     (11002, 'SName02',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2005-01-01', 'O+', 9876543202, 'Address2', '2019-01-01', 'edstudio'),
                     (11003, 'SName03',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2006-01-01', 'O+', 9876543203, 'Address3', '2020-01-01', 'edstudio'),
                     (11004, 'SName04',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2007-01-01', 'O+', 9876543204, 'Address4', '2021-01-01', 'edstudio'),
                     (11005, 'SName05',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2008-01-01', 'O+', 9876543205, 'Address5', '2022-01-01', 'edstudio'),
                     (11006, 'SName06',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2004-01-01', 'O+', 9876543206, 'Address6', '2018-01-01', 'edstudio'),
                     (11007, 'SName07',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2005-01-01', 'O+', 9876543207, 'Address7', '2019-01-01', 'edstudio'),
                     (11008, 'SName08',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2006-01-01', 'O+', 9876543208, 'Address8', '2020-01-01', 'edstudio'),
                     (11009, 'SName09',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2007-01-01', 'O+', 9876543209, 'Address9', '2021-01-01', 'edstudio'),
                     (11010, 'SName10',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2008-01-01', 'O+', 9876543210, 'Address10', '2022-01-01', 'edstudio')))
# 11-20
db_s.InsertTbValues('Student', pswrd,
                    ((11011, 'SName11',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2004-01-01', 'O+', 9876543211, 'Address11', '2018-01-01', 'edstudio'),
                     (11012, 'SName12',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2005-01-01', 'O+', 9876543212, 'Address12', '2019-01-01', 'edstudio'),
                     (11013, 'SName13',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2006-01-01', 'O+', 9876543213, 'Address13', '2020-01-01', 'edstudio'),
                     (11014, 'SName14',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2007-01-01', 'O+', 9876543214, 'Address14', '2021-01-01', 'edstudio'),
                     (11015, 'SName15',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2008-01-01', 'O+', 9876543215, 'Address15', '2022-01-01', 'edstudio'),
                     (11016, 'SName16',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2004-01-01', 'O+', 9876543216, 'Address16', '2018-01-01', 'edstudio'),
                     (11017, 'SName17',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2005-01-01', 'O+', 9876543217, 'Address17', '2019-01-01', 'edstudio'),
                     (11018, 'SName18',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2006-01-01', 'O+', 9876543218, 'Address18', '2020-01-01', 'edstudio'),
                     (11019, 'SName19',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2007-01-01', 'O+', 9876543219, 'Address19', '2021-01-01', 'edstudio'),
                     (11020, 'SName20',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2008-01-01', 'O+', 9876543220, 'Address20', '2022-01-01', 'edstudio')))
# 21-30
db_s.InsertTbValues('Student', pswrd,
                    ((11021, 'SName21',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2004-01-01', 'O+', 9876543221, 'Address21', '2018-01-01', 'edstudio'),
                     (11022, 'SName22',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2005-01-01', 'O+', 9876543222, 'Address22', '2019-01-01', 'edstudio'),
                     (11023, 'SName23',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2006-01-01', 'O+', 9876543223, 'Address23', '2020-01-01', 'edstudio'),
                     (11024, 'SName24',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2007-01-01', 'O+', 9876543224, 'Address24', '2021-01-01', 'edstudio'),
                     (11025, 'SName25',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2008-01-01', 'O+', 9876543225, 'Address25', '2022-01-01', 'edstudio'),
                     (11026, 'SName26',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2004-01-01', 'O+', 9876543226, 'Address26', '2018-01-01', 'edstudio'),
                     (11027, 'SName27',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2005-01-01', 'O+', 9876543227, 'Address27', '2019-01-01', 'edstudio'),
                     (11028, 'SName28',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2006-01-01', 'O+', 9876543228, 'Address28', '2020-01-01', 'edstudio'),
                     (11029, 'SName29',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2007-01-01', 'O+', 9876543229, 'Address29', '2021-01-01', 'edstudio'),
                     (11030, 'SName30',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2008-01-01', 'O+', 9876543230, 'Address30', '2022-01-01', 'edstudio')))
# 31-40
db_s.InsertTbValues('Student', pswrd,
                    ((11031, 'SName31',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2004-01-01', 'O+', 9876543231, 'Address31', '2018-01-01', 'edstudio'),
                     (11032, 'SName32',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2005-01-01', 'O+', 9876543232, 'Address32', '2019-01-01', 'edstudio'),
                     (11033, 'SName33',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2006-01-01', 'O+', 9876543233, 'Address33', '2020-01-01', 'edstudio'),
                     (11034, 'SName34',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2007-01-01', 'O+', 9876543234, 'Address34', '2021-01-01', 'edstudio'),
                     (11035, 'SName35',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2008-01-01', 'O+', 9876543235, 'Address35', '2022-01-01', 'edstudio'),
                     (11036, 'SName36',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2004-01-01', 'O+', 9876543236, 'Address36', '2018-01-01', 'edstudio'),
                     (11037, 'SName37',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2005-01-01', 'O+', 9876543237, 'Address37', '2019-01-01', 'edstudio'),
                     (11038, 'SName38',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2006-01-01', 'O+', 9876543238, 'Address38', '2020-01-01', 'edstudio'),
                     (11039, 'SName39',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'F', '2007-01-01', 'O+', 9876543239, 'Address39', '2021-01-01', 'edstudio'),
                     (11040, 'SName40',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      'M', '2008-01-01', 'O+', 9876543240, 'Address40', '2022-01-01', 'edstudio')))


# Guardian Table Values
# 1-10
db_s.InsertTbValues('Guardian', pswrd,
                    ((10001, 'GName1',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450001, 'Address1', 'gname1@gmail.com'),
                     (10002, 'GName2',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450002, 'Address2', 'gname2@gmail.com'),
                     (10003, 'GName3',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450003, 'Address3', 'gname3@gmail.com'),
                     (10004, 'GName4',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450004, 'Address4', 'gname4@gmail.com'),
                     (10005, 'GName5',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450005, 'Address5', 'gname5@gmail.com'),
                     (10006, 'GName6',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450006, 'Address6', 'gname6@gmail.com'),
                     (10007, 'GName7',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450007, 'Address7', 'gname7@gmail.com'),
                     (10008, 'GName8',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450008, 'Address8', 'gname8@gmail.com'),
                     (10009, 'GName9',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450009, 'Address9', 'gname9@gmail.com'),
                     (10010, 'GName10',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450010, 'Address10', 'gname10@gmail.com')))

# 11-20
db_s.InsertTbValues('Guardian', pswrd,
                    ((10011, 'GName11',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450011, 'Address1', 'gname11@gmail.com'),
                     (10012, 'GName12',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450012, 'Address2', 'gname12@gmail.com'),
                     (10013, 'GName13',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450013, 'Address3', 'gname13@gmail.com'),
                     (10014, 'GName14',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450014, 'Address4', 'gname14@gmail.com'),
                     (10015, 'GName15',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450015, 'Address5', 'gname15@gmail.com'),
                     (10016, 'GName16',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450016, 'Address6', 'gname16@gmail.com'),
                     (10017, 'GName17',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450017, 'Address7', 'gname17@gmail.com'),
                     (10018, 'GName18',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450018, 'Address8', 'gname18@gmail.com'),
                     (10019, 'GName19',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450019, 'Address9', 'gname19@gmail.com'),
                     (10020, 'GName20',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9123450020, 'Address10', 'gname20@gmail.com')))

# GuardianRelationship Table Values
db_s.InsertTbValues('Relationship', pswrd,
                    ((10, 'Father'),
                     (11, 'Mother'),
                     (12, 'Sibling'),
                     (13, 'Grand Parent'),
                     (14, 'Guardian'),
                     (15, 'Local Guardian'),
                     (16, 'Relative'),
                     (17, 'Other')))

# Teacher Table Values
# 1-10
db_s.InsertTbValues('Teacher', pswrd,
                    ((101, 'TName1',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9213450001, '1992-01-01', 'F', 'B.Ed.', 'Employee', 'edstudio'),
                     (102, 'TName2',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9213450002, '1991-01-01', 'F', 'B.Ed., B.Sc.', 'Contract', 'edstudio'),
                     (103, 'TName3',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9213450003, '1990-01-01', 'F', 'B.Ed.', 'Contract', 'edstudio'),
                     (104, 'TName4',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9213450004, '1989-01-01', 'F', 'B.Ed., B.Sc.', 'Employee', 'edstudio'),
                     (105, 'TName5',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9213450005, '1988-01-01', 'F', 'B.Ed.', 'Contract', 'edstudio'),
                     (106, 'TName6',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9213450006, '1987-01-01', 'F', 'B.Ed., B.Sc.', 'Employee', 'edstudio'),
                     (107, 'TName7',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9213450007, '1986-01-01', 'T', 'B.Ed.', 'Contract', 'edstudio'),
                     (108, 'TName8',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9213450008, '1985-01-01', 'T', 'B.Ed., B.Sc.', 'Employee', 'edstudio'),
                     (109, 'TName9',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9213450009, '1984-01-01', 'T', 'B.Ed.', 'Contract', 'edstudio'),
                     (110, 'TName10',
                      'https://i0.wp.com/www.dc-hauswartungen.ch/wp-content/uploads/2018/01/dummy_profile.png?ssl=1',
                      9213450010, '1983-01-01', 'T', 'B.Ed., B.Sc.', 'Employee', 'edstudio'),
                     (12, 'Admin',
                      '', 1000000000, '1900-01-01', 'T', '-', 'Employee', 'admin')))

# Subject Table Values
db_s.InsertTbValues('Subject', pswrd,
                    ((1, 'Mathematics 1'),
                     (2, 'Science'),
                     (3, 'Social Science'),
                     (4, 'English 1'),
                     (5, 'Physics'),
                     (6, 'Chemistry'),
                     (7, 'Mathematics 2'),
                     (8, 'English 2'),
                     (9, 'Computer Science'),
                     (10, 'Biology')))

# Grade Table Values
db_s.InsertTbValues('Grade', pswrd,
                    ((9,),
                     (10,),
                     (11,),
                     (12,)))

# ExamGroup Table Values
db_s.InsertTbValues('ExamGroup', pswrd,
                    ((100, 'Weekly Test'),
                     (101, 'Unit Test 1'),
                     (102, 'Unit Test 2'),
                     (103, 'Quarterly Examination'),
                     (104, 'Half-Yearly Examination'),
                     (105, 'Annual Examination'),
                     (106, 'Pre-Board 1'),
                     (107, 'Pre-Board 2')))

# Class Table Values
db_s.InsertTbValues('Class', pswrd,
                    ((1, 9, 'A'),
                     (2, 9, 'B'),
                     (3, 10, 'A'),
                     (4, 10, 'B'),
                     (5, 11, 'A'),
                     (6, 11, 'B'),
                     (7, 12, 'A'),
                     (8, 12, 'B')))

# Exam Table Values
db_s.InsertTbValues('Exam', pswrd,
                    ((101, 101, 5, 12, '2022-01-01', 50),
                     (102, 101, 6, 12, '2022-01-02', 50),
                     (103, 101, 7, 12, '2022-01-03', 50),
                     (104, 101, 8, 12, '2022-01-04', 50),
                     (105, 101, 9, 12, '2022-01-05', 50),
                     (106, 101, 10, 12, '2022-01-06', 50)))

# StudentGuardianRelationship Table Values
db_s.InsertTbValues('StudGuardRelate', pswrd,
                    ((11001, 10001, 10),
                     (11002, 10001, 10),
                     (11003, 10002, 11),
                     (11004, 10002, 11),
                     (11005, 10003, 12),
                     (11006, 10003, 12),
                     (11007, 10004, 13),
                     (11008, 10004, 13),
                     (11009, 10005, 14),
                     (11010, 10005, 14),
                     (11011, 10006, 15),
                     (11012, 10006, 15),
                     (11013, 10007, 16),
                     (11014, 10007, 16),
                     (11015, 10008, 10),
                     (11016, 10008, 10),
                     (11017, 10009, 11),
                     (11018, 10009, 11),
                     (11019, 10010, 12),
                     (11020, 10010, 12),
                     (11021, 10011, 13),
                     (11022, 10011, 13),
                     (11023, 10012, 14),
                     (11024, 10012, 14),
                     (11025, 10013, 15),
                     (11026, 10013, 15),
                     (11027, 10014, 16),
                     (11028, 10014, 16),
                     (11029, 10015, 10),
                     (11030, 10015, 10),
                     (11031, 10016, 11),
                     (11032, 10016, 11),
                     (11033, 10017, 12),
                     (11034, 10017, 12),
                     (11035, 10018, 13),
                     (11036, 10018, 13),
                     (11037, 10019, 14),
                     (11038, 10019, 14),
                     (11039, 10020, 15),
                     (11040, 10020, 15)))

# TeacherSubject Table Values
db_s.InsertTbValues('TeacherSubject', pswrd,
                    ((1, 101, 1),
                     (2, 102, 2),
                     (3, 103, 3),
                     (4, 104, 4),
                     (5, 105, 5),
                     (6, 106, 6),
                     (7, 107, 7),
                     (8, 108, 8),
                     (9, 109, 9),
                     (10, 110, 10),
                     (11, 104, 3),
                     (12, 12, 1),
                     (13, 12, 2),
                     (14, 12, 3),
                     (15, 12, 4),
                     (16, 12, 5),
                     (17, 12, 6),
                     (18, 12, 7),
                     (19, 12, 8),
                     (20, 12, 9),
                     (21, 12, 10)))

# StudentClass Table Values
# Class 12 A & B
db_s.InsertTbValues('StudentClass', pswrd,
                    ((11001, 7),
                     (11036, 7),
                     (11016, 7),
                     (11011, 7),
                     (11021, 7),
                     (11006, 8),
                     (11026, 8),
                     (11031, 8),
                     (11002, 8),
                     (11007, 8)))
# Class 11 A & B
db_s.InsertTbValues('StudentClass', pswrd,
                    ((11012, 5),
                     (11017, 5),
                     (11022, 5),
                     (11027, 5),
                     (11032, 5),
                     (11037, 6),
                     (11003, 6),
                     (11008, 6),
                     (11013, 6),
                     (11018, 6)))
# Class 10 A & B
db_s.InsertTbValues('StudentClass', pswrd,
                    ((11028, 3),
                     (11023, 3),
                     (11033, 3),
                     (11038, 3),
                     (11004, 3),
                     (11009, 4),
                     (11014, 4),
                     (11019, 4),
                     (11029, 4),
                     (11034, 4)))
# Class 9 A & B
db_s.InsertTbValues('StudentClass', pswrd,
                    ((11024, 1),
                     (11039, 1),
                     (11005, 1),
                     (11010, 1),
                     (11015, 1),
                     (11020, 2),
                     (11025, 2),
                     (11030, 2),
                     (11035, 2),
                     (11040, 2)))

# TeacherSubjectClass Table Values
db_s.InsertTbValues('TeacherSubjectClass', pswrd,
                    ((1, 1), (2, 1), (3, 1), (4, 1),
                     (1, 2), (2, 2), (3, 2), (4, 2),
                     (1, 3), (2, 3), (3, 3), (4, 3),
                     (1, 4), (2, 4), (3, 4), (4, 4),
                     (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
                     (5, 6), (6, 6), (7, 6), (8, 6), (10, 6),
                     (5, 7), (6, 7), (7, 7), (8, 7), (9, 7),
                     (5, 8), (6, 8), (7, 8), (8, 8), (10, 8),))

# Marks Table Values
# For class 12 A
db_s.InsertTbValues('Marks', pswrd,
                    ((11, 11001, 101, 26),
                     (12, 11001, 102, 27),
                     (13, 11001, 103, 28),
                     (14, 11001, 104, 29),
                     (15, 11001, 105, 30),
                     (16, 11036, 101, 31),
                     (17, 11036, 102, 32),
                     (18, 11036, 103, 33),
                     (19, 11036, 104, 34),
                     (20, 11036, 105, 35),
                     (21, 11016, 101, 36),
                     (22, 11016, 102, 37),
                     (23, 11016, 103, 38),
                     (24, 11016, 104, 39),
                     (25, 11016, 105, 40),
                     (26, 11011, 101, 41),
                     (27, 11011, 102, 42),
                     (28, 11011, 103, 43),
                     (29, 11011, 104, 44),
                     (30, 11011, 105, 45),
                     (31, 11021, 101, 46),
                     (32, 11021, 102, 47),
                     (33, 11021, 103, 48),
                     (34, 11021, 104, 49),
                     (35, 11021, 105, 50)))
# For class 12 B
db_s.InsertTbValues('Marks', pswrd,
                    ((36, 11006, 101, 46),
                     (37, 11006, 102, 47),
                     (38, 11006, 103, 48),
                     (39, 11006, 104, 49),
                     (40, 11006, 106, 40),
                     (41, 11026, 101, 41),
                     (42, 11026, 102, 42),
                     (43, 11026, 103, 43),
                     (44, 11026, 104, 44),
                     (45, 11026, 106, 45),
                     (46, 11031, 101, 46),
                     (47, 11031, 102, 47),
                     (48, 11031, 103, 48),
                     (49, 11031, 104, 49),
                     (50, 11031, 106, 40),
                     (51, 11002, 101, 41),
                     (52, 11002, 102, 42),
                     (53, 11002, 103, 43),
                     (54, 11002, 104, 44),
                     (55, 11002, 106, 45),
                     (56, 11007, 101, 56),
                     (57, 11007, 102, 57),
                     (58, 11007, 103, 58),
                     (59, 11007, 104, 59),
                     (60, 11007, 106, 50),))

# Assignment Table Values
db_s.InsertTbValues('Assignment', pswrd,
                    ((1, 101, 9, 1, 'Linear Equations WS', '2022-07-01', '2022-08-01',
                      'https://data.templateroller.com/pdf_docs_html/167/1671/167137/algebra-2-wkst-3-5-3-7-linear-equations-in-slope-intercept-form-worksheet-with-answers_print_big.png'),
                     (2, 106, 11, 6, 'Nomenclature of Organic Compounds WS', '2022-07-02', '2022-08-01',
                      'https://i.pinimg.com/236x/9f/d9/2a/9fd92a1ac9d20a03a650fef71252d169--ap-chemistry-level-.jpg'),
                     (3, 110, 12, 10, 'Principles of Inheritance and Variation WS', '2022-07-03', '2022-08-02',
                      'https://i0.wp.com/www.worksheeto.com/postpic/2012/04/ap-biology-chapter-16-guided-reading-assignment-answers_206593.png')))

# Announcement Table Values
db_s.InsertTbValues('Announcement', pswrd,
                    ((1, 11, 109, '2022-07-20',
                      'A trek will be organised for all students of grade 11. \nInterested students may ask the CT for more details.',
                      'NULL'),
                     (2, 12, 110, '2022-07-19',
                      'A trek will be organised for all students of grade 12. \nInterested students may ask the CT for more details.',
                      'NULL')))
