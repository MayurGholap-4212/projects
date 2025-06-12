
# **Product Scraper - Amazon & Croma**

## **📌 Overview**

This Python-based web scraper extracts product details (name, price, rating, and URL) from **Amazon India** and **Croma** and saves them in an Excel file. The application features a **user-friendly GUI** built with **Tkinter** and uses **Selenium** for web scraping.

---

## **✨ Features**

✅ **Dual-Platform Scraping** - Fetches data from **Amazon** and **Croma**
✅ **Excel Export** - Saves results in `product_results.xlsx`
✅ **Rating Validation** - Ensures ratings are between **1-5** (ignores irrelevant numbers)
✅ **Error Handling** - Logs errors for debugging
✅ **User-Friendly GUI** - Simple interface for easy interaction
✅ **Headless Mode** - Runs Chrome in the background (optional)

---

## **⚙️ Installation**

### **Prerequisites**

* **Python 3.8+**
* **Google Chrome** (for Selenium WebDriver)

### **Steps**

1. **Clone the repository**
   * git clone
   * cd product-scraper
2. **Install dependencies**
   * pip install -r requirements.txt
3. **Run the application**
   * python main.py

## **📂 Project Structure**

```
product-scraper/
├── data/                   # Output Excel files
│   └── product_results.xlsx  
├── logs/                   # Error logs
│   ├── scraper.log    
│   └── scraper_errors.log  
├── main.py                 # Main script (GUI + Scraper)
└── README.md               # This file
```


## **🛠️ How It Works**

### **1. Amazon Scraping**

* Searches for products using the query.
* Extracts:
  * **Product Name**
  * **Price**
  * **Rating** (1-5 scale)
  * **Product URL**

### **2. Croma Scraping**

* Uses **smart rating detection** to avoid capturing irrelevant numbers.
* Extracts:
  * **Product Name**
  * **Price**
  * **Valid Rating** (only between 1-5)
  * **Product URL**

### **3. Excel Export**

* Results are saved in `data/product_results.xlsx` with columns:
  * **Source** (Amazon/Croma)
  * **Product Name**
  * **Price**
  * **Rating**
  * **URL**

---

## **🔧 Customization**

### **Modify Search Behavior**

* **Change wait times** (in `main.py`):
  * time.sleep(uniform(2, 4))  # Adjust delay between page loads
* **Enable/Disable Headless Mode** (for debugging):
  * chrome_options.add_argument("--headless")  # Comment to see browser

### **Add More Retailers**

* To scrape additional websites (e.g., Flipkart), add a new scraping function following the same structure.

---

## **🚨 Troubleshooting**

| **Issue**                   | **Solution**                                                 |
| --------------------------------- | ------------------------------------------------------------------ |
| **No data in Excel**        | Check `logs/scraper_errors.log` for errors                       |
| **Croma ratings incorrect** | Update XPaths in `main.py` for latest website structure          |
| **ChromeDriver issues**     | Ensure Chrome is updated and matches `webdriver_manager` version |

---

## **📜 License**

This project is open-source under the  **MIT License** .
