import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages import auth_page, reg_page
from pages.auth_page import AuthPage


class TestRecovery:
    def test_recovery_page_loads(self, driver):
        """Проверка загрузки страницы восстановления пароля"""
        page = AuthPage(driver)
        page.open()
        page.go_to_recovery()

        assert "reset-credentials" in driver.current_url

    def test_password_recovery_with_phone(self, driver):
        """Восстановление пароля по телефону"""
        page = AuthPage(driver)
        page.open()
        page.go_to_recovery()

        username_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        username_field.send_keys("+79991234567")

        reset_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "reset"))
        )
        reset_button.click()

        time.sleep(3)
        assert "code" in driver.current_url

    def test_password_recovery_with_email(self, driver):
        """Восстановление пароля по email"""
        page = AuthPage(driver)
        page.open()
        page.go_to_recovery()

        # Вводим email и отправляем запрос
        driver.find_element(By.ID, "username").send_keys("test@mail.ru")
        driver.find_element(By.ID, "reset").click()

        time.sleep(5)

        # Проверяем, что перешли на страницу ввода кода
        assert "code" in driver.current_url


    def test_recovery_with_nonexistent_account(self, driver):
        """Восстановление пароля для несуществующего аккаунта (негативный тест)"""
        page = AuthPage(driver)
        page.open()
        page.go_to_recovery()

        # Вводим несуществующий email
        driver.find_element(By.ID, "username").send_keys("nonexistent@mail.ru")
        driver.find_element(By.ID, "reset").click()

        # Проверяем сообщение об ошибке
        error_message = driver.find_element(By.ID, "form-error-message").text
        assert "Неверный логин или текст с картинки" in error_message

    def test_back_to_auth_from_recovery(self, driver):
        """Возврат к авторизации со страницы восстановления"""
        page = AuthPage(driver)
        page.open()
        page.go_to_recovery()

        driver.find_element(By.ID, "reset-back").click()

        # Проверяем, что вернулись на страницу авторизации
        assert "authenticate" in driver.current_url

    def test_recovery_form_validation(self, driver):
        """Проверка валидации формы восстановления пароля"""
        page = AuthPage(driver)
        page.open()
        page.go_to_recovery()

        # Пытаемся отправить пустую форму
        driver.find_element(By.ID, "reset").click()

        # Проверяем сообщение об ошибке
        error_message = driver.find_element(By.CLASS_NAME, "rt-input-container__meta--error").text
        assert "Введите номер телефона" in error_message

# pytest -v tests/test_recovery.py
