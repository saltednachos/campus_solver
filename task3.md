# task2.md — Frontend Redesign Prompt

Replace all Streamlit UI code across `pages/submit.py`, `pages/track.py`, `pages/admin.py`, and `app.py` with the following design system. Do not change any backend logic — only the presentation layer changes.

---

## Design Reference

The UI takes inspiration from a bold editorial web design language:
- Heavy, confident typography as the primary visual element
- One strong accent color (lime green) against white and near-black
- Floating card elements with subtle geometry
- Generous whitespace — content breathes
- A dark top bar anchors the page; everything else is light

---

## Design System

**Color palette**

```css
--bg:           #ffffff;
--surface:      #f5f5f0;     /* warm off-white for cards */
--dark:         #0f2318;     /* deep forest green — top bar, headings */
--text:         #111111;
--muted:        #5a5a5a;
--accent:       #c8f04a;     /* lime green — primary CTA, highlights */
--accent-dark:  #8ab832;     /* hover state for accent */
--border:       #e2e2dc;
--white:        #ffffff;
```

**Typography**
- Headings: `'Inter', system-ui, sans-serif` — weight 800, tight letter-spacing (-0.03em)
- Body: weight 400, 15px, line-height 1.65, `#111111`
- Labels: 11px, weight 600, uppercase, letter-spacing 0.1em, `#5a5a5a`
- The large page heading should feel bold enough to anchor the page — aim for 2.8–3.5rem

**Layout**
- Max content width: 760px, centered
- Top announcement bar: full-width, `#0f2318` background, small white text
- Navigation: white background, bottom border `1px solid #e2e2dc`
- Sections separated by whitespace (48–64px), not dividers

**Buttons**
- Primary: `#c8f04a` background, `#0f2318` text, font-weight 700, border-radius 4px, no shadow. On hover: background `#8ab832`.
- Secondary / ghost: transparent background, `1px solid #111111` border, `#111111` text. On hover: background `#f5f5f0`.
- Size: padding `10px 24px`, font-size 14px

**Cards / Panels**
- Background: `#ffffff`, border: `1px solid #e2e2dc`, border-radius: 6px
- No drop shadows — use border only
- Internal padding: 24px

**Status labels** — text only, uppercase, small
- `SUBMITTED` — plain text, color `#5a5a5a`
- `IN PROGRESS` — color `#0f2318`, font-weight 700
- `RESOLVED` — color `#8ab832`, font-weight 700

**Decorative geometry** — subtle only
- Use `border-radius: 50%` circles as CSS pseudo-elements or inline `<span>` blocks in markdown
- Limit to 1–2 small shapes per page (20–40px), color `#c8f04a` or `#0f2318`
- Never use emojis as decoration

---

## Global CSS (inject_css function in app.py)

```python
def inject_css():
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');

      /* --- Reset --- */
      #MainMenu, footer { visibility: hidden; }
      .block-container {
        padding: 0 !important;
        max-width: 100% !important;
      }

      html, body, [class*="css"] {
        font-family: 'Inter', system-ui, sans-serif;
        background: #ffffff;
        color: #111111;
      }

      /* --- Announcement bar --- */
      .announce-bar {
        width: 100%;
        background: #0f2318;
        color: #ffffff;
        text-align: center;
        font-size: 12px;
        letter-spacing: 0.04em;
        padding: 10px 0;
      }

      /* --- Nav bar --- */
      .top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 48px;
        border-bottom: 1px solid #e2e2dc;
        background: #ffffff;
        position: sticky;
        top: 0;
        z-index: 100;
      }
      .nav-logo {
        font-size: 15px;
        font-weight: 800;
        color: #0f2318;
        letter-spacing: -0.02em;
      }
      .nav-links a {
        font-size: 13px;
        color: #111111;
        text-decoration: none;
        margin-left: 28px;
        font-weight: 500;
      }

      /* --- Page content wrapper --- */
      .page-wrap {
        max-width: 760px;
        margin: 0 auto;
        padding: 56px 24px 80px;
      }

      /* --- Eyebrow label --- */
      .eyebrow {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #5a5a5a;
        margin-bottom: 12px;
      }

      /* --- Page heading --- */
      .page-heading {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.1;
        color: #0f2318;
        margin-bottom: 16px;
      }

      /* --- Subtext --- */
      .sub-text {
        font-size: 15px;
        color: #5a5a5a;
        margin-bottom: 36px;
        max-width: 480px;
        line-height: 1.65;
      }

      /* --- Card --- */
      .card {
        background: #ffffff;
        border: 1px solid #e2e2dc;
        border-radius: 6px;
        padding: 28px;
        margin-bottom: 16px;
      }

      /* --- Field label inside card --- */
      .field-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #5a5a5a;
        margin-bottom: 4px;
      }
      .field-value {
        font-size: 15px;
        color: #111111;
        margin-bottom: 20px;
        font-weight: 500;
      }

      /* --- Status --- */
      .status-submitted  { color: #5a5a5a; font-weight: 600; font-size: 13px; letter-spacing: 0.06em; }
      .status-inprogress { color: #0f2318; font-weight: 700; font-size: 13px; letter-spacing: 0.06em; }
      .status-resolved   { color: #8ab832; font-weight: 700; font-size: 13px; letter-spacing: 0.06em; }

      /* --- Accent dot / geometry accent --- */
      .geo-dot {
        display: inline-block;
        width: 14px; height: 14px;
        border-radius: 50%;
        background: #c8f04a;
        vertical-align: middle;
        margin-right: 8px;
      }

      /* --- Tracking ID badge --- */
      .tracking-id {
        display: inline-block;
        background: #c8f04a;
        color: #0f2318;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: 0.04em;
        padding: 8px 20px;
        border-radius: 4px;
        margin: 8px 0 20px;
      }

      /* --- Inputs --- */
      textarea, input[type="text"], input[type="password"] {
        border: 1px solid #e2e2dc !important;
        border-radius: 4px !important;
        background: #ffffff !important;
        font-size: 14px !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: none !important;
        color: #111111 !important;
      }
      textarea:focus, input:focus {
        border-color: #0f2318 !important;
        box-shadow: none !important;
      }

      /* --- Streamlit label override --- */
      label, .stSelectbox label, .stTextArea label, .stTextInput label {
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        color: #5a5a5a !important;
        font-weight: 600 !important;
      }

      /* --- Primary button --- */
      .stButton > button {
        background: #c8f04a !important;
        color: #0f2318 !important;
        border: none !important;
        border-radius: 4px !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        padding: 10px 24px !important;
        box-shadow: none !important;
        font-family: 'Inter', sans-serif !important;
      }
      .stButton > button:hover {
        background: #8ab832 !important;
      }

      /* --- File uploader --- */
      [data-testid="stFileUploader"] {
        border: 1px dashed #c8f04a !important;
        border-radius: 4px !important;
        background: #f5f5f0 !important;
      }

      /* --- Metric cards --- */
      [data-testid="metric-container"] {
        background: #f5f5f0 !important;
        border: 1px solid #e2e2dc !important;
        border-radius: 6px !important;
        padding: 20px !important;
      }

      /* --- Expander --- */
      .streamlit-expanderHeader {
        font-size: 14px !important;
        font-weight: 600 !important;
        background: #f5f5f0 !important;
        border: 1px solid #e2e2dc !important;
        border-radius: 4px !important;
        color: #111111 !important;
      }

      /* --- Remove default alert colors --- */
      .stAlert {
        border-radius: 4px !important;
        border-left: 3px solid #c8f04a !important;
        background: #f5f5f0 !important;
      }

      /* --- Horizontal rule --- */
      hr {
        border: none;
        border-top: 1px solid #e2e2dc;
        margin: 32px 0;
      }

      /* --- Tabs --- */
      .stTabs [role="tab"] {
        font-size: 13px !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em !important;
        color: #5a5a5a !important;
      }
      .stTabs [aria-selected="true"] {
        color: #0f2318 !important;
        border-bottom: 2px solid #c8f04a !important;
      }
    </style>
    """, unsafe_allow_html=True)
```

Call `inject_css()` as the very first line inside every page file, followed immediately by the announcement bar and nav HTML.

---

## Announcement Bar + Nav (render at top of every page)

```python
def render_nav():
    st.markdown("""
    <div class="announce-bar">
      AI-powered campus complaint resolution — problems routed automatically.
    </div>
    <div class="top-nav">
      <span class="nav-logo">Campus<span style="color:#c8f04a">.</span></span>
      <div class="nav-links">
        <a href="/">Submit</a>
        <a href="/track">Track</a>
        <a href="/admin">Admin</a>
      </div>
    </div>
    """, unsafe_allow_html=True)
```

No `st.sidebar`. No tab strip inside the page body. Navigation lives in the top nav bar only.

---

## Page: Submit (pages/submit.py)

```
Render after inject_css() and render_nav():

1. Open .page-wrap div via st.markdown

2. Eyebrow label: "PROBLEM SUBMISSION"

3. Large heading: "Submit a problem."
   Use .page-heading class.

4. Subtext: "Describe the issue and our AI agent will classify and route
   it to the right department automatically."
   Use .sub-text class, max-width 420px.

5. A single .card div containing the form:
   - Label: "DESCRIPTION"
     Text area, 5 rows, no placeholder text
   - Label: "ATTACH IMAGE  —  OPTIONAL"
     File uploader (jpg, jpeg, png). Filename shown on upload. No preview.
   - Submit button — label: "Submit problem"
     Left-aligned, not full-width. Lime green.

6. On success — replace the card with a confirmation card:

   .card layout:
   ┌──────────────────────────────────────────┐
   │  Problem submitted.                      │
   │                                          │
   │  TRACKING ID                             │
   │  [  AB12CD34  ]  ← lime green badge      │
   │                                          │
   │  CATEGORY                                │
   │  Infrastructure / Maintenance            │
   │                                          │
   │  ASSIGNED TO                             │
   │  Campus Maintenance Cell                 │
   │                                          │
   │  STATUS                                  │
   │  SUBMITTED                               │
   └──────────────────────────────────────────┘

   Render using st.markdown with .card, .field-label, .field-value,
   .tracking-id, and .status-submitted CSS classes.

   Below the card, one line in muted style:
   "Keep your tracking ID — you'll need it to check status."

7. Close .page-wrap div
```

---

## Page: Track (pages/track.py)

```
Layout:

1. Eyebrow: "STATUS TRACKER"
2. Heading: "Track your problem."
3. Subtext: "Enter your tracking ID to see the current status and any updates."

4. Input row — st.columns([5, 1]):
   - Text input, label: "TRACKING ID", placeholder: ""
   - Button: "Track"

5. If found — render a .card:

   Top section (st.columns([2, 1])):
   LEFT:
     TRACKING ID      → plain value (not the badge here)
     DESCRIPTION      → full text
     CATEGORY         → category name
     DEPARTMENT       → department name

   RIGHT:
     STATUS
     [ SUBMITTED / IN PROGRESS / RESOLVED ]
     in correct CSS class

     SUBMITTED        → formatted date
     UPDATED          → formatted date or "—"

   hr inside the card

   If resolution_note exists:
     RESOLUTION NOTE
     {note text}
     Rendered in a block with left border: 3px solid #c8f04a, padding-left 12px

6. If not found:
   Plain muted text: "No record found for this tracking ID."
   No warning box, no colored alert.

7. Small right-aligned "Refresh" text link below the card.
   Style: font-size 12px, color #5a5a5a. On click: st.rerun()
```

---

## Page: Admin (pages/admin.py)

```
Layout:

1. Password gate:
   Eyebrow: "ADMIN ACCESS"
   Heading: "Dashboard."
   Text input (type password), label: "ENTER PASSWORD"
   Button: "Enter"
   If wrong: muted text "Incorrect password." — no st.error.
   st.stop()

2. After login — no greeting. Go straight to content.

3. Three metric cards in st.columns(3):
   - Total Problems
   - In Progress
   - Resolved
   No delta values, no color. Plain numbers, black on off-white.

4. hr divider

5. Filter row — st.columns([3, 3, 2]):
   - Selectbox: DEPARTMENT
   - Selectbox: STATUS
   - Download button: "Export CSV"
     Style as ghost/outline: border 1px solid #0f2318, background white, text #0f2318

6. Problem list — st.expander per problem:
   Title: "{tracking_id}  ·  {first 55 chars of description}..."

   Inside each expander (.card):
   Two columns (st.columns([3, 2])):
   LEFT:
     DESCRIPTION → full text
     CATEGORY    → value
     CONFIDENCE  → plain "{n}%" — no progress bar
     SUBMITTED   → timestamp

   RIGHT:
     DEPARTMENT     → value
     CURRENT STATUS → value in correct CSS class
     hr
     UPDATE STATUS  → selectbox
     RESOLUTION NOTE → text area, 3 rows
     [Update] button — lime green, label "Update"

   On success: st.toast("Updated.") — not st.success() banner.
```

---

## Home / Landing (app.py)

```
After inject_css() and render_nav():

1. Two-column layout — st.columns([1.1, 0.9]):

   LEFT:
     Eyebrow: "CAMPUS PROBLEM SOLVER"
     Heading (3 lines):
       "Resolve campus
        problems —
        automatically."
     font-size 3.5rem, .page-heading class

     Subtext: "Submit a complaint. Our AI agent classifies it and routes
     it to the right department — no manual sorting needed."

     Buttons on one row (st.columns([2, 2, 3])):
     - "Submit a problem"  → lime green primary
     - "Track status"      → ghost / outline secondary

     Muted line: "{total_count} problems submitted · {resolved_count} resolved this week."

   RIGHT:
     A styled .card via st.markdown:
     ┌──────────────────────────────┐
     │  What happens next?          │
     │                              │
     │  ● 01  You describe the issue│
     │  ● 02  AI classifies it      │
     │  ● 03  Routed to department  │
     │  ● 04  Status updates live   │
     └──────────────────────────────┘
     Each ● is a <span class="geo-dot"></span> (lime green circle).

2. hr divider

3. Stats row — st.columns(3) with .metric cards:
   - Problems submitted today
   - Avg. classification confidence
   - Departments active
```

---

## Things to Explicitly Remove

Go through all existing page files and delete every instance of:

- `st.success(...)` — replace with `.card` HTML block via `st.markdown`
- `st.error(...)` — replace with muted italic text
- `st.warning(...)` — replace with muted italic text
- `st.info(...)` — replace with plain text or left-bordered note block
- `st.balloons()`, `st.snow()`
- All emojis in UI strings — headings, labels, buttons, status text, tab names
- `st.progress()` for confidence — replace with plain `{n}%` text
- Colored status dots (green/yellow/blue) — use CSS classes instead
- `layout="wide"` — remove; content width is controlled by `.page-wrap`
- `st.sidebar` — navigation is in the top nav bar only
- `st.metric(delta=...)` — no deltas, plain numbers only

---

## Design Principles to Follow

**Hierarchy through type, not color.**
The heading carries the page. Color (lime green) appears only on interactive elements — buttons, the tracking ID badge, the resolution border accent. Everything else is black on white.

**One accent, used sparingly.**
`#c8f04a` appears in: the primary button, the tracking ID badge, the resolution note left border, the logo dot, and the active tab underline. Nowhere else.

**Cards contain, whitespace separates.**
Group related fields inside a `.card`. Use vertical spacing between sections — not extra horizontal rules or nested borders.

**Labels set context, values carry weight.**
Labels: small, uppercase, muted. Values: 15px, weight 500, dark. The hierarchy is immediate.

**No decoration for its own sake.**
The only geometric element is the lime dot in `Campus.` and the step indicators on the landing page. The rest is pure information design.

---

*Apply this prompt after completing task.md steps 0–7. This replaces the previous black-and-white task2.md entirely.*
