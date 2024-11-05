import requests
import platform
import threading
import time
from datetime import datetime, timedelta
import cookies_finder
from cookies_finder import get_cookie_values
import os

LICENSE_FILE = "license_key.txt"
DEVICE_ID = platform.node()  # Уникальный идентификатор устройства (например, имя устройства)

# Функция для запроса и сохранения лицензионного ключа
def get_license_key():
    if os.path.exists(LICENSE_FILE):
        with open(LICENSE_FILE, "r") as file:
            return file.read().strip()
    else:
        license_key = input("Введите ваш ключ активации: ").strip()
        with open(LICENSE_FILE, "w") as file:
            file.write(license_key)
        return license_key

LICENSE_KEY = get_license_key()  # Получаем или сохраняем введенный пользователем ключ

# Проверка лицензии
def check_license():
    try:
        response = requests.post("http://localhost:5000/verify_license", json={"license_key": LICENSE_KEY, "device_id": DEVICE_ID})
        if response.status_code == 200 and response.json().get("status") == "valid":
            print("Лицензия подтверждена. Запуск программы.")
            return True
        else:
            print("Неверная лицензия или неавторизованное устройство.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения к серверу лицензий: {e}")
        return False

# Регистрация лицензии
def register_license():
    try:
        response = requests.post("http://localhost:5000/register_license", json={"license_key": LICENSE_KEY, "device_id": DEVICE_ID})
        if response.status_code == 200 and response.json().get("status") == "registered":
            print("Лицензия успешно зарегистрирована!")
            return True
        else:
            print("Ошибка при регистрации лицензии.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения к серверу лицензий: {e}")
        return False

# Проверяем или регистрируем лицензию перед запуском основной логики
if not check_license():
    if not register_license():
        exit("Программа завершена: нет действительной лицензии.")

# Основной код программы
user_cookies = get_cookie_values("user1/cookies.pkl")

COOKIES = {
    'x-o3-app-name': 'ozonapp_android',
    'x-o3-app-version': '17.40.1(2517)',
    'MOBILE_APP_TYPE': 'ozonapp_android',
    '__Secure-access-token': user_cookies.get("__Secure-access-token", ""),
    '__Secure-refresh-token': user_cookies.get("__Secure-refresh-token", ""),
    'abt_data': user_cookies.get("abt_data", ""),
}

PROXY = 'JJsaiiaq1:123aa1dqa@109.248.13.177:5500'
cookie_header = "; ".join([f"{key}={value}" for key, value in COOKIES.items()])

def refresh_cart_and_go_to_checkout():
    start_time = time.time()
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'cookie': cookie_header, 'proxies': PROXY, "sku_id": "177359226"}

    response = requests.post('https://api.theimpulse.cc/ozon_cart_refresh', headers=headers, data=data)
    print(response.text)
    response = requests.post('https://api.theimpulse.cc/ozon_checkout_step_1', headers=headers, data=data)
    print(response.text)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения {execution_time:.6f} секунд")

def main_():
    start_time = time.time()
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'cookie': cookie_header, 'proxies': PROXY}

    response = requests.post('https://api.theimpulse.cc/ozon_checkout_step_2', headers=headers, data=data)
    print(response.text)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения {execution_time:.6f} секунд")
    time.sleep(1)

def mega_alarm(target_hour, target_minute, target_second, target_millisecond):
    now = datetime.now()
    target_time = now.replace(hour=target_hour, minute=target_minute, second=target_second,
                              microsecond=target_millisecond * 1000)
    if target_time < now:
        target_time += timedelta(days=1)
    while datetime.now() < target_time:
        time.sleep(0.0001)

    threading.Thread(target=refresh_cart_and_go_to_checkout).start()
    threading.Thread(target=main_).start()

# Укажите время для запуска
mega_alarm(16, 20, 00, 000)
