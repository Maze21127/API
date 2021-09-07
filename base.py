import pymysql
from student import Student
from main import update


class MySQL:
    def __init__(self, host, port, user, password, database):
        try:
            self.connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Подключение успешно")
            self.cursor = self.connection.cursor()
            print('Курсор получен успешно')
            try:
                self.db = self.get_data()
                self.cache_db = self.get_student_set()
            finally:
                self.connection.close()
                print('Соединение закрыто')
        except Exception as ex:
            print(ex)

    def insert_data(self, stud):
        self.connection.ping()
        insert_query = f"REPLACE INTO students (place, snils, accept, payment, benefits, total_score," \
                       f" first_obj, second_obj, third_obj) VALUES (" \
                       f"{stud.place}, '{stud.snils}', '{stud.accept}', '{stud.payment}', '{stud.benefits}', " \
                       f"{stud.total_score}, '{stud.first_obj}', '{stud.second_obj}', '{stud.third_obj}'" \
                       f")"
        print(insert_query)
        self.cursor.execute(insert_query)
        self.connection.commit()

    def get_data(self):
        self.cursor.execute("SELECT * FROM students ORDER BY place")
        return tuple(self.cursor.fetchall())

    def update_bd(self):
        self.cursor.execute("SELECT * FROM students ORDER BY place")
        self.db = self.cursor.fetchall()

    def print_data(self):
        for row in self.db:
            print(row)

    def get_best(self, number=1):
        return self.db[0:number]

    def get_last(self, number=-1):
        return self.db[-number:]

    def get_place(self, score):
        bd_len = len(self.db)
        mid = bd_len // 2
        low = 0
        high = bd_len - 1
        while self.db[mid]['total_score'] != score and low <= high:
            if score < self.db[mid]['total_score']:
                low = mid + 1
            else:
                high = mid - 1
            mid = (low + high) // 2
        if low > high:
            return mid + 2
        else:
            return mid + 1

    def find_snils(self, snils: str) -> dict:
        for stud in self.db:
            if stud['snils'] == snils:
                return stud

    def get_student_set(self):
        students_set = list()
        for i in self.db:
            stud = Student(
                i['place'],
                i['snils'].strip(),
                i['accept'].strip(),
                i['payment'].strip(),
                i['benefits'].strip(),
                i['total_score'],
                i['first_obj'].strip(),
                i['second_obj'].strip(),
                i['third_obj'].strip())
            students_set.append(stud)
        return list(students_set)

    def is_new(self):
        temp = update()
        if temp == self.cache_db:
            print('Изменений нет')
        else:
            #print(temp - self.cache_bd)
            print(temp[0])
            print(self.cache_db[0])
            print('Изменения есть')


sql = MySQL(host='localhost', port=3306, user='admin', password='zxcdewqas322', database='myapi')
sql.is_new()
