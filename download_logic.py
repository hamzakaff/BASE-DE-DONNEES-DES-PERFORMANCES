# download_logic.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def telecharger_fichiers_depuis_site(url, download_dir, nb_pages=3):
    chrome_options = Options()
    chrome_options.add_argument("--window-position=0,10000")
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(url)

        # Cliquer sur le bouton "Tous"
        bouton_tous = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Tous')]")))
        bouton_tous.click()

        for i in range(1, nb_pages + 1):
            print(f"Téléchargement - Page {i}")
            liens = wait.until(EC.presence_of_all_elements_located((By.LINK_TEXT, "Télécharger")))
            lignes = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr")))

            for lien, ligne in zip(liens, lignes):
                print(f"Téléchargement : {ligne.text}")
                lien.click()

                # Attendre que le fichier soit téléchargé
                while any(fname.endswith(".crdownload") for fname in os.listdir(download_dir)):
                    time.sleep(1)

            # Bouton page suivante
            if i < nb_pages:
                suivant = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{i+1}')]")))
                suivant.click()
                time.sleep(1)

        print("Téléchargement terminé.")
        driver.quit()
        return True

    except Exception as e:
        print(f"Erreur : {e}")
        driver.quit()
        return False
