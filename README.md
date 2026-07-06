# EduPro Learner Analysis — Project Package

## Files included
- `EduPro_Research_Paper.docx` — full EDA write-up with insights & recommendations (submit as-is or edit).
- `EduPro_Executive_Summary.docx` — 2-page stakeholder summary.
- `app.py` — Streamlit dashboard (source code).
- `EduPro_Online_Platform.xlsx` — your original data file (needed to run the app).

## Run the dashboard today

1. Install dependencies (one time):
   ```
   pip install streamlit pandas plotly openpyxl
   ```
2. Put `app.py` and `EduPro_Online_Platform.xlsx` in the same folder.
3. Run:
   ```
   streamlit run app.py
   ```
4. It opens in your browser at `http://localhost:8501`.

## What's in the dashboard
- **Sidebar filters:** Age group, Gender, Course Category, Course Level, Course Type.
- **KPI row:** Total Enrollments, Active Learners, Avg Courses/Learner, Female Share, Top Category.
- **4 tabs:**
  1. Demographic Overview (age & gender distributions, participation by group)
  2. Age-wise Enrollment (enrollments by age, age×level and age×category heatmaps)
  3. Gender Preferences (gender×level, gender×category)
  4. Category Popularity (category ranking, free vs paid, level distribution)

## If you want to deploy it live (not just run locally)
Free option: push `app.py` + the xlsx to a GitHub repo, then deploy on
[share.streamlit.io](https://share.streamlit.io) (Streamlit Community Cloud) —
takes about 5 minutes and gives you a public link, useful if your submission
requires a live demo link.

## Submission checklist
- [ ] Research paper (docx) — included
- [ ] Executive summary (docx) — included
- [ ] Streamlit dashboard — run locally or deploy for a live link
- [ ] (Optional) Record a short screen-capture video of the dashboard in case
      your evaluator can't run it themselves
