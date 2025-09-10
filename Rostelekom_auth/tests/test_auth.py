import pytest
from selenium.webdriver.support.wait import WebDriverWait
from pages.auth_page import AuthPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TestAuth:
    def test_auth_page_loads(self, driver):
        """Проверка загрузки страницы авторизации"""
        page = AuthPage(driver)
        page.open()

        assert "authenticate" in driver.current_url

    @pytest.mark.parametrize("auth_type", ["phone", "email", "login", "ls"])
    def test_auth_type_switching(self, driver, auth_type):
        """Проверка переключения между типами авторизации"""
        page = AuthPage(driver)
        page.open()
        page.select_auth_type(auth_type)

        active_tab = driver.find_element(By.CLASS_NAME, "rt-tab--active")
        assert auth_type in active_tab.get_attribute("id")

    def test_auth_with_valid_phone(self, driver):
        """Успешная авторизация по номеру телефона (позитивный тест)"""
        page = AuthPage(driver)
        page.open()
        page.select_auth_type("phone")
        page.enter_username("+79991234567")
        page.enter_password("ValidPassword123")
        page.click_submit()

        assert page.is_redirected("account_b2c")

    def test_auth_with_invalid_password(self, driver):
        """Авторизация с неверным паролем (негативный тест)"""
        page = AuthPage(driver)
        page.open()
        page.select_auth_type("phone")
        page.enter_username("+79991234567")
        page.enter_password("InvalidPassword")
        page.click_submit()

        assert "Неверный логин или пароль" in page.get_error_message()

    def test_auth_with_invalid_phone(self, driver):
        """Авторизация с неверным телефоном (негативный тест)"""
        page = AuthPage(driver)
        page.open()
        page.select_auth_type("phone")
        page.enter_username("+79991299599")
        page.enter_password("ValidPassword123")
        page.click_submit()

        assert "Неверный логин или пароль" in page.get_error_message()

    def test_auto_switch_to_email_tab(self, driver):
        """Автоматическое переключение на таб email при вводе email"""
        page = AuthPage(driver)
        page.open()
        page.enter_username("test@mail.ru")

        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element_attribute(
                (By.CLASS_NAME, "rt-tab--active"), "id", "mail"
            )
        )

        active_tab = driver.find_element(By.CLASS_NAME, "rt-tab--active")
        assert "mail" in active_tab.get_attribute("id")

    def test_successful_login_auth(self, driver):
        """Успешная авторизация по логину"""
        page = AuthPage(driver)
        page.open()
        page.select_auth_type('login')
        page.enter_username("TestLogin")
        page.enter_password("ValidPassword123")
        page.click_submit()

        assert page.is_redirected("account_b2c")

    def test_successful_email_auth(self, driver):
        """Успешная авторизация по почте"""
        page = AuthPage(driver)
        page.open()
        page.select_auth_type('email')
        page.enter_username("test@mail.ru")
        page.enter_password("ValidPassword123")
        page.click_submit()

        assert page.is_redirected("account_b2c")


    def test_go_to_registration(self, driver):
        """Переход на страницу регистрации"""
        page = AuthPage(driver)
        page.open()
        page.go_to_registration()

        assert "registration" in driver.current_url

    def test_go_to_recovery(self, driver):
        """Переход на страницу восстановления пароля"""
        page = AuthPage(driver)
        page.open()
        page.go_to_recovery()

        assert "reset-credentials" in driver.current_url

# pytest -v tests/test_auth.py
# суммарно 13 тестов