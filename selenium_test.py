import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumStart():
    def __init__(self, spisok_csv: list[str]):
        self.spisok_csv = spisok_csv
        self.slovar = dict()
        binary = './FirefoxPortable/App/Firefox64/Firefox.exe'
        driver = './FirefoxPortable/geckodriver-v0.33.0-win64/geckodriver.exe'
        service = Service(executable_path=driver)
        options = webdriver.FirefoxOptions()
        options.binary_location = binary
        self.driver = webdriver.Firefox(service=service, options=options)

    # windows 64 bit
    def start_selenium(self):
        self.driver.get("https://www.megaputer.ru/produkti/sertifikat/")
        for i in self.spisok_csv:
            span_element = self.driver.find_element(By.ID, 'certificates-text')
            span_element.clear()
            span_element.send_keys(" ".join(i))
            self.driver.implicitly_wait(2.6)
            button_element = self.driver.find_element(By.ID, 'certificates-button')
            button_element.click()
            time.sleep(2)
            self.driver.implicitly_wait(2.6)
            xpa1 = self.driver.find_element(By.ID, 'text1')
            # print(xpa1.find_elements(By.XPATH, '//table/tbody/tr[1]/td[2]'))
            if xpa1.text == "По данному запросу ничего не найдено":
                self.slovar.setdefault(' '.join(i), [])
            else:
                try:
                    name = ' '.join(i)
                    for j in range(1, 100):
                        if j == 1:
                            kurs = (self.driver.find_element(By.XPATH, '//tr[1]/td[2]'))
                            data = self.driver.find_element(By.XPATH, '//tr[1]/td[3]')
                            self.slovar.setdefault(name, []).append((kurs.text, (datetime.strptime(data.text, "%d.%m.%Y"))))
                        else:
                            kurs = (self.driver.find_element(By.XPATH, f'//tr[{j}]/td[1]'))
                            data = self.driver.find_element(By.XPATH, f'//tr[{j}]/td[2]')
                            self.slovar.setdefault(name, []).append((kurs.text, (datetime.strptime(data.text, "%d.%m.%Y"))))
                except:
                    pass
        self.driver.quit()
        return self.slovar