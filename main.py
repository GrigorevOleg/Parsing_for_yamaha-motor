from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
import requests
import csv

browser = webdriver.Chrome()

with open('res.csv', 'w', newline='', encoding='utf-8-sig') as file:  # Очистка файла перед парсингом
    pass

for i in range(1962, 2025):

    url = f'https://yamaha-api-poc-main.prod.yamaha-motor.com/v1.0.0/parts/browse/motorcycle/{515232 + i - 1962}/models'  # Получаем файл json со списком моделей для конкретного года
    head = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0Mjk3OTI5LCJpYXQiOjE3MDQyNzYzMjksImp0aSI6IjA0ZjI2MDFjYWMwMzRlYjBiYmY5MmU5NzQ4Y2EwMTk4IiwiYW5vbiI6dHJ1ZSwiYWNjZXNzIjpbImd1ZXN0Iiwic2hvcCIsImRlYWxlcnMiLCJjb250ZW50IiwiaGVhbHRoIiwic2VhcmNoIiwiZml0bWVudCIsInBhcnRzIl19._D6bKGHKfk2mMggt-wZ859Too6BApY2xV15T24TkTVg'}
    response = requests.get(url=url, headers=head).json()
    list_models = [i['name'] for i in response['data']]

    for model in list_models:
        browser.get('https://yamaha-motor.com/parts/motorcycle')
        time.sleep(3)

        year_input = browser.find_element(By.XPATH, '/html/body/div/section/div[2]/div[3]/div[1]/div/div/div/input')
        model_input = browser.find_element(By.XPATH, '/html/body/div/section/div[2]/div[3]/div[2]/div/div/div/input')
        button_search = browser.find_element(By.XPATH, '/html/body/div/section/div[2]/div[3]/button')

        year_input.clear()  # Выбираем год
        year_input.send_keys(str(i))
        time.sleep(3)
        year_input.send_keys(Keys.ARROW_DOWN)
        year_input.send_keys(Keys.ENTER)

        model_input.clear()  # Выбираем модель
        model_input.send_keys(model)
        time.sleep(3)
        model_input.send_keys(Keys.ARROW_DOWN)
        model_input.send_keys(Keys.ENTER)
        time.sleep(3)

        while True:  # Проверка успела ли загрузиться кнопка, если нет, ждем еще 3 секунды
            try:
                button_search.click()
                break
            except Exception as e:
                time.sleep(3)

        time.sleep(3)

        name = browser.find_element(By.CLASS_NAME, "ModelInfo_ModelInfo__Title__ZxLcj").text  # Забираем название модели

        while True:  # Что бы прогрузились все ссылки пролистываем страницу до конца
            last_height = browser.execute_script("return document.body.scrollHeight")
            scroll_by = f'window.scrollBy(0, 1000);'
            browser.execute_script(scroll_by)
            time.sleep(3)
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break

        links = [link.get_attribute('href') for link in
                 browser.find_elements(By.CLASS_NAME, 'DiagramItem_diagramItem__w0bwW')]  # Собираем ссылки на схемы

        with open('res.csv', 'a', newline='', encoding='utf-8-sig') as file:  # Записываем данные в csv файл
            writer = csv.writer(file, delimiter=';')
            writer.writerow([name, '\n'.join(links)])
