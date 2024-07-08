import time
import unittest


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

"""
Libraria unittest ofera suport pentru crearea de teste rulabile direct in interiorul clasei
Se implementeaza prin mostenirea clasei TestCase din libraria unittest
Orice clasa de teste trebuie sa mosteneasca clasa TestCase si sa aiba urmatoarele particularitati:
1. metoda setUp() -> toate activitatile care trebuiesc executate inainte de ORICE TEST din clasa respectiva
2. metoda tearDown() -> toate activitatile care trebuie sa fie executate dupa ORICE TEST din clasa respectiva
3. toate metodele de test trebuie sa aiba prefixul: test_
"""

class Test(unittest.TestCase):
    LOGIN_LINK = "https://the-internet.herokuapp.com/login"
    BUTTON_LOGIN = (By.CLASS_NAME, "fa-sign-in")
    BUTTON_LOGOUT = (By.CLASS_NAME, "button secondary radius")
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    User_corect = "tomsmith"
    Pass_corect = "SuperSecretPassword!"



    # suprascriem metoda setUp care va rula inainte de fiecare test
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.LOGIN_LINK)
        self.driver.maximize_window()
        time.sleep(1)

    #suprascriem metoda tearDown care va rula dupa fiecare test
    def tearDown(self):
        self.driver.quit()

    #TEST 1
    # - Verifica daca URL-ul paginii este corect
    @unittest.skip
    def test_url(self):
        actual_url = self.driver.current_url
        self.assertEqual(self.LOGIN_LINK, actual_url, "Unexpected URL")

    #TEST 2
    # - Verifica daca titlul paginii apare corect
    @unittest.skip
    def test_title(self):
        expected_title = "The Internet"
        actual_title = self.driver.title

        # assert expected_title == actual_title, f"Unexpected title, expected {expected_title}, but found {actual_title}"
        self.assertEqual(expected_title, actual_title, "Unexpected title")

    #TEST 3
    # - verifica daca textul de pe elementul xpath = //h2 este corect
    @unittest.skip
    def test_h2_text(self):
        text_h2 = self.driver.find_element(By.XPATH, "//h2").text
        expected_text = "Login Page"

        self.assertEqual(expected_text, text_h2, "Textul h2 este incorect")

    #TEST 4
    # - verificam daca butonul submit este afisat
    @unittest.skip
    def test_button_login_displayed(self):
        login_button = self.driver.find_element(*self.BUTTON_LOGIN)
        assert login_button.is_displayed(), "Butonul de login nu este afisat"

    #Test 5
    # - verifica daca atributul href al linkului "ELemental Selenium" e corect
    @unittest.skip
    def test_atribut_href(self):
        expected_href = "http://elementalselenium.com/"

        # luam atributul de top "href" de pe acel element de tip a
        actual_href = self.driver.find_element(By.XPATH, "//a[text()='Elemental Selenium']").get_attribute("href")

        self.assertEqual(expected_href, actual_href, "Link-ul 'href este incorect")


    #TEST 6
    # - lasam goale user si pass;
    # - click login
    # - verifica daca eroare e displayed
    @unittest.skip
    def test_blank_login(self):
        # Facem click pe butonul de login
        self.driver.find_element(*self.BUTTON_LOGIN).click()
        eroare = self.driver.find_element(By.ID, "flash")
        assert eroare.is_displayed(), "Eroarea nu este afisata dupa logarea far Username/Parola"

    #TEST 7
    # - Completeaza cu user si pass invalide
    # - Click login
    # - Verifica daca mesajul de pe eroare este corect
    @unittest.skip
    def test_invalid_login(self):
        username = self.driver.find_element(*self.USERNAME)
        username.send_keys("wrong_user")
        password = self.driver.find_element(*self.PASSWORD)
        password.send_keys("wrong_password")
        self.driver.find_element(*self.BUTTON_LOGIN).click()
        expected_message = "Your username is invalid"
        actual_message = self.driver.find_element(By.ID, "flash").text # luam textul, am testat si asta inclusiv

        # Assert pentru a verifica daca o expresie este adevarata
        # Metoda assertTrue() primeste 2 parametrii:
        #  * primul param - expresie de evaluat
        #  * al doilea param - (optional) mesajul de eroare afisat
        self.assertTrue(expected_message in actual_message, "Mesajul de eroare nu este corect!")

    # metoda ajutatoare - ea nu va fi rulata ca test pentru ca nu are prefixul test_
    # metoda are doi paramentrii:
    # 1 - element_locator: locatorul elementului dupa care asteptam sa apara
    # 2 - seconds_to_wait: numarul maxim de secunde de asteptare pentru ca elementul sa apara
    def wait_for_element_to_disappear(self, element_locator, seconds_to_wait):
        wait = WebDriverWait(self.driver, seconds_to_wait)
        return wait.until(EC.none_of(EC.presence_of_element_located(element_locator)))

    # metoda ajutatoare -
    def is_element_present(self, locator):
        return len(self.driver.find_element(*locator)) > 0 # daca nu gaseste nimic, returneaza o lista goala


    #TEST 8
    # - Lasa goale user si pass
    # - click login
    # - apasa x pe eroare
    # - verifica daca eroarea a disparut
    @unittest.skip
    def test_error_message_disappears_on_click(self):
        self.driver.find_element(*self.BUTTON_LOGIN).click()
        self.driver.find_element(By.CLASS_NAME, "close").click()
        self.wait_for_element_to_disappear((By.ID, "flash"), 5) # pentru ca nu dispare din prima, dureaza putin
                                                                                              # sa dispara dupa ce dai pe x
        self.assertTrue(not self.is_element_present((By.ID, "flash")))


    #TEST 9
    # - IA CA O LISTA TOATE //label
    # - verifica ca textul de pe ele sa fie cel asteptat (Username si Password)
    # - Aici e ok sa avem 2 asserturi
    @unittest.skip
    def test_username_label(self):
        username_label = self.driver.find_element(By.XPATH,'//label[@for="username"]')
        self.assertEqual(username_label.text, 'Username', "Nu coincid")

    @unittest.skip
    def test_password_label(self):
        password_label = self.driver.find_element(By.XPATH,'//label[@for="password"]')
        self.assertEqual(password_label.text, 'Password' , "Nu coincid")


    # TEST 10
    # - Completeaza cu user si parssword valide
    # - click login
    # - Verifica faptul ca noul URL contine stringul "secure"
    # - Foloseste un explicit wait pentru elementul cu clasa "flash success"
    # - Verifica daca elementul cu clasa 'flash success' este displayed
    # - Verifica daca mesajul de pe acest element CONTINE textul 'secure area'


    def test_verifica_string_secure(self):
        username = self.driver.find_element(*self.USERNAME)
        username.send_keys(*self.User_corect)

        password = self.driver.find_element(*self.PASSWORD)
        password.send_keys(*self.Pass_corect)

        self.driver.find_element(*self.BUTTON_LOGIN).click()

        # self.assertTrue("secure" in self.driver.current_url, "Linkul nu este bun")

        # sau

        self.assertIn("secure", self.driver.current_url, "Linkul nu este corect")

        wait = WebDriverWait(self.driver, 3)
        flash = wait.until(EC.visibility_of_element_located((By.ID, "flash")))

        # Verifică dacă elementul este afișat
        self.assertTrue(flash.is_displayed(), "Elementul cu clasa 'flash success' nu este afișat.")

        # Verifică dacă textul de pe element conține "secure area"
        self.assertIn("secure area", flash.text, "Mesajul nu conține textul 'secure area'.")


    #Test 11
    # completeaza cu user si pass valide;
    # click login
    # click logout
    # verifica daca ai ajuns pe https://the-internet.herokuapp.com/login
    @unittest.skip
    def test_verifica_url_initial(self):
        username = self.driver.find_element(*self.USERNAME)
        username.send_keys(*self.User_corect)

        password = self.driver.find_element(*self.PASSWORD)
        password.send_keys(*self.Pass_corect)

        self.driver.find_element(*self.BUTTON_LOGIN).click()

        self.driver.find_element(By.XPATH, '//a[@class="button secondary radius"]').click()

        self.assertEqual(self.driver.current_url, self.LOGIN_LINK , "Linkul nu este la fel")


