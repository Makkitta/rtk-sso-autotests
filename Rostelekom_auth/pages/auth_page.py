from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        """Открываем страницу авторизации"""
        self.driver.get("https://b2c.passport.rt.ru/")

    def select_auth_type(self, auth_type):
        """Словарь соответствия типов авторизации и их ID на странице"""
        types = {
            "phone": "t-btn-tab-phone",
            "email": "t-btn-tab-mail",
            "login": "t-btn-tab-login",
            "ls": "t-btn-tab-ls"
        }
        self.wait.until(EC.element_to_be_clickable((By.ID, types[auth_type]))).click()

    def enter_username(self, username):
        """Ввод логина/телефона/email в поле username"""
        self.wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(username)

    def enter_password(self, password):
        """Ввод пароля"""
        self.wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(password)

    def click_submit(self):
        """Нажатие кнопки Войти"""
        self.wait.until(EC.element_to_be_clickable((By.ID, "kc-login"))).click()

    def get_error_message(self):
        """Получение текста ошибки авторизации"""
        return self.wait.until(EC.visibility_of_element_located((By.ID, "form-error-message"))).text

    def go_to_registration(self):
        """Переход на страницу регистрации"""
        self.wait.until(EC.element_to_be_clickable((By.ID, "kc-register"))).click()

    def go_to_recovery(self):
        """Переход на страницу восстановления пароля"""
        self.wait.until(EC.element_to_be_clickable((By.ID, "forgot_password"))).click()

    def is_redirected(self, url_part):
        """Проверка редиректа на определенную страницу"""
        return url_part in self.driver.current_url
