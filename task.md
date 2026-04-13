# Campus Problem Solver — Build Prompts

Use these prompts sequentially with an AI coding assistant (Claude Code, Cursor, Copilot, etc.)
Each prompt is self-contained and builds on the previous step.

---

## STEP 0 — Project Scaffold

```
Create a full-stack Python web application called "Campus Problem Solver" with the following folder structure:

campus-problem-solver/
├── app.py                  # Main Streamlit entry point
├── pages/
│   ├── submit.py           # Student submission portal
│   ├── track.py            # Student tracking dashboard
│   └── admin.py            # Admin/executive dashboard
├── core/
│   ├── classifier.py       # AI classification agent
│   ├── router.py           # Automatic routing logic
│   ├── database.py         # SQLite database helpers
│   └── notifier.py         # Notification/logging system
├── data/
│   └── schema.sql          # DB schema
├── requirements.txt
└── README.md

Use Streamlit as the frontend framework. Use SQLite as the database (via Python's built-in sqlite3). 
Initialize git, create a .gitignore for Python/Streamlit, and fill requirements.txt with all necessary packages.
```

---

## STEP 1 — Database Schema & Helpers

```
In core/database.py and data/schema.sql, implement the following:

Tables:
1. problems
   - id (TEXT, primary key) — UUID tracking ID
   - description (TEXT, NOT NULL)
   - image_path (TEXT, nullable)
   - category (TEXT)
   - confidence (REAL)
   - department (TEXT)
   - status (TEXT) — "Submitted" | "In Progress" | "Resolved"
   - resolution_note (TEXT)
   - submitted_at (DATETIME)
   - updated_at (DATETIME)

2. departments
   - id (INTEGER, primary key)
   - name (TEXT)
   - contact_email (TEXT)
   - category (TEXT) — the category this dept handles

Seed the departments table with these mappings:
- Bathroom & Hygiene → Housekeeping Department
- Anti-Ragging & Safety → Student Affairs / Security Office
- Mess & Food Quality → Mess Committee / Warden
- Academic Issues → Academic Office / HOD
- Infrastructure/Maintenance → Campus Maintenance Cell
- Other → General Administration

In core/database.py write helper functions:
- init_db() — creates tables if not exist
- insert_problem(id, description, image_path) → inserts a new row
- get_problem(id) → returns single problem dict
- get_all_problems() → returns all problems
- get_problems_by_department(dept) → filtered list
- update_problem_classification(id, category, confidence, department)
- update_problem_status(id, status, resolution_note)

Call init_db() on import so the DB is always ready.
```

---

## STEP 2 — AI Classification Agent

```
In core/classifier.py, build a ClassificationAgent that uses the Anthropic Claude API to classify student complaints.

Requirements:
- Use the anthropic Python SDK (pip install anthropic)
- Read ANTHROPIC_API_KEY from environment variable or st.secrets
- The agent must classify input text into exactly one of these 6 categories:
    1. Bathroom & Hygiene
    2. Anti-Ragging & Safety
    3. Mess & Food Quality
    4. Academic Issues
    5. Infrastructure/Maintenance
    6. Other
- Call claude-3-haiku-20240307 for speed and cost efficiency
- Prompt the model to return ONLY a JSON object: {"category": "...", "confidence": 0.0-1.0, "reason": "..."}
- Parse the JSON response safely with a try/except
- If confidence < 0.5, override category to "Other" (fallback for low-confidence)
- Expose a single function: classify(text: str) -> dict with keys: category, confidence, reason

Write a simple test at the bottom under if __name__ == "__main__" that classifies 3 sample complaints and prints the results.
```

---

## STEP 3 — Routing System

```
In core/router.py, implement an automatic routing system.

Requirements:
- Import database helpers
- Define a CATEGORY_TO_DEPARTMENT dict mapping all 6 categories to their departments (match the seeded data from Step 1)
- Implement: route_problem(problem_id: str, category: str, confidence: float) -> str
    1. Look up the correct department from CATEGORY_TO_DEPARTMENT
    2. Call database.update_problem_classification(problem_id, category, confidence, department)
    3. Call notifier.notify(problem_id, department, category)
    4. Return the department name

In core/notifier.py, implement a simple notifier:
- notify(problem_id, department, category) should:
    1. Log a structured message to a file called logs/notifications.log with timestamp, tracking ID, department, and category
    2. Also print to console
    3. If an SMTP config is present in environment (SMTP_HOST, SMTP_USER, SMTP_PASS, ADMIN_EMAIL), send a plain-text email notification — otherwise skip silently

Create the logs/ directory if it doesn't exist.
```

---

## STEP 4 — Problem Submission Portal

```
In pages/submit.py, build the student problem submission page in Streamlit.

UI layout:
- Page title: "🎓 Submit a Campus Problem"
- Subheader: "We'll route your complaint to the right department automatically."
- A text_area for Problem Description (required, placeholder: "Describe your issue in detail...")
- A file_uploader for optional image (jpg, jpeg, png)
- A Submit button
- On submit:
    1. Validate that description is not empty — show st.error if blank
    2. Generate a UUID tracking ID (use uuid.uuid4(), take first 8 chars, uppercase: e.g. "AB12CD34")
    3. Save uploaded image to uploads/ folder if present
    4. Insert the problem into DB via database.insert_problem()
    5. Call classifier.classify(description) to get category + confidence
    6. Call router.route_problem() to assign department
    7. Show a success box with:
        - "✅ Problem Submitted Successfully!"
        - Tracking ID in large text (use st.metric or st.code)
        - Detected category and assigned department
        - Confidence score as a progress bar
    8. Store tracking ID in st.session_state for easy reference

Add a note: "Save your Tracking ID to check status later."
```

---

## STEP 5 — User Tracking Dashboard

```
In pages/track.py, build the student problem tracking page in Streamlit.

UI layout:
- Page title: "🔍 Track Your Problem"
- A text_input for the Tracking ID
- A "Track" button
- If tracking ID is found in DB:
    - Show problem description
    - Show category (with an emoji per category: 🚿 Bathroom, 🛡️ Safety, 🍽️ Mess, 📚 Academic, 🔧 Maintenance, 📋 Other)
    - Show assigned department
    - Show status as a colored badge:
        - "Submitted" → 🟡
        - "In Progress" → 🔵
        - "Resolved" → 🟢
    - Show submitted_at and updated_at timestamps
    - If resolution_note is present, show it in an info box
- If not found: show st.warning("No problem found with this tracking ID.")
- Add a "Refresh" button to re-query the DB
- If st.session_state has a tracking ID from submission, pre-fill the input
```

---

## STEP 6 — Admin / Executive Dashboard

```
In pages/admin.py, build the admin dashboard in Streamlit.

UI layout:
- Page title: "🛠️ Admin Dashboard"
- Simple password gate: check for ADMIN_PASSWORD in st.secrets or env var. If not set, use "admin123" as default. Show a password input; if wrong, st.stop().
- After login:
    - Show total counts at the top: Total Submitted, In Progress, Resolved (use st.metric in 3 columns)
    - A selectbox to filter by Department (show "All Departments" + each department name)
    - A selectbox to filter by Status
    - Display all matching problems as Streamlit cards (use st.expander per problem):
        - Title: Tracking ID + short description
        - Inside: full description, category, confidence score, department, submitted_at
        - A selectbox to change status: Submitted / In Progress / Resolved
        - A text_area for Resolution Note
        - An "Update" button — on click, call database.update_problem_status() and show st.success
    - Add a "Download CSV" button that exports all problems as a CSV using pandas + st.download_button
```

---

## STEP 7 — Main App Entry Point

```
In app.py, set up the Streamlit multi-page app.

Requirements:
- Set page config: title="Campus Problem Solver", page_icon="🎓", layout="wide"
- Call database.init_db() at startup
- Build a sidebar with navigation:
    - 📝 Submit a Problem → pages/submit.py
    - 🔍 Track My Problem → pages/track.py
    - 🛠️ Admin Dashboard → pages/admin.py
- On the home/landing page, show:
    - A hero section: app name, tagline "AI-powered campus complaint resolution"
    - A brief "How it works" section with 4 steps: Submit → AI Classifies → Routes to Dept → Resolved
    - Stats: total problems submitted, resolved today (query from DB)
- Use st.set_page_config only once in app.py
```

---

## STEP 8 — README & Documentation

```
Write a comprehensive README.md for the Campus Problem Solver project.

Include:
1. Project title and one-line description
2. Features list (all 5 components)
3. Tech stack: Python, Streamlit, SQLite, Anthropic Claude API
4. Setup instructions:
   a. Clone the repo
   b. pip install -r requirements.txt
   c. Set ANTHROPIC_API_KEY in .env or Streamlit secrets
   d. Run: streamlit run app.py
5. Environment variables table (ANTHROPIC_API_KEY, ADMIN_PASSWORD, SMTP_HOST, SMTP_USER, SMTP_PASS, ADMIN_EMAIL)
6. Folder structure overview
7. AI Classification section:
   - Model used: claude-3-haiku-20240307
   - Categories and their mapped departments
   - How confidence scoring works
   - Accuracy methodology (tested on 30 manual samples, achieved ~90% with LLM)
8. Screenshots placeholder section
9. Deployment instructions for Streamlit Cloud:
   - Push to GitHub
   - Connect repo on share.streamlit.io
   - Add secrets in Streamlit Cloud dashboard
10. License: MIT
```

---

## STEP 9 — Polish & Edge Cases

```
Review the entire Campus Problem Solver codebase and apply these improvements:

1. Error handling: Wrap all Anthropic API calls in try/except. If the API fails, fall back to keyword-based classification:
   - Keywords for each category (e.g. "bathroom", "toilet", "water" → Bathroom & Hygiene)
   - Set confidence to 0.6 for keyword fallback, 0.4 for "Other" fallback

2. Image handling: If a student uploads an image, also pass it to the Claude API as a base64-encoded image alongside the text description for multimodal classification.

3. Input sanitization: Strip and truncate description to 2000 characters before sending to the API.

4. Loading states: Add st.spinner("🤖 AI is analyzing your complaint...") during classification.

5. Session persistence: Use st.session_state to remember the last tracking ID across page navigations.

6. Mobile responsiveness: Ensure all columns degrade gracefully by using st.columns with appropriate ratios.

7. Duplicate detection: Before inserting, check if a very similar problem (same description, same day) already exists. If so, show a warning but still allow submission.

8. requirements.txt: Make sure it includes: streamlit, anthropic, pandas, Pillow, python-dotenv — all pinned to stable versions.
```

---

## STEP 10 — Final Check & Deploy Prep

```
Perform a final end-to-end test of the Campus Problem Solver and prepare it for deployment.

Tasks:
1. Run the app locally and test these 6 user flows:
   a. Submit "The fan in Room 204 is broken" → should classify as Infrastructure/Maintenance
   b. Submit "A senior is threatening juniors in hostel" → should classify as Anti-Ragging & Safety
   c. Submit "Dal is undercooked in today's lunch" → should classify as Mess & Food Quality
   d. Submit "My attendance is wrongly marked" → should classify as Academic Issues
   e. Submit "Toilet on 2nd floor has no water" → should classify as Bathroom & Hygiene
   f. Submit "I have a general suggestion" → should classify as Other

2. For each: verify tracking ID is generated, department is assigned, and status shows "Submitted".

3. Open Admin Dashboard, update one problem to "Resolved" with a resolution note. Verify it reflects on Track page.

4. Export CSV from Admin and verify it downloads correctly.

5. Create a .streamlit/secrets.toml.example file showing required secrets format.

6. Write a TESTING.md documenting:
   - The 6 test cases above with expected vs actual category
   - Accuracy score (correct / 6)
   - Any misclassifications and why

7. Final git commit message: "feat: complete MVP - all 5 components working end-to-end"
```

---

## Quick Reference — Category → Department Map

| Category | Department |
|---|---|
| Bathroom & Hygiene | Housekeeping Department |
| Anti-Ragging & Safety | Student Affairs / Security Office |
| Mess & Food Quality | Mess Committee / Warden |
| Academic Issues | Academic Office / HOD |
| Infrastructure/Maintenance | Campus Maintenance Cell |
| Other | General Administration |

---

## Tech Stack Summary

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI Classification | Anthropic Claude API (claude-3-haiku) |
| Database | SQLite (built-in, zero setup) |
| Image Handling | Pillow |
| Notifications | File logging + optional SMTP email |
| Deployment | Streamlit Cloud / Vercel / Local |

---

*Follow steps 0 → 10 in order. Each prompt is designed to be pasted directly into Claude Code or any AI coding assistant.*
