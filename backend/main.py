import asyncio
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from backend.services import pipeline_service
import json

app = FastAPI(title="AI Lead Pipeline API", version="3.2")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/leads/process")
async def process_leads(
    file: UploadFile = File(...),
    company_context: str = Form(...),
    custom_properties: str = Form(...) # JSON list string of custom column names
):
    contents = await file.read()
    df = pipeline_service.parse_file(contents, file.filename.lower())
    
    properties_list = json.loads(custom_properties)

    rows_with_index = []
    for idx, row in df.iterrows():
        row_dict = row.to_dict()
        row_dict["row_index"] = idx
        rows_with_index.append(row_dict)

    # 1) 40-profile batching per single prompt chunk
    chunk_size = 40
    chunks = [rows_with_index[i:i + chunk_size] for i in range(0, len(rows_with_index), chunk_size)]

    all_results = {}

    for i, chunk in enumerate(chunks):
        # Run batch analysis
        results = await asyncio.to_thread(
            pipeline_service.evaluate_lead_batch, chunk, company_context, properties_list
        )
        for res in results:
            idx = res.get("row_index")
            if idx is not None:
                all_results[idx] = res
        
        # 2) 5-second sleep pacing between chunks to completely eliminate 429 errors
        if i < len(chunks) - 1:
            await asyncio.sleep(5.0)

    # Reassemble dynamic properties into dataframe columns
    for prop in properties_list:
        col_values = []
        for idx in range(len(df)):
            res = all_results.get(idx, {})
            col_values.append(res.get(prop, "N/A"))
        df[prop] = col_values

    output_stream = pipeline_service.dataframe_to_csv_stream(df)
    
    return StreamingResponse(
        output_stream,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=qualified_leads_enriched.csv"}
    )