from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def scrap():

# Setup (optional headless)
    options = Options()

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    def safe_search(css_selector):
        try:
            return driver.find_element(By.CSS_SELECTOR , css_selector).text.strip()
        except:
            return None

    url = "https://world.openfoodfacts.org/facets/categories/meats"
    driver.get(url)

    # Wait until at least one product link is available
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.list_product_a"))
    )

    # Find and print all product URLs
    products = driver.find_elements(By.CSS_SELECTOR, "a.list_product_a")
    links = [product.get_attribute("href") for product in products]
    product_data = []
    for link in links:
        try:
            driver.get(link)
            WebDriverWait(driver , 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"span.field")))
            time.sleep(2)
        except Exception as error:
            print(f"failed to fetch{link}:{error}") 
        selectors = {
            "name": "h2.title-1",
            "quantity": "p#field_quantity span.field_value",
            "brand": "p#field_brands span.field_value a" ,
            "categories": "p#field_categories span.field_value",
            "countries": "p#field_countries span.field_value",
            "nutrition_grade": "li.accordion-navigation h4[class^='grade_']",
            "energy_per_serving": "table tbody tr:nth-child(1) td:nth-child(3) span",
            "fat_per_serving": "table tbody tr:nth-child(2) td:nth-child(3) span",
            "carbohydrates_per_serving": "table tbody tr:nth-child(4) td:nth-child(3) span",
            "protein_per_serving": "table tbody tr:nth-child(7) td:nth-child(3)"
        }

        temp_data = {key:safe_search(selector) for key, selector in selectors.items()}
        energy_raw = temp_data.get("energy_per_serving")
        if energy_raw:
            digits = ''.join(filter(str.isdigit, energy_raw))  # keeps only digits
            temp_data["energy_per_serving"] = digits if digits else None
        product_data.append(temp_data)

    driver.quit()
    return product_data




