import os
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from pydantic import BaseModel, Field
from typing import List

# Import the core logic from your working classify.py file
from classify import classify_log, classify

app = FastAPI(
    title="Log Analysis Automation API",
    description="REST API for scalable, automated log classification using a hybrid Regex, BERT, and LLM pipeline.",
    version="1.0.0"
)

# Ensure the resources folder exists so CSV operations never crash
os.makedirs("resources", exist_ok=True)

# ─── Pydantic Data Models (Defines the expected JSON structure) ───
class LogRequest(BaseModel):
    source: str = Field(..., example="ModernHR")
    log_message: str = Field(..., example="Admin access escalation detected for user 9429.")

class LogResponse(BaseModel):
    source: str
    log_message: str
    predicted_label: str

class BatchLogRequest(BaseModel):
    logs: List[LogRequest]

class BatchLogResponse(BaseModel):
    total_processed: int
    results: List[LogResponse]


# ─── API Endpoints ───

@app.get("/", include_in_schema=False)
def root():
    """Fixes the 404 error by redirecting the base URL straight to the UI."""
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["System Maintenance"])
def health_check():
    """Simple health check to verify the server is live."""
    return {"status": "Active", "message": "Log Analysis API is up and running!"}

@app.post("/classify/single", response_model=LogResponse, tags=["Log Classification"])
def classify_single_log(request: LogRequest):
    """Processes a single log message through the pipeline."""
    try:
        label = classify_log(request.source, request.log_message)
        return LogResponse(
            source=request.source,
            log_message=request.log_message,
            predicted_label=label
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@app.post("/classify/batch", response_model=BatchLogResponse, tags=["Log Classification"])
def classify_batch_logs(request: BatchLogRequest):
    """Processes an entire JSON array of logs (Scalable Automation)."""
    try:
        # Convert request logs into the list of tuples your classify() function expects
        log_pairs = [(log.source, log.log_message) for log in request.logs]
        labels = classify(log_pairs)
        
        results = []
        for i, log in enumerate(request.logs):
            results.append(LogResponse(
                source=log.source,
                log_message=log.log_message,
                predicted_label=labels[i]
            ))
        
        return BatchLogResponse(total_processed=len(results), results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch processing failed: {str(e)}")

@app.post("/classify/csv", tags=["Bulk Operations"])
async def classify_csv_file(file: UploadFile = File(...)):
    """Upload a CSV with 'source' and 'log_message' columns to download a classified version."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Uploaded file must be a .csv")
        
    try:
        df = pd.read_csv(file.file)
        if "source" not in df.columns or "log_message" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'source' and 'log_message' headers.")
            
        # Run classification
        log_pairs = list(zip(df["source"], df["log_message"]))
        df["target_label"] = classify(log_pairs)
        
        # Save locally and return the file to the user
        output_path = f"resources/classified_{file.filename}"
        df.to_csv(output_path, index=False)
        
        return FileResponse(path=output_path, filename=f"classified_{file.filename}", media_type='text/csv')
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process CSV: {str(e)}")
    finally:
        file.file.close()


if __name__ == "__main__":
    import uvicorn
    # Bound explicitly to localhost to prevent Windows routing errors
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)