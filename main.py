from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
import mysql.connector
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="wingo"
    )

@app.get("/api/latest-draw")
def get_latest_draw():
    try:
        # Run the scraper script
        result = subprocess.run(
            ["python", "scrape_latest.py"],
            capture_output=True,
            text=True,
            timeout=20
        )

        if result.returncode != 0:
            return {
                "error": "Scraper failed",
                "stderr": result.stderr.strip()
            }

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON from scraper: {str(e)}"}

        # Save to MySQL
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO results (draw_number, result_number, size, color, created_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    data["draw_number"],
                    data["result_number"],
                    data["size"],
                    data["color"],
                    datetime.now()
                )
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()

        return data

    except Exception as e:
        return {"error": f"API error: {str(e)}"}
