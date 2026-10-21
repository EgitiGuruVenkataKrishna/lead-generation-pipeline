import streamlit as st
import requests
import pandas as pd
import io
import json

st.set_page_config(page_title="AI Lead Intelligence Hub", page_icon="⚡", layout="wide")

st.title("⚡ AI Lead Qualification & Custom Property Pipeline")
st.markdown("Upload raw lead data, specify your company context, and dynamically define custom output properties for zero LLM overhead.")

with st.sidebar:
    st.header("⚙️ Pipeline Controls")
    
    st.markdown("### 1. Company & ICP Context")
    company_context = st.text_area(
        "Define your product, pricing, and ICP:",
        placeholder="e.g., B2B SaaS cloud cost monitoring tool for $499/mo. Target: CTOs, VPs Eng.",
        height=150
    )
    
    st.markdown("### 2. Custom Output Properties")
    st.markdown("Define extra columns you want the AI to generate:")
    default_props = "Lead_Type, Reason, Personalized_Email, Follow_Up_Questions"
    properties_input = st.text_input(
        "Comma-separated property names:",
        value=default_props
    )
    
    st.markdown("### 3. Upload Dataset")
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
    
    st.markdown("---")
    run_button = st.button("🚀 Run AI Pipeline (40-Batch / 5s Pacing)", use_container_width=True, type="primary")

if "processed_df" not in st.session_state:
    st.session_state.processed_df = None

if run_button:
    if not company_context or not uploaded_file:
        st.warning("⚠️ Please provide both company context and an uploaded dataset.")
    else:
        props_list = [p.strip() for p in properties_input.split(",") if p.strip()]
        
        with st.status("🔄 Processing batches (40 profiles/chunk with 5s rate-limit pacing)...", expanded=True) as status:
            st.write("Chunking dataset and dispatching optimized payloads...")
            
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {
                    "company_context": company_context,
                    "custom_properties": json.dumps(props_list)
                }
                
                response = requests.post("http://localhost:8000/api/leads/process", files=files, data=data)
                
                if response.status_code == 200:
                    status.update(label="✅ Pipeline Completed Successfully!", state="complete", expanded=False)
                    csv_content = response.content
                    st.session_state.processed_df = pd.read_csv(io.BytesIO(csv_content))
                    st.session_state.raw_csv_bytes = csv_content
                    st.success("All leads successfully analyzed with zero errors!")
                else:
                    status.update(label="❌ Failed", state="error")
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                status.update(label="❌ Connection Error", state="error")
                st.error("Could not connect to FastAPI backend. Ensure backend is running: `uvicorn backend.main:app --reload`")

if st.session_state.processed_df is not None:
    df = st.session_state.processed_df
    st.markdown("---")
    st.header("📊 Enriched Leads Preview")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.download_button(
        label="📥 Download Enriched Leads CSV",
        data=st.session_state.raw_csv_bytes,
        file_name="qualified_leads_enriched.csv",
        mime="text/csv",
        use_container_width=True,
        type="primary"
    )
else:
    st.info("👈 Configure your settings in the sidebar and click **Run AI Pipeline**.")