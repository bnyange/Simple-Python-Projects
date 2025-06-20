from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_fibe_partners():
    driver_path = "C:/Users/blais/OneDrive/Desktop/Job/chromedriver-win64/chromedriver.exe"
    driver = webdriver.Chrome(service=Service(driver_path))
    driver.get("https://www.fibe-berlin.com/en/partners/partners-sponsors/")
    
    try:
        print("Page loaded, waiting for content...")
        time.sleep(5)  # Initial wait for dynamic content

        # Handle cookie popup
        print("Checking for cookie popup...")
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='uc-accept-all-button']"))
            ).click()
            print("Cookie popup clicked (data-testid).")
        except:
            print("Trying text-based fallback...")
            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
                ).click()
                print("Cookie popup clicked (text).")
            except:
                print("No cookie popup found, moving on.")

        # Wait for partners section
        print("Waiting for partners section...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "content_abschnitt_6_id"))
        )

        # Extract partner links
        print("Extracting partner data...")
        partner_links = driver.find_elements(By.CSS_SELECTOR, "#content_abschnitt_6_id a.link-extern-image")
        data = [
            {
                "Company": link.find_element(By.TAG_NAME, "img").get_attribute("alt").replace(" Logo", "").strip(),
                "Homepage URL": link.get_attribute("href"),
                "LinkedIn Search URL": f"https://www.linkedin.com/search/results/companies/?keywords={link.find_element(By.TAG_NAME, 'img').get_attribute('alt').replace(' ', '%20').replace(' Logo', '')}",
                "Email": ""
            }
            for link in partner_links if link.get_attribute("href")
        ]

        # Save to Excel
        if data:
            pd.DataFrame(data).to_excel("fibe_partners.xlsx", index=False)
            print(f"Saved {len(data)} partners to fibe_partners.xlsx")
        else:
            print("No partners found.")

    except Exception as e:
        print(f"Error: {e}")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Saved page source to page_source.html.")
    finally:
        driver.quit()

scrape_fibe_partners()
