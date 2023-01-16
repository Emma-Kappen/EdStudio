import mysql.connector as sql


def connect(host: str = 'localhost', user: str = 'root', pswrd: str = 'dpsbn', database: str = 'EdStudio'):
    if database == '':
        con = sql.connect(host=host,
                          user=user,
                          password=pswrd)
    else:
        con = sql.connect(host=host,
                          user=user,
                          password=pswrd,
                          database=database)
    if not con.is_connected():
        print("Connection Error!")
        exit(0)
    else:
        return con


def createDatabase(DBname: str, pswrd: str):
    con = connect(database='', pswrd=pswrd)
    cur = con.cursor()
    q_1 = 'DROP DATABASE IF EXISTS {}'.format(DBname)
    cur.execute(q_1)
    q2 = 'CREATE DATABASE IF NOT EXISTS {}'.format(DBname)
    cur.execute(q2)
    con.commit()
    con.close()


def createParentTable(TbName: str, pswrd: str, Fields_Datatype_Constraints: tuple):
    con = connect(pswrd=pswrd)
    cur = con.cursor()

    q_1 = 'CREATE TABLE {}({})'.format(TbName, Fields_Datatype_Constraints[0])
    cur.execute(q_1)

    for i in Fields_Datatype_Constraints[1:len(Fields_Datatype_Constraints)]:
        q_2 = 'ALTER TABLE {} ADD COLUMN {}'.format(TbName, i)
        cur.execute(q_2)

    con.commit()
    con.close()


def createChildTable(TbName: str, pswrd: str, Field_Datatype_Constraints: tuple, ForeignKey_Requirements: tuple):
    con = connect(pswrd=pswrd)
    cur = con.cursor()
    q = 'CREATE TABLE {}({}'.format(TbName, Field_Datatype_Constraints[0])
    for column in Field_Datatype_Constraints[1:]:
        q = q + ', {}'.format(column)
    try:
        for f_key in ForeignKey_Requirements:
            q = q + ', FOREIGN KEY({}) REFERENCES {}({}) ON DELETE CASCADE ON UPDATE CASCADE'.format(f_key[0], f_key[1],
                                                                                                     f_key[2])
        q = q + ')'
        q = str(q)
        cur.execute(q)
    finally:
        con.commit()
        con.close()


def InsertTbValues(tbname: str, pswrd: str, records: tuple):
    counter = 1
    con = connect(pswrd=pswrd)
    cur = con.cursor()

    if len(records) == 1:
        q1 = 'INSERT INTO {} VALUES('.format(tbname)
        for i in range(len(records)):
            for j in range(len(records[i])):
                if i == 0:
                    if records[i][j] == 'NULL':
                        q1 = q1 + 'NULL'
                    elif records[i][j] == 'default':
                        q1 = q1 + 'default'
                    elif type(records[i][j]) == str:
                        q1 = q1 + "'{}'".format(records[i][j])
                    elif type(records[i][j]) == int or type(records[i][j]) == float:
                        q1 = q1 + '{}'.format(records[i][j])
                else:
                    if records[i][j] == 'NULL':
                        q1 = q1 + ',NULL'
                    elif records[i][j] == 'default':
                        q1 = q1 + ',default'
                    elif type(records[i][j]) == str:
                        q1 = q1 + ",'{}'".format(records[i][j])
                    elif type(records[i][j]) == int or type(records[i][j]) == float:
                        q1 = q1 + ',{}'.format(records[i][j])
        q1 = q1 + ')'

    if len(records) > 1:
        q1 = 'INSERT INTO {} VALUES('.format(tbname)
        for i in range(len(records)):
            for j in range(len(records[i])):
                if j == 0:
                    if records[i][j] == 'NULL':
                        q1 = q1 + 'NULL'
                    elif records[i][j] == 'default':
                        q1 = q1 + 'default'
                    elif type(records[i][j]) == str:
                        q1 = q1 + "'{}'".format(records[i][j])
                    elif type(records[i][j]) == int or type(records[i][j]) == float:
                        q1 = q1 + '{}'.format(records[i][j])
                else:
                    if records[i][j] == 'NULL':
                        q1 = q1 + ',NULL'
                    elif records[i][j] == 'default':
                        q1 = q1 + ',default'
                    elif type(records[i][j]) == str:
                        q1 = q1 + ",'{}'".format(records[i][j])
                    elif type(records[i][j]) == int or type(records[i][j]) == float:
                        q1 = q1 + ',{}'.format(records[i][j])
            counter += 1
            if counter <= len(records):
                q1 = q1 + '),('
        q1 = q1 + ')'
    cur.execute(q1)
    con.commit()
    con.close()
