import os
import time
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import logging
from random import uniform

# Configure logging
logging.basicConfig(
    filename='logs/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def scrape_products():
    query = entry.get()
    if not query:
        messagebox.showwarning("Input Required", "Please enter a product name.")
        return

    # Ensure folders exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Disabled for debugging
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    products = []
    errors = []

    # Initialize WebDriver
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        wait = WebDriverWait(driver, 15)
    except Exception as e:
        messagebox.showerror("WebDriver Error", str(e))
        logging.error(f"WebDriver initialization failed: {e}")
        return

    # -------- AMAZON SCRAPING --------
    try:
        amazon_url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
        driver.get(amazon_url)
        time.sleep(uniform(2, 4))
        
        # Wait for results to load
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 's-result-item')]")))
        except Exception as e:
            errors.append(f"Amazon results not loading: {e}")
            logging.warning(f"Amazon results not loading: {e}")

        results = driver.find_elements(By.XPATH, "//div[contains(@class, 's-result-item') and .//h2]")[:10]
        
        for item in results:
            try:
                # Product Name
                name = item.find_element(By.XPATH, ".//h2//span").text
                
                # Price
                try:
                    price = item.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
                except:
                    price = "N/A"
                
                # Rating
                rating = "N/A"
                try:
                    rating_element = item.find_element(By.XPATH, ".//span[contains(@class,'a-icon-alt')]")
                    rating = rating_element.get_attribute("innerHTML").split()[0]
                except:
                    pass
                
                # URL
                try:
                    url = item.find_element(By.XPATH, ".//a[@class='a-link-normal s-no-outline']").get_attribute("href")
                except:
                    url = "N/A"
                
                products.append(["Amazon", name, price, rating, url])
            except Exception as e:
                errors.append(f"Amazon product error: {e}")
                continue
    except Exception as e:
        errors.append(f"Amazon scraping failed: {e}")
        logging.error(f"Amazon scraping error: {e}")

    # -------- CROMA SCRAPING (FIXED URL AND RATINGS) --------
# -------- UPDATED CROMA SCRAPING SECTION --------
    try:
        croma_url = f"https://www.croma.com/searchB?q={query.replace(' ', '%20')}%3Arelevance&text={query.replace(' ', '%20')}"
        driver.get(croma_url)
        time.sleep(uniform(3, 5))
        
        # Accept cookies if popup appears
        try:
            accept_cookies = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Accept') or contains(@class,'accept-cookies')]")))
            accept_cookies.click()
            time.sleep(1)
        except:
            pass

        # Wait for results to load
        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'product-list')]")))
            time.sleep(2)  # Additional wait for dynamic content
        except Exception as e:
            errors.append(f"Croma results not loading: {e}")
            logging.warning(f"Croma results not loading: {e}")

        # Get all product items
        results = driver.find_elements(By.XPATH, "//li[contains(@class,'product-item')]")[:10]
        
        for item in results:
            try:
                # Product Name
                try:
                    name = item.find_element(By.XPATH, ".//h3[contains(@class,'product-title')]").text.strip()
                except:
                    name = "N/A"

                # Price
                try:
                    price = item.find_element(By.XPATH, ".//span[contains(@class,'amount')]").text.strip()
                except:
                    price = "N/A"

                # RATING (FIXED TO EXCLUDE COMPANY NAMES)
                rating = "N/A"
                try:
                    # First try to find the rating number directly
                    rating_divs = item.find_elements(By.XPATH, ".//div[contains(@class,'rating') or contains(@class,'stars')]")
                    for div in rating_divs:
                        # Skip if it contains "Reviews" or looks like a brand name
                        if 'review' in div.text.lower() or 'rated' in div.text.lower():
                            continue
                        # Check for numeric rating (4.3, 5, etc.)
                        if any(char.isdigit() for char in div.text):
                            rating = ''.join(c for c in div.text if c.isdigit() or c == '.')
                            rating = rating[:3]  # Take only first 3 chars (4.5)
                            break
                        
                    # If not found, try getting from title attribute
                    if rating == "N/A":
                        rating_elements = item.find_elements(By.XPATH, ".//*[@title and contains(translate(@title, 'RATED', 'rated'), 'rated')]")
                        for element in rating_elements:
                            title = element.get_attribute("title")
                            if 'rated' in title.lower():
                                rating = ''.join(c for c in title if c.isdigit() or c == '.')
                                rating = rating[:3]
                                break
                except:
                    pass

                # URL
                url = "N/A"
                try:
                    url_elements = item.find_elements(By.XPATH, ".//a[contains(@href,'/p/')] | .//a[contains(@class,'product__link')]")
                    for element in url_elements:
                        url = element.get_attribute("href")
                        if url:
                            if url.startswith("/"):
                                url = "https://www.croma.com" + url
                            break
                except:
                    pass

                products.append(["Croma", name, price, rating, url])
            except Exception as e:
                errors.append(f"Croma product error: {e}")
                continue
    except Exception as e:
        errors.append(f"Croma scraping failed: {e}")
        logging.error(f"Croma scraping error: {e}")

    driver.quit()

    # Save results
    if products:
        df = pd.DataFrame(products, columns=["Source", "Product Name", "Price", "Rating", "URL"])
        output_path = os.path.join("data", "product_results.xlsx")
        df.to_excel(output_path, index=False)
        
        # Show success message with error summary if any
        msg = f"Successfully saved {len(products)} products to:\n'{output_path}'"
        if errors:
            msg += f"\n\nEncountered {len(errors)} errors during scraping."
            with open(os.path.join("logs", "scraper_errors.log"), "w") as f:
                f.write("\n".join(errors))
        
        messagebox.showinfo("Success", msg)
    else:
        messagebox.showinfo("No Data", "No product details found.\nPossible reasons:\n1. No results for your search\n2. Website structure changed\n3. Blocked by website")

# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("Product Scraper - Amazon & Croma")
root.geometry("500x220")

# Styling
root.configure(bg="#f0f0f0")
font_style = ("Arial", 12)

# Widgets
label = tk.Label(
    root, 
    text="Enter Product Name to Search:", 
    font=font_style,
    bg="#f0f0f0"
)
label.pack(pady=10)

entry = tk.Entry(
    root, 
    width=45,
    font=font_style,
    bd=2,
    relief="groove"
)
entry.pack(pady=5)

button = tk.Button(
    root, 
    text="Search & Export to Excel", 
    command=scrape_products,
    bg="#4CAF50", 
    fg="white", 
    font=font_style,
    padx=15,
    pady=8,
    bd=0,
    activebackground="#45a049"
)
button.pack(pady=20)

root.mainloop()