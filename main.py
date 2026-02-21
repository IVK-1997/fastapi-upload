from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
from io import StringIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 85 * 1024
VALID_TOKEN = "winh3cmzs8lkxiqy"

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_3535: str = Header(None)
):

    if x_upload_token_3535 != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not file.filename.endswith((".csv", ".json", ".txt")):
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    if file.filename.endswith(".csv"):
        text_data = contents.decode("utf-8")
        csv_reader = csv.DictReader(StringIO(text_data))

        rows = list(csv_reader)
        row_count = len(rows)
        columns = csv_reader.fieldnames

        total_value = 0
        category_counts = {}

        for row in rows:
            total_value += float(row["value"])
            category = row["category"]
            category_counts[category] = category_counts.get(category, 0) + 1

        return {
            "email": "24f3003942@ds.study.iitm.ac.in",
            "filename": file.filename,
            "rows": row_count,
            "columns": columns,
            "totalValue": round(total_value, 2),
            "categoryCounts": category_counts
        }

    return {"message": "File validated successfully"}
