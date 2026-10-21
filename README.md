# ⚡ AI Lead Intelligence Hub & Qualification Pipeline

An enterprise-grade, high-performance B2B lead qualification and personalization platform built with **FastAPI**, **Streamlit**, and **Google Gemini AI**.

Designed to process large customer datasets (CSV/Excel) efficiently while bypassing LLM rate limits through intelligent multi-row batching and request pacing.

---

## 🚀 Key Features

- **Zero-Mapping CSV/Excel Ingestion**: Instantly parses raw lead files with automatic error handling and data cleaning.
- **40-Profile Batch Processing**: Groups customer records into structured batch payloads to reduce API calls by 90% and conserve Token-Per-Minute (TPM) limits.
- **Dynamic Custom Properties**: Allows businesses to define custom output columns dynamically before execution, minimizing LLM cognitive overload.
- **Rate-Limit Pacing**: Built-in async delay mechanisms between batch chunks to help prevent `429 RESOURCE_EXHAUSTED` errors on free-tier APIs.
- **Interactive Dashboard**: Real-time analytics summary metrics, status categorization tabs (Hot, Cold, Unrelated), and one-click enriched CSV export.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn, Pydantic, Pandas, Google GenAI SDK (`google-genai`).
- **Frontend**: Streamlit, Custom CSS UI layout.
- **AI Engine**: Google Gemini (`gemini-2.5-flash`).

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
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/lead-generation-pipeline.git
cd lead-generation-pipeline
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
```

**On Windows:**

```bash
venv\Scripts\activate
```

**On macOS/Linux:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add your Google Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

---

## 🏃 Running the Application

### Step 1: Start the FastAPI Backend

```bash
uvicorn backend.main:app --reload
```

*The backend API will run on `http://127.0.0.1:8000`.*

### Step 2: Launch the Streamlit Frontend

Open a new terminal and run:

```bash
streamlit run frontend/app.py
```

*The dashboard will open automatically in your browser at `http://localhost:8501`.*
