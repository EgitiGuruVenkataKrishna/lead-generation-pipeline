# ⚡ AI Lead Intelligence Hub & Qualification Pipeline

An enterprise-grade, high-performance B2B lead qualification and personalization platform built with **FastAPI**, **Streamlit**, and **Google Gemini AI**. 

Designed to process large customer datasets (CSV/Excel) efficiently while bypassing LLM rate limits through intelligent multi-row batching and request pacing.

---

## 🚀 Key Features

* **Zero-Mapping CSV/Excel Ingestion**: Instantly parses raw lead files with automatic error-handling and data cleaning.
* **40-Profile Batch Processing**: Groups customer records into structured batch payloads to reduce API calls by 90% and conserve Token-Per-Minute (TPM) limits.
* **Dynamic Custom Properties**: Allows businesses to define custom output columns dynamically before execution, minimizing LLM cognitive overload.
* **Rate-Limit Pacing**: Built-in async delay mechanisms between batch chunks to completely eliminate `429 RESOURCE_EXHAUSTED` errors on free-tier APIs.
* **Interactive Dashboard**: Real-time analytics summary metrics, status categorization tabs (Hot, Cold, Unrelated), and one-click enriched CSV export.

---

## 🛠️ Tech Stack

* **Backend**: FastAPI, Uvicorn, Pydantic, Pandas, Google GenAI SDK (`google-genai`).
* **Frontend**: Streamlit, Custom CSS UI layout.
* **AI Engine**: Google Gemini (`gemini-2.5-flash`).

---

## 📂 Project Structure

```text
lead_pipeline/
│
├── backend/
│   ├── main.py          # FastAPI app & chunked batch processing router
│   ├── config.py        # Environment settings loader
│   ├── schemas.py       # Pydantic validation schemas
│   └── services.py      # Gemini AI integration & parser service
│
├── frontend/
│   └── app.py           # Streamlit interactive user dashboard
│
├── .env                 # Environment API credentials (ignored in git)
├── .gitignore           # Git exclusion rules
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation