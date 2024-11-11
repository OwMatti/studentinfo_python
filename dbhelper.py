from sqlite3 import connect, Row

database: str = "studentinfo.db"


def getprocess(sql: str) -> list:
    pass


def get_user(username, password):
    db = connect(database)
    db.row_factory = Row
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
    )
    user = cursor.fetchone()
    db.close()
    return user


def get_students():
    db = connect(database)
    db.row_factory = Row
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    db.close()
    return students


def postprocess(sql: str) -> bool:
    db: object = connect(database)
    cursor: object = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return True if cursor.rowcount > 0 else False


# add record to the def saveinformation()
def add_record(table: str, **kwargs) -> bool:
    keys: list = list(kwargs.keys())
    values: list = list(kwargs.values())
    fld: str = "`,`".join(keys)
    val: str = "','".join(values)
    sql: str = f"INSERT INTO `{table}`(`{fld}`) VALUES('{val}')"
    return postprocess(sql)


# update record
def update_record(table: str, **kwargs) -> bool:
    idno = kwargs.pop("idno")
    update_fields = ", ".join([f"{k}='{v}'" for k, v in kwargs.items()])
    sql = f"UPDATE {table} SET {update_fields} WHERE idno='{idno}'"
    return postprocess(sql)


# delete record
def delete_record(table: str, **kwargs) -> bool:
    conditions = " AND ".join([f"{k}='{v}'" for k, v in kwargs.items()])
    sql = f"DELETE FROM `{table}` WHERE {conditions}"
    return postprocess(sql)
