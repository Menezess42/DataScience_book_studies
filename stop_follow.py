from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# Configurar o navegador
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Acessar a página de empresas seguidas
driver.get("https://www.linkedin.com/mynetwork/network-manager/company/")

# Aguarde o senhor fazer o login manualmente (ou pode implementar via cookies, se preferir)
input("Após o login e a página estiver carregada, pressione ENTER...")

# Rolar a página para carregar mais empresas
for _ in range(10):  # Ajustar conforme o número de empresas
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(2)

# Encontrar todos os botões "Seguindo"
buttons = driver.find_elements(By.XPATH, '//span[text()="Seguindo"]/ancestor::button')

print(f"Encontrados {len(buttons)} botões de 'Seguindo'.")

for button in buttons:
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(1)
        button.click()
        time.sleep(2)

        # Clicar em "Parar de seguir" no pop-up
        unfollow_btn = driver.find_element(By.XPATH, '//span[text()="Parar de seguir"]/ancestor::button')
        unfollow_btn.click()
        time.sleep(2)
    except Exception as e:
        print("Erro ao tentar deixar de seguir:", e)
        continue

print("Processo concluído.")

