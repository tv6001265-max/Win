from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = FastAPI()

def get_size(number):
    try:
        return "Big" if int(number) >= 5 else "Small"
    except:
        return "N/A"

def scrape_data():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Use correct path if needed: executable_path='/path/to/chromedriver'
    driver = webdriver.Chrome(options=options)
    driver.get("https://wingoanalyst.com/#/wingo_30s")

    time.sleep(5)  # Wait for table to load

    rows = driver.find_elements(By.CSS_SELECTOR, ".el-table__body-wrapper tr")
    data = []

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 3:
            period = cells[0].text.strip()
            number = cells[1].text.strip()
            color = cells[2].text.strip()
            size = get_size(number)
            data.append({
                "period": period,
                "number": number,
                "size": size,
                "color": color
            })

    driver.quit()
    return data

@app.get("/data")
def get_wingo_data():
    try:
        return {"status": "success", "data": scrape_data()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
        
