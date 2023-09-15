import time
from settings import valid_email, valid_password
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()


@pytest.fixture(scope='class', autouse=True)
def run():
    try:
        # страница авторизации
        driver.get('http://petfriends.skillfactory.ru/login')
        # добавляем ожидание появления кнопки войти
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@type="submit"]')))
        # вводим email
        driver.find_element(By.ID, 'email').send_keys(valid_email)
        # вводим пароль
        driver.find_element(By.ID, 'pass').send_keys(valid_password)
        # кликаем на кнопку входа в аккаунт
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        yield
    except Exception as e:
        # обрабатываем исключение
        print(f"Произошла ошибка: {str(e)}")
    finally:
        driver.quit()


class TestLocators:
    def test_my_pets(self):
        # проверка наличия питомцев
        driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="all_my_pets"]')))
        cards = driver.find_elements(By.CSS_SELECTOR, 'tbody>tr')
        statistics = driver.find_element(By.CSS_SELECTOR, 'div.task3 div')
        amount = statistics.text.split(': ')
        assert len(cards) != int(amount[1][0])

    def test_images_numbers(self):
        # проверка, есть ли у половины питомцев фото
        driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]/h2')))
        images = driver.find_elements(By.CSS_SELECTOR, 'img')
        statistics = driver.find_element(By.CSS_SELECTOR, 'div.task3 div')
        amount = statistics.text.split(': ')
        count = 0
        for i in range(len(images)):
            if images[i].get_attribute('src') != '':
                count += 1
        assert count > (int(amount[1][0]) // 2)

    def test_check_animal_data(self):
        # проверка данных питомцев
        driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
        driver.implicitly_wait(5)
        descriptions = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets table tbody tr')
        for i in range(len(descriptions)):
            parts = descriptions[i].text.split(' ')
            if len(parts) >= 3:
                assert len(parts[0]) > 0
                assert len(parts[1]) > 0
                assert len(parts[2]) > 0

    def test_check_name(self):
        # проверяем, все ли имена питомцев уникальны
        driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
        driver.implicitly_wait(5)
        names = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets table tbody tr')
        pet_name = []
        for i in range(len(names)):
            parts = names[i].text.split(' ')
            pet_name.append(parts[0])
        for i in range(len(pet_name) - 1):
            for j in range(i+1, len(pet_name)):
                assert pet_name[i] != pet_name[j]


    def test_check_all_animals(self):
        # проверяем, все ли карточки питомцев уникальны
        driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
        driver.implicitly_wait(5)
        descriptions = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets table tbody tr')
        animal_data = []
        for i in range(len(descriptions)):
            animal_data.append(descriptions[i].text.split(' '))
        for i in range(len(animal_data)-1):
            for j in range(i+1, len(animal_data)):
                assert animal_data[i][0] != animal_data[j][0]
                assert animal_data[i][1] != animal_data[j][1]
                assert animal_data[i][2] != animal_data[j][2]