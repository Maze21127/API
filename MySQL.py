import pymysql
from vvsu_parse import VVSU_Parse
from random import choice
import time


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
            self.cursor = self.connection.cursor()
            try:
                self.db = self.get_data_from_db()
            finally:
                self.connection.close()
                print('Соединение закрыто')
        except Exception as ex:
            print(ex)

    def insert_data(self, stud):
        self.connection.ping()
        insert_query = f"REPLACE INTO students (place, snils, accept, payment, benefits, total_score," \
                       f" first_obj, second_obj, third_obj, achievements) VALUES (" \
                       f"{stud['place']}," \
                       f"'{stud['snils']}'," \
                       f"'{stud['accept']}'," \
                       f"'{stud['payment']}'," \
                       f"'{stud['benefits']}', " \
                       f"{stud['total_score']}," \
                       f"'{stud['first_obj']}'," \
                       f"'{stud['second_obj']}', " \
                       f"'{stud['third_obj']}', " \
                       f"{stud['achievements']}" \
                       f")"
        print(insert_query)
        self.cursor.execute(insert_query)
        self.connection.commit()
        #print(f'{insert_query} success!')

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
        return list(self.cursor.fetchall())

    def update_bd(self):
        self.cursor.execute("SELECT * FROM students ORDER BY place")
        self.db = self.cursor.fetchall()

    def print_data(self):
        for row in self.db:
            print(row)

    def get_best(self, number=1):
        return self.db[0:number]

    def get_random(self, number=1):
        return [choice(self.db) for _ in range(number)]

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
            return {"place": mid + 2}
        else:
            return {"place": mid + 1}

    def find_student_by_snils(self, snils: str):
        for stud in self.db:
            if stud['snils'] == snils:
                return stud
        return f'Student not found'

    def find_student_by_place(self, place: int):
        for stud in self.db:
            if stud['place'] == place:
                return stud
        return f'Student not found'

    def is_new(self):
        start = time.time()
        vvsu = VVSU_Parse()
        vvsu.update()
        temp = vvsu.get_students_list()
        if temp != self.db:
            print("Есть изменения")
            diff_to_insert = [item for item in temp if item not in self.db]
            diff_to_delete = [item for item in self.db if item not in temp]
            for i in diff_to_insert:
                self.insert_data(i)
            for i in diff_to_delete:
                self.delete_stud(i)
            self.update_bd()
            return "Database is Updated"
        else:
            return "Database has no changes"
