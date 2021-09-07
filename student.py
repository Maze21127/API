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
        # return f'№ {self.place}\n' \
        #        f'СНИЛС {self.snils}\n' \
        #        f'Согласие на зачисление: {self.accept}\n' \
        #        f'Прием на места: {self.payment}\n' \
        #        f'Преимущество: {self.benefits}\n' \
        #        f'Сумма баллов: {self.total_score}\n' \
        #        f'{self.first_obj}\n' \
        #        f'{self.second_obj}\n' \
        #        f'{self.third_obj}\n'
