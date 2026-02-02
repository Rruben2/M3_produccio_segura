from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        # cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(f'{self.live_server_url}/admin/login/')

        self.assertEqual(self.selenium.title, "Log in | Django site admin")

        # Login admin
        self.selenium.find_element(By.NAME, "username").send_keys('admin')
        self.selenium.find_element(By.NAME, "password").send_keys('admin123')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        self.assertEqual(self.selenium.title, "Site administration | Django site admin")

        # Click en Users
        self.selenium.find_element(By.XPATH, '//a[text()="Users"]').click()

        # Click Add user
        self.selenium.find_element(
            By.XPATH,
            '//a[@class="addlink" and contains(text(), "Add user")]'
        ).click()

        # Crear usuario
        self.selenium.find_element(By.NAME, "username").send_keys('liltimmy')
        self.selenium.find_element(By.NAME, "password1").send_keys('proof12345')
        self.selenium.find_element(By.NAME, "password2").send_keys('proof12345')
        self.selenium.find_element(By.XPATH, '//input[@value="Save"]').click()

        # Confirmar creación
        self.selenium.find_element(By.XPATH, '//input[@value="Save"]').click()

        # ======= AQUÍ ESTABA LO QUE FALTABA =======
        # Volver a la lista de usuarios y comprobar que existe
        self.selenium.find_element(By.XPATH, '//a[text()="Users"]').click()

        usuario = self.selenium.find_element(By.XPATH, '//a[text()="liltimmy"]')
        self.assertIsNotNone(usuario)
        # =========================================

        # Logout admin
        self.selenium.find_element(
            By.XPATH,
            '//button[@type="submit" and contains(text(), "Log out")]'
        ).click()

        # Login con el nuevo usuario
        self.selenium.find_element(By.LINK_TEXT, "Log in again").click()
        self.selenium.find_element(By.NAME, "username").send_keys('liltimmy')
        self.selenium.find_element(By.NAME, "password").send_keys('proof12345')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
