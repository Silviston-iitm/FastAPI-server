from fastapi import FastAPI, File, UploadFile, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import csv
import io
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

VALID_TOKEN = "84y69useuinziis0"
MAX_SIZE = 93 * 1024  # 93 KB
ALLOWED_EXTENSIONS = {".csv", ".json", ".txt"}


@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        x_upload_token_1848: str = Header(None),
):
    # Auth check
    if not x_upload_token_1848 or x_upload_token_1848 != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    filename = file.filename or ""
    ext = os.path.splitext(filename)[1].lower()

    # File type check
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Bad Request")

    contents = await file.read()

    # Size check
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="Payload Too Large")

    # CSV processing
    if ext == ".csv":
        try:
            text = contents.decode("utf-8")
        except:
            raise HTTPException(status_code=400, detail="Invalid CSV encoding")

        reader = csv.DictReader(io.StringIO(text))
        rows = list(reader)

        columns = list(rows[0].keys()) if rows else []

        total_value = 0.0
        category_counts = {}

        if "value" in columns and "category" in columns:
            for row in rows:
                total_value += float(row["value"])
                cat = row["category"]
                category_counts[cat] = category_counts.get(cat, 0) + 1

        total_value = round(total_value, 2)

        return {
            "email": "24f1002710@ds.study.iitm.ac.in",
            "filename": filename,
            "rows": len(rows),
            "columns": columns,
            "totalValue": total_value,
            "categoryCounts": category_counts,
        }

    # Non-CSV files
    return {
        "email": "24f1002710@ds.study.iitm.ac.in",
        "filename": filename,
        "message": "File accepted",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)