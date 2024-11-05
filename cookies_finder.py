import pickle

def get_cookie_values(cookie_file):
    """
    Извлекает значения для указанных ключей из файла cookies.pkl.

    Параметры:
        cookie_file (str): Путь к файлу куки.

    Возвращает:
        dict: Словарь с найденными значениями для ключей 'Secure-access-token', 'Secure-refresh-token', 'abt_data'.
    """
    # Список интересующих ключей
    keys_to_find = ['Secure-access-token', 'Secure-refresh-token', 'abt_data']
    found_cookies = {key: None for key in keys_to_find}  # Словарь для хранения значений

    # Загружаем куки из файла
    with open(cookie_file, 'rb') as file:
        cookies = pickle.load(file)

    # Поиск значений для указанных ключей
    for cookie in cookies:
        name = cookie.get('name')
        if name in keys_to_find:
            found_cookies[name] = cookie.get('value')

    return found_cookies