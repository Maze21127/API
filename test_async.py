import aiohttp
import asyncio
from bs4 import BeautifulSoup
from time import time


def get_pagination(soup_obj):
    test = soup_obj.find(class_="pagination").find_all('li')
    url = test[-1].find('a').get('href')
    return int(url[url.find('page/') + 5:-1])


async def get_page_data(session, page):
    data = {
        'GetInfoBlock': '{"filters":[{"id":"604734","value":41,"label":"Высшее образование  - Бакалавриат "},'
                        '{"id":"604735","value":1,"label":"очная "},'
                        '{"id":"631093","value":892,"label":"Информационные системы и технологии "},'
                        '{"id":"631098","value":2169,"label":"09.03.02 Информационные системы и технологии "},'
                        '{"id":"631383","value":11507,"label":"Институт информационных технологий "}],'
                        '"filterDates":[]}',
        'url': f'https://www.vvsu.ru/enter/order/page/{page}/',
        'element': '2149012088',
        'clearPager': 'true'
    }
    url = 'https://www.vvsu.ru/controller/elementLoad.php'

    async with session.post(url=url, data=data) as response:
        assert response.status == 200
        print(f'get url: {data["url"]}')
        response_text = await response.text()
        print(f'ответ для {page = } получен')
        all_data.append(response_text)
        return response_text


async def gather_data():
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
        'url': f'https://www.vvsu.ru/enter/order/page/{1}/',
        'element': '2149012088',
        'clearPager': 'True'
    }
    url = 'https://www.vvsu.ru/controller/elementLoad.php'
    async with aiohttp.ClientSession() as session:
        response = await session.post(url=url, headers=headers, data=data)
        soup = BeautifulSoup(await response.text(), 'lxml')
        pages_count = get_pagination(soup)

        tasks = []
        for page in range(1, pages_count + 1):

            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


def get_students(data):
    students = []
    soup = BeautifulSoup(data, 'lxml')
    soup_obj = soup.find_all(style=["background:#F6F6F6; !important;", "background:#C1E0C1; !important;"])
    for student in soup_obj:
        student_td = student.find_all('td')
        student_td = list(map(lambda x: x.text.strip(), student_td))
        my_student = (student_td[0], student_td[1], student_td[2], student_td[3], student_td[4],
                      student_td[5],
                      student_td[6], student_td[7], student_td[8])
        students.append(my_student)
    return students


all_data = []
start = time()
asyncio.run(gather_data())

print(f'Данные собраны за {time() - start} секунд')
print(len(all_data))
