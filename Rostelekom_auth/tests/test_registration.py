import time

from pages.auth_page import AuthPage
from pages.reg_page import RegPage


class TestRegistration:
    def test_registration_page_loads(self, driver):
        """Проверка загрузки страницы регистрации"""
        auth_page = AuthPage(driver)
        auth_page.open()
        auth_page.go_to_registration()

        assert "registration" in driver.current_url

    def test_registration_with_valid_data(self, driver):
        """Регистрация с валидными данными (позитивный тест)"""
        auth_page = AuthPage(driver)
        auth_page.open()
        auth_page.go_to_registration()

        reg_page = RegPage(driver)
        reg_page.enter_firstname("Иван")
        reg_page.enter_lastname("Иванов")
        reg_page.select_region()
        reg_page.enter_email_or_phone("existing@mail.ru")
        reg_page.enter_password("ValidPass123")
        reg_page.enter_password_confirm("ValidPass123")
        reg_page.click_register()

        time.sleep(5)

        # Проверяем, что перешли на страницу подтверждения email
        assert "execution" in driver.current_url

    def test_registration_existing_email(self, driver):
        """Регистрация с существующим email (негативный тест)"""
        auth_page = AuthPage(driver)
        auth_page.open()
        auth_page.go_to_registration()

        reg_page = RegPage(driver)
        reg_page.enter_firstname("Иван")
        reg_page.enter_lastname("Иванов")
        reg_page.select_region()
        reg_page.enter_email_or_phone("test@mail.ru")  # Предполагаем, что этот email уже зарегистрирован
        reg_page.enter_password("ValidPass123")
        reg_page.enter_password_confirm("ValidPass123")
        reg_page.click_register()

        time.sleep(5)

        assert reg_page.is_existing_account_error_displayed()

    def test_registration_short_name(self, driver):
        """Регистрация с коротким именем (негативный тест)"""
        auth_page = AuthPage(driver)
        auth_page.open()
        auth_page.go_to_registration()

        reg_page = RegPage(driver)
        reg_page.enter_firstname("И")  # Слишком короткое имя
        reg_page.enter_lastname("Иванов")

        assert "Необходимо заполнить поле кириллицей. От 2 до 30 символов." in reg_page.get_error_message()

    def test_registration_password_mismatch(self, driver):
        """Регистрация с несовпадающими паролями (негативный тест)"""
        auth_page = AuthPage(driver)
        auth_page.open()
        auth_page.go_to_registration()

        reg_page = RegPage(driver)
        reg_page.enter_firstname("Иван")
        reg_page.enter_lastname("Иванов")
        reg_page.select_region()
        reg_page.enter_email_or_phone("test@mail.ru")
        reg_page.enter_password("ValidPass123")
        reg_page.enter_password_confirm("DifferentPass123")  # Пароли не совпадают
        reg_page.click_register()

        assert "Пароли не совпадают" in reg_page.get_error_message()

    def test_registration_invalid_password(self, driver):
        """Регистрация с невалидным паролем (негативный тест)"""
        auth_page = AuthPage(driver)
        auth_page.open()
        auth_page.go_to_registration()

        reg_page = RegPage(driver)
        reg_page.enter_firstname("Иван")
        reg_page.enter_lastname("Иванов")
        reg_page.select_region()
        reg_page.enter_email_or_phone("test@mail.ru")
        reg_page.enter_password("short")  # Слишком короткий пароль
        reg_page.enter_password_confirm("short")

        assert "Длина пароля должна быть не менее 8 символов" in reg_page.get_error_message()

# pytest -v tests/test_registration.py
# суммарно 6 тестов