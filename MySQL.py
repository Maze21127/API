import pymysql
from student import Student


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
                self.db = self.get_data_from_db()
                self.cache_db = list(self.db)
            finally:
                self.connection.close()
                print('Соединение закрыто')
        except Exception as ex:
            print(ex)

    def insert_data(self, stud):
        self.connection.ping()
        insert_query = f"REPLACE INTO students (place, snils, accept, payment, benefits, total_score," \
                       f" first_obj, second_obj, third_obj) VALUES (" \
                       f"{stud['place']}," \
                       f"'{stud['snils']}'," \
                       f"'{stud['accept']}'," \
                       f"'{stud['payment']}'," \
                       f"'{stud['benefits']}', " \
                       f"{stud['total_score']}," \
                       f"'{stud['first_obj']}'," \
                       f"'{stud['second_obj']}', " \
                       f"'{stud['third_obj']}'" \
                       f")"
        print(insert_query)
        self.cursor.execute(insert_query)
        self.connection.commit()

    def delete_stud(self, stud):
        self.connection.ping()
        insert_query = f"DELETE FROM students WHERE snils='{stud['snils']}'"
        self.cursor.execute(insert_query)
        self.connection.commit()

    def delete_stud_snils(self, snils):
        self.connection.ping()
        insert_query = f"DELETE FROM students WHERE snils='{snils}'"
        self.cursor.execute(insert_query)
        self.connection.commit()

    def get_data_from_db(self):
        self.cursor.execute("SELECT * FROM students ORDER BY place")
        return tuple(self.cursor.fetchall())

    def update_bd(self):
        self.cursor.execute("SELECT * FROM students ORDER BY place")
        self.db = self.cursor.fetchall()
        self.cache_db = list(self.db)

    def print_data(self):
        for row in self.db:
            print(row)

    def get_best(self, number=1):
        return self.db[0:number]

    def get_last(self, number=-1):
        if number != -1:
            return self.db[-number:]
        return self.db[number:]

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
        students_set = []
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
        #print(students_set)
        return students_set

    def is_new(self):
        temp = Student.get_students_dict()
        if temp != self.cache_db:
            print("Есть изменения")
            diff_to_insert = [item for item in temp if item not in self.cache_db]
            diff_to_delete = [item for item in self.cache_db if item not in temp]
            print(len(diff_to_delete))
            for i in diff_to_insert:
                self.insert_data(i)
            for i in diff_to_delete:
                self.delete_stud(i)
            self.update_bd()
        else:
            print("Изменений нет")

