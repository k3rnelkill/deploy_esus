#pip install selenium
#pip install webdriver-manager --break-system-packages

#from time import sleep
import paramiko
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def iniciar_driver():
    chrome_options = Options()
    prefs = {
        # Alterar o local padrão de download de arquivos
        'download.default_directory': r"/root/temporario/",
        #'download.default_directory': 'C:\\Users\\ThiagoMarques\\Downloads',
        # notificar o google chrome sobre essa alteração
        'download.directory_upgrade': True,
        # Desabilitar a confirmação de download
        'download.prompt_for_download': False,
        # Desativar popups
        'profile.default_content_settings.popups': 0,
        # Desabilitar notificações
        'profile.default_content_setting_values.notifications': 2,
        # Permitir multiplos downloads
        'profile.default_content_setting_values.automatic_downloads': 1,
         # Habilitar navegação segura
        'safebrowsing.enabled': True,
    }

    # Adicionar opções headless
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--headless")  # Executar em modo headless
    chrome_options.add_argument("--disable-gpu")  # Necessário para o modo headless em alguns sistemas
    chrome_options.add_argument("--window-size=1920,1080")  # Definir o tamanho da janela
    chrome_options.add_argument("--no-sandbox")  # Para evitar problemas de permissão em alguns sistemas
    chrome_options.add_argument("--disable-dev-shm-usage")  # Para evitar problemas de recursos em contêineres

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

driver = iniciar_driver()
driver.get('https://sisaps.saude.gov.br/esus/')

botao_download = driver.find_element(By.XPATH,'//*[@id="monthly"]/div/ul[2]/li[4]/a')
#botao_download.click()

if botao_download is not None:
    print('xpath foi encontrado!')
    #print(botao_download.get_attribute('href'))#PEGANDO URL
    link_download = botao_download.get_attribute('href') #COLOCANDO EM VARIAVEL
    #print(link_download)#PRINT DE TESTE

#input('') #não estava feixando até ter um click
driver.close()

print(link_download)#PRINT DE TESTE

# Dados do servidor ESUS, adiciona a chave ao servidor de destino, caso não queira utilizar senha.
hostname = 'IPDOSERVIDOR'
port = 22
username = 'USUARIO'

# Conectando ao servidor
client = paramiko.SSHClient()
# Aceitar a chave do host automaticamente
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, port, username)

# Limpando arquivos antigos
comando_clean_file = f'rm -fv /root/temporario/eSUS-AB-PEC.jar'
stdin, stdout, stderr = client.exec_command(comando_clean_file)

# Executando download do esus atual
comando_get_link = f'curl {link_download} --output /root/temporario/eSUS-AB-PEC.jar'
stdin, stdout, stderr = client.exec_command(comando_get_link)


# Capturando e imprimindo a saída
print("Saída:")
print(stdout.read().decode())

print("Erros (se houver):")
print(stderr.read().decode())

# Fechando a conexão
client.close()