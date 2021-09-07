import requests
from bs4 import BeautifulSoup


class Student:
    def __init__(self, place, snils, accept, payment, benefits, total_score, first_obj, second_obj, third_obj):
        self.place = int(place)
        self.snils = snils
        self.accept = accept
        self.payment = payment
        self.benefits = benefits
        self.total_score = int(total_score)
        self.first_obj = first_obj
        self.second_obj = second_obj
        self.third_obj = third_obj

    def get_dict(self):
        students_dict = dict()
        students_dict['place'] = self.place
        students_dict['snils'] = self.snils
        students_dict['accept'] = self.accept
        students_dict['payment'] = self.payment
        students_dict['benefits'] = self.benefits
        students_dict['total_score'] = self.total_score
        students_dict['first_obj'] = self.first_obj
        students_dict['second_obj'] = self.second_obj
        students_dict['third_obj'] = self.third_obj
        return students_dict

    def __repr__(self):
        return str(self.get_dict())

    @staticmethod
    def get_soup(page=1):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.8.1.468 Yowser/2.5 Safari/537.36',
            'accept': '*/*'
        }
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
        url = 'https://www.vvsu.ru/controller/elementLoad.php'
        html = requests.post(url=url, headers=headers, data=data)
        html.encoding = 'utf-8'
        return BeautifulSoup(html.text, 'lxml')

    @staticmethod
    def get_students_soup(soup_obj):
        return soup_obj.find_all(style=["background:#F6F6F6; !important;", "background:#C1E0C1; !important;"])

    @staticmethod
    def get_pagination(soup_obj):
        test = soup_obj.find(class_="pagination").find_all('li')
        url = test[-1].find('a').get('href')
        return int(url[url.find('page/') + 5:-1])

    @staticmethod
    def get_students_list(soup_obj):
        students = []

        for student in soup_obj:
            student_td = student.find_all('td')

            student_td = list(map(lambda x: x.text.strip(), student_td))
            my_student = Student(student_td[0], student_td[1], student_td[2], student_td[3], student_td[4],
                                 student_td[5],
                                 student_td[6], student_td[7], student_td[8])
            students.append(my_student)
        return students

    @staticmethod
    def get_students_dict():
        first_page_soup = Student.get_soup()
        print(f'first_page_complete')
        first_page_students = Student.get_students_soup(first_page_soup)

        page_count = Student.get_pagination(first_page_soup)
        students_list = Student.get_students_list(first_page_students)

        for i in range(2, page_count + 1):
            temp_students = Student.get_students_list(Student.get_students_soup(Student.get_soup(i)))
            students_list += temp_students
            print(f'{i} - complete')
        # return students_list
        return [stud.get_dict() for stud in students_list]