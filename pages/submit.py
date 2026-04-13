import streamlit as st
import uuid
import os
import time
from datetime import datetime
from core import database, classifier, router
from core.utils import load_css

st.set_page_config(page_title="Submit a Problem", page_icon="🎓", layout="wide")
load_css()

st.title("🎓 Submit a Campus Problem")
st.subheader("Automated Multi-Agent Routing Flow")

os.makedirs("uploads", exist_ok=True)

with st.form("submission_form"):
    description = st.text_area("Incident Description", placeholder="Feed context to the AI...")
    image = st.file_uploader("Upload visual evidence (optional)", type=["jpg", "jpeg", "png"])
    submit_button = st.form_submit_button("Engage AI Pipeline")
    
if submit_button:
    if not description.strip():
        st.error("Input required for AI processing.")
    else:
        # Pre-checks
        tracking_id = str(uuid.uuid4())[:8].upper()
        image_path = None
        if image:
            image_path = os.path.join("uploads", f"{tracking_id}_{image.name}")
            with open(image_path, "wb") as f:
                f.write(image.getbuffer())

        # Streamlit dynamic UI containers
        terminal_container = st.empty()
        
        # Initiate Hollywood Hacker UI sequence
        terminal_html = f"""
        <div class="ai-terminal">
            <p class="terminal-text" style="color: #A64EEC;">[SYSTEM] >> INITIALIZING ENSEMBLE PIPELINE...</p>
        </div>"""
        terminal_container.markdown(terminal_html, unsafe_allow_html=True)
        time.sleep(0.8)
        
        terminal_html = terminal_html.replace('</div>', f'<p class="terminal-text">>> ALLOCATING UUID: <span class="terminal-highlight">{tracking_id}</span></p></div>')
        terminal_container.markdown(terminal_html, unsafe_allow_html=True)
        time.sleep(0.5)

        terminal_html = terminal_html.replace('</div>', '<p class="terminal-text">>> INVOKING AGENT 1 (Entity Extraction Engine)...</p></div>')
        terminal_container.markdown(terminal_html, unsafe_allow_html=True)
        
        # ─── REAL AI INFERENCE HAPPENS HERE ───
        result = classifier.classify(description.strip(), image_path)
        
        # Pull rich data
        urgency = result.get("urgency", "MEDIUM")
        entities = ", ".join(result.get("entities", []))
        sentiment = result.get("sentiment", "NEUTRAL")
        reasoning = result.get("reasoning", "Standard routing active.")
        category = result.get("category", "Other")
        confidence = result.get("confidence", 0.0)
        latency = result.get("latency_ms", "N/A")
        
        # DB & Router insertion
        database.insert_problem(tracking_id, description.strip(), image_path)
        department = router.route_problem(tracking_id, category, confidence)
        st.session_state["tracking_id"] = tracking_id

        # Finish streaming UI with real extracted AI metrics
        terminal_html = terminal_html.replace('</div>', f"""
            <p class="terminal-text" style="color:#7bed9f;">>> AGENT 1 SUCCESS. Context Extracted:</p>
            <p class="terminal-text" style="padding-left: 20px;">- URGENCY: [{urgency}]</p>
            <p class="terminal-text" style="padding-left: 20px;">- ENTITIES: [{entities}]</p>
            <p class="terminal-text" style="padding-left: 20px;">- SENTIMENT: [{sentiment}]</p>
            <p class="terminal-text" style="margin-top:10px;">>> INVOKING AGENT 2 (Semantic Routing CoT)...</p>
        </div>""")
        terminal_container.markdown(terminal_html, unsafe_allow_html=True)
        time.sleep(1.2)
        
        terminal_html = terminal_html.replace('</div>', f"""
            <p class="terminal-text" style="color:#7bed9f;">>> AGENT 2 CHAIN-OF-THOUGHT TRACE:</p>
            <p class="terminal-text" style="padding-left: 20px; font-style: italic;">"{reasoning}"</p>
            <p class="terminal-text" style="margin-top:10px;">>> LLM CLASSIFICATION RESULT: <span class="terminal-highlight">[{category.upper()}]</span></p>
            <p class="terminal-text">>> SEMANTIC ROUTE ASSIGNED: <span style="color:#A64EEC; font-weight:700;">{department.upper()}</span></p>
            <p class="terminal-text">>> INFERENCE LATENCY: {latency}ms | PIPELINE COMPLETED.</p>
        </div>""")
        terminal_container.markdown(terminal_html, unsafe_allow_html=True)
        
        # Finish with metrics
        st.write("")
        st.progress(confidence, text=f"Calibration Confidence Score: {int(confidence*100)}%")
        st.caption("🔒 Security Note: Save your Tracking ID to monitor the resolution lifecycle.")
        st.balloons()
