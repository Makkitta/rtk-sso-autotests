from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class RegPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def enter_firstname(self, firstname):
        """Ввод имени"""
        self.wait.until(EC.visibility_of_element_located((By.NAME, "firstName"))).send_keys(firstname)

    def enter_lastname(self, lastname):
        """Ввод фамилии"""
        self.wait.until(EC.visibility_of_element_located((By.NAME, "lastName"))).send_keys(lastname)

    def select_region(self, region=None):
        """Выбор региона из выпадающего списка"""
        region_field = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='page-right']/div[1]/div[1]/div[1]/form[1]/div[2]/div[1]/div[1]/input[1]")))
        region_field.click()

        first_region_option = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='page-right']/div[1]/div[1]/div[1]/form[1]/div[2]/div[2]/div[2]/div[1]/div[2]")))
        first_region_option.click()


    def enter_email_or_phone(self, contact):
        """Bвод email или телефона"""
        self.wait.until(EC.visibility_of_element_located((By.ID, "address"))).send_keys(contact)

    def enter_password(self, password):
        """Ввод пароля"""
        self.wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(password)

    def enter_password_confirm(self, password):
        """Подтверждение пароля"""
        self.wait.until(EC.visibility_of_element_located((By.ID, "password-confirm"))).send_keys(password)

    def click_register(self):
        """Нажатие кнопки Зарегистрироваться"""
        self.wait.until(EC.element_to_be_clickable((By.NAME, "register"))).click()

    def get_error_message(self):
        """Получение текста ошибки валидации"""
        return self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "rt-input-container__meta--error"))).text

    def is_existing_account_error_displayed(self):
        """Проверяет, отображается ли ошибка 'Учётная запись уже существует'"""
        error_modal = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'card-modal__card')]"))
        )
        error_title = error_modal.find_element(By.XPATH, ".//h2[contains(@class, 'card-modal__title')]")
        error_text = error_title.text.strip()
        return "Учётная запись уже существует" in error_text

