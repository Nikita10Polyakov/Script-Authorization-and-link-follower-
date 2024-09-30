import requests
import webbrowser
from bs4 import BeautifulSoup

# Пример использования
login_page_url = "https://?/login/"
login_url = "https://?/login/login"
protected_url = "https://?/"  # измените на нужный URL защищенной страницы
credentials = {
    'login': '?',
    'password': '?',
    'remember': '1',
    '_xfRedirect': 'https://?'
}
headers = {
    'User-Agent': '?',
    'Referer': 'https://?/login/'
}

def visit_url(url):
    try:
        # Выполнение HTTP-запроса
        response = requests.get(url)

        # Проверка успешного выполнения запроса
        if response.status_code == 200:
            print(f"Успешно перешли по ссылке: {url}")
            print("Статус код:", response.status_code)
            print("Содержимое страницы:")
            print(response.text[:500])  # Выводим первые 500 символов содержимого страницы

            # Открытие ссылки в веб-браузере
            # webbrowser.open(url)
        else:
            print(f"Не удалось перейти по ссылке: {url}")
            print("Статус код:", response.status_code)

    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при переходе по ссылке: {e}")
def login_and_visit(protected_url, login_url, login_page_url, credentials, headers=None):
    with requests.Session() as session:
        # Выполнение GET-запроса для получения страницы авторизации
        get_response = session.get(login_page_url, headers=headers)

        # Извлечение CSRF-токена из страницы (если необходимо)
        soup = BeautifulSoup(get_response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': '_xfToken'})['value']
        credentials['_xfToken'] = csrf_token

        # Выполнение POST-запроса для авторизации
        response = session.post(login_url, data=credentials, headers=headers)

        # Проверка успешной авторизации
        if response.status_code == 200 and 'data-logged-in="true"' in response.text:
            print("Успешная авторизация.")

            # Выполнение GET-запроса к защищенной странице
            response = session.get(protected_url, headers=headers)

            if response.status_code == 200:
                print(f"Успешно перешли по ссылке: {protected_url}")
                print("Статус код:", response.status_code)
                print("Содержимое страницы:")
                print(response.text[:1])  # Выводим первые 500 символов содержимого страницы

                # Открытие ссылки в веб-браузере
                # webbrowser.open(protected_url)

                a = "https://1?"
                b = "https://2?"
                c = "https://3?"

                # Пример использования
                url_to_visit = input("a,b,c ")

                if url_to_visit == "a":
                    url_to_visit = a
                elif url_to_visit == "b":
                    url_to_visit = b
                elif url_to_visit == "c":
                    url_to_visit = c

                visit_url(url_to_visit)

            else:
                print(f"Не удалось перейти по ссылке: {protected_url}")
                print("Статус код:", response.status_code)
        else:
            print("Не удалось авторизоваться")
            print("Статус код:", response.status_code)
            print("Причина:", response.text)  # Выводим текст ответа для диагностики

        # # Дополнительная диагностика
        # print("Cookies после авторизации:")
        # print(session.cookies.get_dict())
        #
        # print("Содержимое страницы после авторизации (первые 500 символов):")
        #
        # soup = BeautifulSoup(response.text, 'html.parser')
        # body_content = soup.body.text  # Получаем текст из тега <body>
        # print("Содержимое страницы внутри тега <body>:\n", body_content)


login_and_visit(protected_url, login_url, login_page_url, credentials, headers)

