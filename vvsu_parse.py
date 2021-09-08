import threading
import requests
from bs4 import BeautifulSoup


class VVSU_Parse:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.8.1.468 Yowser/2.5 Safari/537.36',
            'accept': '*/*'
        }
        self.url = 'https://www.vvsu.ru/controller/elementLoad.php'
        self.all_data = []

    def get_soup(self, page):
        data = {
            'GetInfoBlock': '{"filters":[{"id":"604734","value":41,"label":"Высшее образование  - Бакалавриат "},'
                            '{"id":"604735","value":1,"label":"очная "},'
                            '{"id":"631093","value":892,"label":"Информационные системы и технологии "},'
                            '{"id":"631098","value":2169,"label":"09.03.02 Информационные системы и технологии "},'
                            '{"id":"631383","value":11507,"label":"Институт информационных технологий "}],'
                            '"filterDates":[]}',
            'url': f'https://www.vvsu.ru/enter/order/page/{page}/',
            'element': '2149012088',
            'clearPager': 'True'
        }
        html = requests.post(url=self.url, headers=self.headers, data=data)
        html.encoding = 'utf-8'
        self.all_data.append(html.text)

    def get_pagination(self):
        data = {
            'GetInfoBlock': '{"filters":[{"id":"604734","value":41,"label":"Высшее образование  - Бакалавриат "},'
                            '{"id":"604735","value":1,"label":"очная "},'
                            '{"id":"631093","value":892,"label":"Информационные системы и технологии "},'
                            '{"id":"631098","value":2169,"label":"09.03.02 Информационные системы и технологии "},'
                            '{"id":"631383","value":11507,"label":"Институт информационных технологий "}],'
                            '"filterDates":[]}',
            'url': f'https://www.vvsu.ru/enter/order/page/{1}/',
            'element': '2149012088',
            'clearPager': 'True'
        }
        html = requests.post(url=self.url, headers=self.headers, data=data)
        html.encoding = 'utf-8'
        soup_obj = BeautifulSoup(html.text, 'lxml')
        test = soup_obj.find(class_="pagination").find_all('li')
        url = test[-1].find('a').get('href')
        return int(url[url.find('page/') + 5:-1])

    @staticmethod
    def get_students(data):
        st = []
        soup = BeautifulSoup(data, 'lxml')
        soup_obj = soup.find_all(style=["background:#F6F6F6; !important;", "background:#C1E0C1; !important;"])
        for student in soup_obj:
            student_td = student.find_all('td')
            student_td = list(map(lambda x: x.text.strip(), student_td))
            my_student = dict()
            my_student['place'] = int(student_td[0])
            my_student['snils'] = student_td[1]
            my_student['accept'] = student_td[2]
            my_student['payment'] = student_td[3]
            my_student['benefits'] = student_td[4]
            my_student['total_score'] = int(student_td[5])
            my_student['first_obj'] = student_td[6]
            my_student['second_obj'] = student_td[7]
            my_student['third_obj'] = student_td[8]
            my_student['achievements'] = student_td[9]
            if my_student['achievements'] == "":
                my_student['achievements'] = 0
            else:
                my_student['achievements'] = int(student_td[9])
            st.append(my_student)
        return st

    def get_all_data(self):
        thread_list = []
        pages = self.get_pagination()
        for page in range(1, pages + 1):
            thread = threading.Thread(target=self.get_soup, args=(page,))
            thread_list.append(thread)
            thread.start()
        for t in thread_list:
            t.join()

    def get_students_list(self):
        students = []
        for i in self.all_data:
            students += self.get_students(i)
        sorted_students = [item for item in students]
        return sorted(sorted_students, key=lambda x: x["place"])

    def update(self):
        self.get_all_data()

