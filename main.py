import re
import smtplib
from dotenv import dotenv_values
from email.message import EmailMessage
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Coleta informações do arquivo .env / Variáveis
emails_list = []
email_body = """Olá, tudo bem? 👋

Me chamo Lucas Monte Santo e sou um desenvolvedor backend com paixão por Python e automações. Inclusive, você está lendo um email gerado automaticamente por um código que criei, e eu também encontrei seu perfil no LinkedIn através de um webscraping que desenvolvi em Python! 😄

Atualmente, estou cursando Engenharia da Computação pela Univesp e tenho formação técnica em Desenvolvimento de Sistemas. No meu dia a dia, trabalho com diversas tecnologias como SQL, NoSQL (MongoDB), frameworks como Flask e Kivy, e automações com Selenium e BeautifulSoup. Também sou familiarizado com Linux, Git e testes de APIs com Postman.

Busco uma oportunidade para aplicar esses conhecimentos e aprender ainda mais. Se eu puder deixar meu currículo para sua análise, ficaria muito grato! 😊. Se você não for um recrutador, mas conhecer um e puder deixar o meu currículo com ele, eu ficaria extremamente grato 😁.

Agradeço pela atenção e espero que possamos fazer um "match" em breve!

Atenciosamente,
Lucas Monte Santo"""
email_title = "Olá! Um Dev Python Automatizado por Aqui! 🐍"
env = dotenv_values(".env")
EMAIL = env["EMAIL"]
PASS = env["EMAIL_PASSWORD"]
APP = env["APP_PASSWORD"]

# Inicia o selenium
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://duckduckgo.com")
sleep(2)

# Digita os dorks na caixa de pesquisa
# Duck Duck Go
search_box = driver.find_element(By.XPATH, '//*[@id="searchbox_input"]')
search_box.send_keys(
    """
    intext:"@gmail" OR "@hotmail" OR "@outlook" site:linkedin.com/in !safeoff
    """
)

# Clica no botão 'More Results'
while True:
    try:
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="more-results"]'))
        )
        driver.find_element(By.XPATH, '//*[@id="more-results"]').click()

    except:
        break

# Coleta todos os links da página
links = driver.find_elements(By.TAG_NAME, "a")
list_links = []

# Separa os links do linkedin
for link in links:
    try:
        link = link.get_attribute("href")
        if "linkedin.com/in" in link:
            list_links.append(link)
    except TypeError:
        ...

# Cria um set de links
list_links = set(list_links)
print(list_links, end="\n\n")

# Executa o login no linkedin
driver.get("https://linkedin.com")

sleep(2)

driver.find_element(
    By.XPATH, '//*[@id="main-content"]/section[1]/div/div/div[2]/a'
).click()

sleep(2)

driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(EMAIL)

sleep(2)

driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(PASS)

sleep(1)

try:
    WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'))
    )
    driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()
except:
    WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[4]/button'))
    )
    driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[4]/button').click()


# Acessa cada link coletado no DuckDuckGO
for l in list_links:
    driver.get(l)

    sleep(5)

    html = driver.page_source
    emails_set = set(
        re.findall(r"[a-zA-Z0-9._%+-]+\@[gmail|hotmail|outlook]+\.[a-zA-Z]{2,3}", html)
    )

    for email in emails_set:
        emails_list.append(email)

    sleep(2)

# Envia emails automáticos para cada endereço listado acima
for email in emails_list:
    try:
        msg = EmailMessage()
        msg["Subject"] = email_title
        msg["From"] = EMAIL
        msg["To"] = email
        msg.set_content(email_body)

        with open("contents/Curriculo_Programador.pdf", "rb") as file:
            content = file.read()
            msg.add_attachment(
                content,
                maintype="application",
                subtype="pdf",
                filename="Curriculo_Programador.pdf",
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, APP)
            smtp.send_message(msg)

    except Exception as e:
        print(f"Erro no envio de emails: {e}")
