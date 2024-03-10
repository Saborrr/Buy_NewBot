import requests


URL = 'https://yesno.wtf/api'


def yes_or_no():
    """Метод вывода ответа да/нет."""
    # Делаем GET-запрос к API
    # Метод json() преобразует ответ JSON в тип данных, понятный Python
    response = requests.get(URL).json()
    # получаем ссылку на изображение
    random_answer = response.get('image')
    return random_answer
