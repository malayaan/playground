from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # Importation corrigée
import time

# Configuration des options pour Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Ouvrir le navigateur en plein écran (optionnel)

# Chemin vers le ChromeDriver
driver_path = "/chemin/vers/chromedriver"  # Modifie ce chemin selon ton installation
service = Service(driver_path)

# Initialisation du navigateur avec les options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Ouvrir une page web
driver.get("https://www.example.com")

# Attendre quelques secondes pour voir la page
time.sleep(5)

# Fermer le navigateur
driver.quit()