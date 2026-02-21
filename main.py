print("Version 2 Deploy")
from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.responses import JSONResponse
import csv
from io import StringIO

app = FastAPI()

MAX_FILE_SIZE = 85 * 1024
VALID_TOKEN = "winh3cmzs8lkxiqy"

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Headers": "*",
}

@app.options("/upload")
async def options_upload():
    return JSONResponse(content={}, headers=CORS_HEADERS)

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_3535: str = Header(None)
):
    if x_upload_token_3535 != VALID_TOKEN:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized"},
            headers=CORS_HEADERS
        )

    if not file.filename.endswith((".csv", ".json", ".txt")):
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid file type"},
            headers=CORS_HEADERS
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        return JSONResponse(
            status_code=413,
            content={"detail": "File too large"},
            headers=CORS_HEADERS
        )

    text_data = contents.decode("utf-8")
    csv_reader = csv.DictReader(StringIO(text_data))
    rows = list(csv_reader)

    total_value = sum(float(row["value"]) for row in rows)
    category_counts = {}
    for row in rows:
        cat = row["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

    return JSONResponse(
        content={
            "email": "24f3003942@ds.study.iitm.ac.in",
            "filename": file.filename,
            "rows": len(rows),
            "columns": csv_reader.fieldnames,
            "totalValue": round(total_value, 2),
            "categoryCounts": category_counts
        },
        headers=CORS_HEADERS
    )
