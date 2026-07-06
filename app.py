"""
EduPro Learner Demographics and Course Enrollment Behavior Analysis
Streamlit Dashboard

Run with:  streamlit run app.py
Expects EduPro_Online_Platform.xlsx in the same folder (or update DATA_PATH below).
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="EduPro Learner Analytics",
    page_icon="📊",
    layout="wide",
)

DATA_PATH = "EduPro Online Platform.xlsx"

# ----------------------------------------------------------------------------
# Data loading & preparation
# ----------------------------------------------------------------------------
@st.cache_data
def load_data(path):
    users = pd.read_excel(path, sheet_name="Users")
    courses = pd.read_excel(path, sheet_name="Courses")
    transactions = pd.read_excel(path, sheet_name="Transactions")

    def age_band(age):
        if age < 18:
            return "<18"
        elif age <= 25:
            return "18-25"
        elif age <= 35:
            return "26-35"
        elif age <= 45:
            return "36-45"
        else:
            return "45+"

    users["AgeGroup"] = users["Age"].apply(age_band)

    merged = (
        transactions.merge(users, on="UserID", how="left")
        .merge(courses, on="CourseID", how="left")
    )
    return users, courses, transactions, merged


users, courses, transactions, merged = load_data(DATA_PATH)

AGE_ORDER = ["<18", "18-25", "26-35", "36-45", "45+"]
AGE_ORDER = [a for a in AGE_ORDER if a in users["AgeGroup"].unique()]
LEVEL_ORDER = ["Beginner", "Intermediate", "Advanced"]

# ----------------------------------------------------------------------------
# Sidebar filters
# ----------------------------------------------------------------------------
st.sidebar.title("🎓 EduPro Filters")

age_filter = st.sidebar.multiselect(
    "Age Group", options=AGE_ORDER, default=AGE_ORDER
)
gender_filter = st.sidebar.multiselect(
    "Gender", options=sorted(users["Gender"].unique()),
    default=sorted(users["Gender"].unique())
)
category_filter = st.sidebar.multiselect(
    "Course Category", options=sorted(courses["CourseCategory"].unique()),
    default=sorted(courses["CourseCategory"].unique())
)
level_filter = st.sidebar.multiselect(
    "Course Level", options=LEVEL_ORDER, default=LEVEL_ORDER
)
type_filter = st.sidebar.multiselect(
    "Course Type", options=sorted(courses["CourseType"].unique()),
    default=sorted(courses["CourseType"].unique())
)

filtered = merged[
    merged["AgeGroup"].isin(age_filter)
    & merged["Gender"].isin(gender_filter)
    & merged["CourseCategory"].isin(category_filter)
    & merged["CourseLevel"].isin(level_filter)
    & merged["CourseType"].isin(type_filter)
]

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.title("📊 EduPro: Learner Demographics & Course Enrollment Behavior")
st.caption(
    "Descriptive learner intelligence dashboard — explore who EduPro's learners "
    "are and how they choose courses."
)

# ----------------------------------------------------------------------------
# KPI row
# ----------------------------------------------------------------------------
total_enrollments = len(filtered)
unique_learners = filtered["UserID"].nunique()
avg_courses = round(total_enrollments / unique_learners, 2) if unique_learners else 0
female_share = (
    round(100 * filtered.drop_duplicates("UserID")["Gender"].eq("Female").mean(), 1)
    if unique_learners else 0
)
top_category = (
    filtered["CourseCategory"].value_counts().idxmax()
    if total_enrollments else "N/A"
)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Enrollments", f"{total_enrollments:,}")
c2.metric("Active Learners", f"{unique_learners:,}")
c3.metric("Avg. Courses / Learner", avg_courses)
c4.metric("Female Learner Share", f"{female_share}%")
c5.metric("Top Category", top_category)

st.divider()

# ----------------------------------------------------------------------------
# Tabs for the core modules
# ----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "👥 Demographic Overview",
        "📈 Age-wise Enrollment",
        "⚧ Gender Preferences",
        "📚 Category Popularity",
    ]
)

# --- Tab 1: Demographic overview -------------------------------------------
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        age_counts = (
            users[users["AgeGroup"].isin(age_filter) & users["Gender"].isin(gender_filter)]
            ["AgeGroup"].value_counts().reindex(AGE_ORDER).fillna(0)
        )
        fig = px.bar(
            age_counts, x=age_counts.index, y=age_counts.values,
            labels={"x": "Age Group", "y": "Number of Learners"},
            title="Learner Age Distribution", color_discrete_sequence=["#2E5EAA"]
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        gender_counts = users[
            users["AgeGroup"].isin(age_filter) & users["Gender"].isin(gender_filter)
        ]["Gender"].value_counts()
        fig = px.pie(
            gender_counts, names=gender_counts.index, values=gender_counts.values,
            title="Gender Distribution", color_discrete_sequence=["#2E5EAA", "#E8A33D"]
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Participation Rate by Demographic Group")
    participation = (
        filtered.groupby(["AgeGroup", "Gender"])["UserID"].nunique().reset_index(name="ActiveLearners")
    )
    fig = px.bar(
        participation, x="AgeGroup", y="ActiveLearners", color="Gender",
        barmode="group", category_orders={"AgeGroup": AGE_ORDER},
        title="Active Learners by Age Group and Gender",
        color_discrete_sequence=["#2E5EAA", "#E8A33D"]
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Tab 2: Age-wise enrollment ---------------------------------------------
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        enroll_age = filtered["AgeGroup"].value_counts().reindex(AGE_ORDER).fillna(0)
        fig = px.bar(
            enroll_age, x=enroll_age.index, y=enroll_age.values,
            labels={"x": "Age Group", "y": "Enrollments"},
            title="Enrollments by Age Group", color_discrete_sequence=["#5B9BD5"]
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        ct = pd.crosstab(filtered["AgeGroup"], filtered["CourseLevel"]).reindex(AGE_ORDER)
        ct = ct.reindex(columns=[c for c in LEVEL_ORDER if c in ct.columns])
        fig = px.imshow(
            ct, text_auto=True, color_continuous_scale="Blues",
            title="Age Group vs Course Level (Enrollments)"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Age Group vs Course Category Heatmap")
    ct2 = pd.crosstab(filtered["AgeGroup"], filtered["CourseCategory"]).reindex(AGE_ORDER)
    fig = px.imshow(ct2, text_auto=True, color_continuous_scale="Blues", aspect="auto")
    st.plotly_chart(fig, use_container_width=True)

# --- Tab 3: Gender preferences ----------------------------------------------
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        ct3 = pd.crosstab(filtered["Gender"], filtered["CourseLevel"])
        ct3 = ct3.reindex(columns=[c for c in LEVEL_ORDER if c in ct3.columns])
        fig = px.bar(
            ct3, barmode="group", title="Gender vs Course Level Preference",
            color_discrete_sequence=["#2E5EAA", "#5B9BD5", "#A8CBEE"]
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        ct4 = filtered.groupby(["Gender", "CourseCategory"]).size().reset_index(name="Enrollments")
        fig = px.bar(
            ct4, x="CourseCategory", y="Enrollments", color="Gender", barmode="group",
            title="Gender vs Course Category Preference",
            color_discrete_sequence=["#2E5EAA", "#E8A33D"]
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

# --- Tab 4: Category popularity ----------------------------------------------
with tab4:
    col1, col2 = st.columns(2)
    with col1:
        cat_counts = filtered["CourseCategory"].value_counts()
        fig = px.bar(
            cat_counts, x=cat_counts.values, y=cat_counts.index, orientation="h",
            labels={"x": "Enrollments", "y": "Category"},
            title="Course Category Popularity", color_discrete_sequence=["#2E5EAA"]
        )
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        type_counts = filtered["CourseType"].value_counts()
        fig = px.pie(
            type_counts, names=type_counts.index, values=type_counts.values,
            title="Free vs Paid Enrollments", color_discrete_sequence=["#2E5EAA", "#E8A33D"]
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Course Level Distribution")
    level_counts = filtered["CourseLevel"].value_counts().reindex(LEVEL_ORDER).fillna(0)
    fig = px.bar(
        level_counts, x=level_counts.index, y=level_counts.values,
        labels={"x": "Course Level", "y": "Enrollments"},
        title="Enrollments by Course Level", color_discrete_sequence=["#5B9BD5"]
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption(
    "EduPro Learner Demographics and Course Enrollment Behavior Analysis · "
    "Descriptive analytics only — no predictive or monetization modeling."
)
