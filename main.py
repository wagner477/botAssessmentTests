import os
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

pathToChromeDriver = 'chromedriver.exe'


# -----------------------------Login-------------------------------------------
username = str(input('Digite seu username:\n'))
password = str(input('Digite sua senha:\n'))

os.system('cls' or 'clear')

print("""Selecione o assessment:
      [1] - Burnout
      [2] - Estresse
      [3] - Satisfação com a vida
      [4] - Autoconsciência
      [5] - Autoregulação""")

choice = int(input('Digite o número do assessment: '))


# -----------------------------------------------------------------------------

options = webdriver.ChromeOptions()
options.add_argument('--disable-infobars')
options.add_argument("--kiosk-printing")

driver = webdriver.Chrome(chrome_options=options,
                          executable_path=pathToChromeDriver)
driver.delete_all_cookies()

# Ajuste no tempo de espera para o elemento ser encontrado em segundos
wait = WebDriverWait(driver, 8)


driver.get('https://mobile-dev.wayminder.com.br/login?returnPath=%2Fhome')


# Função para selecionar um elemento e clicar nele a partir do XPATH
def selectAndClick(path: str):
    element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, path)
    ))
    element.click()


def main():
    login()
    while True:
        selectAssessment(choice)


def login():
    usernameInput = wait.until(EC.element_to_be_clickable(
        (By.XPATH,
         '/html/body/div[1]/div/div/div[1]/div[3]/div/form/div/input')
    ))

    usernameInput.send_keys(username)

    # Click no botão prosseguir
    selectAndClick('//*[@id="__layout"]/div/div[1]/div[3]/div/form/button')

    passwordInput = wait.until(EC.element_to_be_clickable(
        (By.XPATH,
         '/html/body/div[1]/div/div/div[1]/div[3]/div/form/div[2]/input')
    ))

    passwordInput.send_keys(password)

    # Click no botão de entrar
    selectAndClick('/html/body/div[1]/div/div/div[1]/div[3]/div/form/button')


def selectAssessment(index: int):

    # Click no botão nova jornada
    selectAndClick('/html/body/div[1]/div/div/main/div[1]/div[2]/button')

    # Selecionar o assessment a partir do index
    selectAndClick(
        f'//*[@id="__layout"]/div/main/div[1]/div/div[2]/button[{index}]')

    # Click no botão iniciar assessment
    selectAndClick(
        '//*[@id="__layout"]/div/main/div[1]/div/div/div[3]/button[1]')

    while True:
        num = randint(1, 4)
        try:
            selectAndClick(
                f'''//*[@id="__layout"]/div/div/div[2]/div/div[1]/div[2]
                /div/a[{num}]''')

        except TimeoutException:
            break

    driver.get('https://mobile-dev.wayminder.com.br/home')


if __name__ == '__main__':
    main()
