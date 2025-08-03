import time
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = FastAPI()

def get_size(number):
    try:
        num = int(number)
        return "Big" if num >= 5 else "Small"
    except:
        return "N/A"

def scrape_data():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get("https://wingoanalyst.com/#/wingo_30s")
    time.sleep(5)

    rows = driver.find_elements(By.CSS_SELECTOR, ".el-table__body-wrapper tr")
    result = []

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 3:
            period = cells[0].text.strip()
            number = cells[1].text.strip()
            color = cells[2].text.strip()
            size = get_size(number)
            result.append({
                "period": period,
                "number": number,
                "size": size,
                "color": color
            })
    
    driver.quit()
    return result

@app.get("/")
def read_root():
    return {"message": "Wingo 30s Scraper API"}

@app.get("/data")
def get_data():
    try:
        data = scrape_data()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
