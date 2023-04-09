import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('tests/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'email'))).send_keys('19qwerty94@mail.ru')
    # Вводим пароль
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'pass'))).send_keys('qwert123!')
    # Нажимаем на кнопку входа в аккаунт
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//a[@class='nav-link'])[1]"))).click()

    pytest.driver.implicitly_wait(10)
    images = pytest.driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-img-top')
    names = pytest.driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-title')
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
