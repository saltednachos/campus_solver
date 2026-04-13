# task2.md — Frontend Redesign Prompt

Replace all Streamlit UI code across `pages/submit.py`, `pages/track.py`, `pages/admin.py`, and `app.py` with the following design system. Do not change any backend logic — only the presentation layer changes.

---

## Design System

**Color palette — strict black and white only.**

```css
--bg:        #ffffff;
--surface:   #f7f7f7;
--border:    #e0e0e0;
--text:      #111111;
--muted:     #666666;
--accent:    #111111;   /* used for buttons and highlights */
--danger:    #111111;   /* no red — use bold text instead */
```

**Typography**
- Font: system-ui, -apple-system, sans-serif (no Google Fonts imports)
- Body: 14px, `#111111`, line-height 1.6
- Labels: 12px uppercase, letter-spacing 0.08em, `#666666`
- Headings: weight 600, no decorative styling

**Spacing**
- Base unit: 8px. Use multiples: 8, 16, 24, 32, 48
- No full-bleed hero sections, no large padding blocks

**Components**
- Inputs: 1px solid `#e0e0e0`, no border-radius (or max 2px), background `#ffffff`
- Buttons: solid black background `#111111`, white text, no border-radius, no shadows, no hover animations — only a subtle `opacity: 0.85` on hover
- Cards/panels: `#f7f7f7` background, 1px solid `#e0e0e0` border, no shadows
- Status badges: text-only with a prefix symbol — no colored dots, no pills
    - Submitted → `[ SUBMITTED ]`
    - In Progress → `[ IN PROGRESS ]`
    - Resolved → `[ RESOLVED ]`
- No emojis anywhere in the UI
- No gradient backgrounds
- No st.balloons, st.snow, or any celebration effects

---

## Global Streamlit Config (app.py)

```python
st.set_page_config(
    page_title="Campus Problem Solver",
    page_icon=None,
    layout="centered",       # not "wide"
    initial_sidebar_state="collapsed",
)

# Inject base CSS — call this at the top of every page
def inject_css():
    st.markdown("""
    <style>
      /* Reset Streamlit chrome */
      #MainMenu, footer, header { visibility: hidden; }
      .block-container { padding: 2rem 1.5rem; max-width: 720px; }

      /* Typography */
      html, body, [class*="css"] {
        font-family: system-ui, -apple-system, sans-serif;
        color: #111111;
        background: #ffffff;
      }

      /* Inputs */
      textarea, input[type="text"], input[type="password"] {
        border: 1px solid #e0e0e0 !important;
        border-radius: 2px !important;
        background: #ffffff !important;
        font-size: 14px !important;
        box-shadow: none !important;
      }
      textarea:focus, input:focus {
        border-color: #111111 !important;
        box-shadow: none !important;
      }

      /* Buttons */
      .stButton > button {
        background: #111111 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 2px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        letter-spacing: 0.04em !important;
        padding: 0.5rem 1.25rem !important;
        box-shadow: none !important;
      }
      .stButton > button:hover { opacity: 0.82 !important; }

      /* Labels */
      label, .stSelectbox label, .stTextArea label {
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: #666666 !important;
        font-weight: 500 !important;
      }

      /* Divider */
      hr { border: none; border-top: 1px solid #e0e0e0; margin: 1.5rem 0; }

      /* Metric overrides */
      [data-testid="metric-container"] {
        background: #f7f7f7;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 2px;
      }

      /* Expander */
      .streamlit-expanderHeader {
        font-size: 13px !important;
        font-weight: 500 !important;
        background: #f7f7f7 !important;
        border: 1px solid #e0e0e0 !important;
      }

      /* Remove all colored alert backgrounds */
      .stAlert { border-radius: 2px !important; }

      /* File uploader */
      [data-testid="stFileUploader"] {
        border: 1px dashed #e0e0e0 !important;
        border-radius: 2px !important;
        background: #f7f7f7 !important;
      }
    </style>
    """, unsafe_allow_html=True)
```

Call `inject_css()` as the very first line inside every page file.

---

## Navigation (app.py sidebar)

Replace the sidebar with a minimal top-of-page tab strip using `st.tabs`:

```python
tab1, tab2, tab3 = st.tabs(["Submit", "Track", "Admin"])
```

Do not use `st.sidebar` at all. No icons in tab labels.

Alternatively, if multi-page routing is kept, replace the sidebar nav with plain `st.page_link` buttons rendered as text links — no icons, no bold.

---

## Page: Submit (pages/submit.py)

```
Layout (top to bottom, centered, max-width 720px):

1. Plain text heading: "Submit a problem"
   - h3 weight, no icon, no subtitle

2. A thin hr divider

3. Label: "DESCRIPTION"
   Text area, 5 rows, placeholder: "Describe the issue clearly."
   Full width.

4. Label: "ATTACH IMAGE  —  OPTIONAL"
   File uploader, accepted: jpg, jpeg, png
   Show filename only after upload, no preview thumbnail

5. Submit button — full width, black, text: "Submit"

6. On success, replace the form with a plain confirmation block:
   ┌─────────────────────────────────────┐
   │ Problem submitted.                  │
   │                                     │
   │ TRACKING ID                         │
   │ AB12CD34                            │
   │                                     │
   │ CATEGORY                            │
   │ Infrastructure / Maintenance        │
   │                                     │
   │ ASSIGNED TO                         │
   │ Campus Maintenance Cell             │
   │                                     │
   │ STATUS                              │
   │ [ SUBMITTED ]                       │
   └─────────────────────────────────────┘
   Render this as a styled st.markdown block with a thin border.
   No confetti. No balloons. No success color.

7. Below the block, one line of muted text:
   "Save your tracking ID to check status."
```

---

## Page: Track (pages/track.py)

```
Layout:

1. Heading: "Track a problem"
2. hr divider
3. Label: "TRACKING ID"
   Single-line text input, placeholder: "e.g. AB12CD34"
   + "Track" button on the same row (use st.columns([4,1]))

4. If found — render a single bordered block:
   ┌─────────────────────────────────────┐
   │ TRACKING ID          AB12CD34       │
   ├─────────────────────────────────────┤
   │ DESCRIPTION                         │
   │ The fan in Room 204 is broken.      │
   │                                     │
   │ CATEGORY                            │
   │ Infrastructure / Maintenance        │
   │                                     │
   │ DEPARTMENT                          │
   │ Campus Maintenance Cell             │
   │                                     │
   │ STATUS                              │
   │ [ IN PROGRESS ]                     │
   │                                     │
   │ SUBMITTED    12 Apr 2026, 10:32 AM  │
   │ UPDATED      12 Apr 2026, 02:14 PM  │
   │                                     │
   │ RESOLUTION NOTE                     │
   │ Technician visit scheduled for      │
   │ tomorrow morning.                   │
   └─────────────────────────────────────┘
   Only show RESOLUTION NOTE section if it exists.

5. A small muted "Refresh" text link below the block (not a button).
   Use st.markdown with an onclick that calls st.rerun().

6. If not found: one line — "No record found for this tracking ID."
   No warning box. Just muted text.
```

---

## Page: Admin (pages/admin.py)

```
Layout:

1. Password input (type="password"), label: "ADMIN ACCESS"
   + "Enter" button. If wrong: one line "Incorrect password." — no st.error box.
   st.stop() after that.

2. After login — no welcome message. Go straight to content.

3. Three metrics in a row (st.columns(3)):
   - Total | In Progress | Resolved
   Plain numbers, no delta arrows, no color

4. hr divider

5. Two filter controls on one row (st.columns([3,3])):
   - Selectbox: "FILTER BY DEPARTMENT"
   - Selectbox: "FILTER BY STATUS"

6. Problem list — one st.expander per problem:
   - Expander title: "{tracking_id}  —  {first 60 chars of description}"
   - Inside:
       DESCRIPTION
       {full text}

       CATEGORY          CONFIDENCE
       {category}        {score}%

       DEPARTMENT
       {department}

       SUBMITTED
       {timestamp}

       ---

       STATUS
       [selectbox: Submitted / In Progress / Resolved]

       RESOLUTION NOTE
       [text_area, no placeholder]

       [Update] button — full width

7. Below the list, one right-aligned "Export CSV" button.
   Use st.download_button, label: "Export CSV"
```

---

## Things to Explicitly Remove

Go through all existing page files and remove every instance of:

- `st.success(...)` — replace with a plain bordered `st.markdown` block
- `st.error(...)` — replace with italic muted text: `st.markdown("_Error message here._")`
- `st.warning(...)` — same as above
- `st.info(...)` — same as above
- `st.balloons()`, `st.snow()`
- Any emoji in UI strings (submit button, labels, headings, status text)
- `st.progress()` for confidence — replace with plain text: `Confidence: 87%`
- Any `st.metric` with `delta=` values
- Colored status badges (green/yellow/blue) — use `[ STATUS ]` text format
- Any `layout="wide"` — change to `"centered"`

---

## What "Minimal" Means Here

The goal is a UI that looks like it was designed, not generated.
Every element should justify its existence.
If something is decorative and carries no information, remove it.
Default Streamlit widgets are fine — the CSS overrides handle the rest.
Do not install any additional frontend libraries.

---

*Paste this entire prompt into Claude Code after completing task.md steps 0–7.*
