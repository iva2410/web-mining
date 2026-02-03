import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import random
import csv

def human_delay(min_sec=12, max_sec=18):
    time.sleep(random.uniform(min_sec, max_sec))

# Lista gradova 
destinacije = {
    "London": "https://www.tripadvisor.com/Restaurants-g186338-London_England.html",
    "Paris": "https://www.tripadvisor.com/Restaurants-g187147-Paris_Ile_de_France.html",
    "Rome": "https://www.tripadvisor.com/Restaurants-g187791-Rome_Lazio.html",
    "Beograd": "https://www.tripadvisor.com/Restaurants-g294472-Belgrade.html",
    "Madrid": "https://www.tripadvisor.com/Restaurants-g187514-Madrid.html",
    "Berlin": "https://www.tripadvisor.com/Restaurants-g187323-Berlin.html"
}

driver = uc.Chrome(version_main=143)

try:
    with open('recenzije_restorana.csv', mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Restoran', 'Grad', 'Ocena', 'Recenzija']) 

        for grad, link_grada in destinacije.items():
            print(f"\n>>> Prelazim na grad: {grad} <<<")
            driver.get(link_grada)
            human_delay(10, 15)
            
            driver.execute_script("window.scrollTo(0, 800);")
            time.sleep(3)

            elementi = driver.find_elements(By.XPATH, "//a[contains(@href, 'Restaurant_Review-')]")
            linkovi = list(set([el.get_attribute("href") for el in elementi if el.get_attribute("href")]))[:15]

            for l in linkovi:
                print(f"Ulazim u: {l.split('-')[-2]} ({grad})")
                driver.get(l)
                human_delay(15, 22)

                try:
                    ime = driver.find_element(By.TAG_NAME, "h1").text
                except:
                    ime = "Restoran"

                try:
                    rating_div = driver.find_element(By.CSS_SELECTOR, 'div[data-automation="bubbleRatingValue"]')
                    ocena = rating_div.find_element(By.TAG_NAME, "span").text
                except:
                    ocena = "N/A"

                spanovi = driver.find_elements(By.TAG_NAME, "span")
                brojac_recenzija = 0
                for s in spanovi:
                    tekst = s.text.strip()
                    if len(tekst) > 70 and "subjective opinion" not in tekst and "trust & safety" not in tekst:
                        writer.writerow([ime, grad, ocena, tekst])
                        brojac_recenzija += 1
                
                f.flush() 
                print(f"--- Završeno: {ime} | Ocena: {ocena} | Recenzija: {brojac_recenzija}")
                
                # Odmaranje 
                time.sleep(random.randint(7, 12))

except Exception as e:
    print(f"Došlo je do prekida: {e}")

finally:
    driver.quit()