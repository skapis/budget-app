from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec
from unittest import skip
from core.models import Transaction
from time import sleep


class TestLoginForm(LiveServerTestCase):

    def setUp(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options,
                                       executable_path=r"C:\Users\jakub\OneDrive\Plocha\chromedriver.exe")
        self.wait = WebDriverWait(self.driver, 5)

    @skip('Not needed now')
    def test_login(self):
        # get login form path
        self.driver.get('http://localhost:8000/en/auth/login/')
        self.user = self.wait.until(ec.visibility_of_element_located((By.NAME, 'username')))
        self.password = self.wait.until(ec.visibility_of_element_located((By.NAME, 'password')))
        self.submit = self.wait.until(ec.visibility_of_element_located((By.ID, 'submitBtn')))
        self.user.send_keys('admin')
        self.password.send_keys('admin')
        self.submit.click()

        try:
            self.wait.until(ec.url_matches('http://localhost:8000/en/dashboard'))
        except:
            print('User login failed')
        finally:
            self.assertURLEqual(self.driver.current_url, 'http://localhost:8000/en/dashboard')


class TestApplicationInterface(LiveServerTestCase):

    def setUp(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options,
                                       executable_path=r"C:\Users\jakub\OneDrive\Plocha\chromedriver.exe")
        self.wait = WebDriverWait(self.driver, 5)
        self.driver.get('http://localhost:8000/en/auth/login/')
        self.user = self.wait.until(ec.visibility_of_element_located((By.NAME, 'username')))
        self.password = self.wait.until(ec.visibility_of_element_located((By.NAME, 'password')))
        self.submit = self.wait.until(ec.visibility_of_element_located((By.ID, 'submitBtn')))
        self.user.send_keys('admin')
        self.password.send_keys('admin')
        self.submit.click()

    @skip('Not needed now')
    def test_create_new_transaction(self):
        # click on button to create new transaction
        self.new_trans_btn = self.wait.until(ec.visibility_of_element_located((By.ID, 'newTransBtn')))
        self.new_trans_btn.click()

        # input values to modal form
        self.amount = self.wait.until(ec.visibility_of_element_located((By.NAME, 'amount')))
        self.description = self.wait.until(ec.visibility_of_element_located((By.NAME, 'description')))
        # add amount
        self.amount.send_keys(25000)
        # add description
        self.description.send_keys('Selenium Test Transaction')
        self.add_btn = self.wait.until(ec.visibility_of_element_located((By.ID, 'submitBtn')))
        self.add_btn.click()

        # check success message after success transaction creation
        self.message = self.wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'alert-success')))
        self.assertEqual(self.message.text, 'Transaction was created')

    @skip('Not needed now')
    def test_delete_transaction(self):
        # locate first transaction in transaction table
        self.trans = self.wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div/div/main/div/div'
                                                                                 '/div[4]/table/tbody/tr[1]')))
        self.del_trans = self.wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div/div/main/div/div'
                                                                                     '/div[4]/table/tbody/tr[1]/td['
                                                                                     '4]/a[2]')))

        # get id of transaction
        self.trans_id = self.trans.get_attribute('id')
        # remove transaction
        self.del_trans.click()
        # check if message with success delete appeared
        self.del_message = self.wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'alert-success')))
        self.assertEqual(self.del_message.text, 'Transaction was removed')

        # check if transaction is not in database
        transaction = Transaction.objects.filter(transactionId=self.trans_id).first()
        self.assertIsNone(transaction)
        print(f'Transaction with {self.trans_id} was removed by selenium')

    def test_change_language(self):
        # locate language switcher
        self.lang_dropdown = self.wait.until(ec.visibility_of_element_located((By.ID, 'navbarDropdown')))
        self.lang_dropdown.click()

        # locate czech language option
        self.czech_lang = self.wait.until(ec.visibility_of_element_located((By.ID, 'cs')))
        self.czech_lang.click()

        # check if user is redirected to url with czech parameter
        self.assertURLEqual(self.driver.current_url, 'http://localhost:8000/cs/dashboard')

    def test_change_currency(self):
        # get balance to check current currency symbol
        self.balance = self.wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div/div/main/div/div'
                                                                                   '/div[2]/div[1]/div/div['
                                                                                   '2]/div/div/h3')))
        self.current_currency_symbol = self.balance.text.split(' ')[1]
        # get account url
        self.driver.get('http://localhost:8000/en/account')
        # locate select of currencies and change to EUR
        self.c_select = self.wait.until(ec.visibility_of_element_located((By.NAME, 'currency')))
        self.currencies = Select(self.c_select)

        self.selected_currency = self.currencies.first_selected_option
        self.options_list = list(map(lambda item: item.get_attribute('value'), self.currencies.options))
        self.options_list.remove(self.selected_currency.get_attribute('value'))

        # select different currency and submit a new currency selection
        self.currencies.select_by_value(self.options_list[0])
        self.submit_btn = self.wait.until(ec.visibility_of_element_located((By.ID, 'submitBtn')))
        self.submit_btn.click()

        # after submit, check if the currency symbol is different
        self.driver.get('http://localhost:8000/en/dashboard')
        self.balance = self.wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div/div/main/div/div'
                                                                                   '/div[2]/div[1]/div/div['
                                                                                   '2]/div/div/h3')))
        print(self.balance.text.split(' ')[1])
        self.assertNotEqual(self.current_currency_symbol, self.balance.text.split(' ')[1])
