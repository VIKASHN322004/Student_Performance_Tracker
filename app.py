import streamlit as st
import pandas as pd
import plotly.express as px
file_path = "student_details.csv"
df = pd.read_csv(file_path)
st.title("Student Performance Analysis")
st.write(df)
exam_columns = [f"Exam{i}_Subject{j}" for i in range(1, 6) for j in range(1, 6)]
df["Total_Exam"] = df[exam_columns].sum(axis=1)
df["Average_Score"] = df[exam_columns].mean(axis=1)
st.title("Student Performance Analysis")
for i in range(1, 6):
    exam_column = f"Exam{i}_Total"
    subject_columns = [f"Exam{i}_Subject{j}" for j in range(1, 6)]
    df[exam_column] = df[subject_columns].sum(axis=1).rank(ascending=False, method='min')
performance_categories = {
    'Excellent': (90, 100),
    'Good': (80, 89),
    'Average': (70, 79),
    'Need Improvement': (60, 69),
    'Poor': (0, 59)
}
st.subheader("Updated Data")
st.write(df)
st.subheader("Total Scores in Each Exam")
total_scores = df[["Total_Exam"] + exam_columns].groupby("Total_Exam").sum()
st.bar_chart(total_scores)
st.subheader("Ranks in Each Exam")
for i in range(1, 6):
    exam_column = f"Exam{i}_Total"
    st.write(f"**Exam {i} Ranks**")
    ranks = df[["StudentID", "Name", exam_column]].sort_values(exam_column).head(1)
    st.write(ranks)
st.subheader("Performance Analysis for Each Student")
selected_student_id = st.sidebar.selectbox("Select Student ID:", df["StudentID"].unique())
selected_student_data = df[df["StudentID"] == selected_student_id]
st.subheader(f"Details for Student ID: {selected_student_id}")
st.write(selected_student_data)
st.subheader("Score Trend")
fig_line_chart = px.line(
    selected_student_data.T,
    title=f"Score Trend for Student ID: {selected_student_id}",
    labels={"value": "Score", "index": "Exams"}
)
st.plotly_chart(fig_line_chart)
st.subheader("Average Scores Across All Students")
average_scores = df[exam_columns].mean()
st.bar_chart(average_scores)
st.subheader("Performance Classification")
total_score_selected_student = selected_student_data["Total_Exam"].values[0]
performance_category = None
total_score_selected_student/=25
st.write(f"Total Score for Student ID {selected_student_id}: {total_score_selected_student}")
for category, (lower_bound, upper_bound) in performance_categories.items():
    st.write(f"Checking category: {category}, Range: ({lower_bound}, {upper_bound})")
    if lower_bound <= total_score_selected_student <= upper_bound:
        performance_category = category
        break
if performance_category:
    st.write(f"Performance Category for Student ID {selected_student_id}: {performance_category}")
else:
    st.warning("Performance category not found for the selected student. Check the defined ranges.")

st.subheader("Histograms for Each Exam")
for i in range(1, 6):
    exam_column = f"Exam{i}_Total"
    fig_hist = px.histogram(df, x=exam_column, nbins=20, title=f"Histogram for {exam_column}")
    st.plotly_chart(fig_hist)

st.subheader("Distribution of Performance Categories")
bounds = sorted([bound[0] for bound in performance_categories.values()] + [float('inf')])
performance_counts = pd.cut(df["Average_Score"], bins=bounds, labels=performance_categories.keys()).value_counts()
fig_pie = px.pie(
    names=performance_counts.index,
    values=performance_counts.values,
    title="Distribution of Performance Categories"
)
st.plotly_chart(fig_pie)
st.subheader("Download Updated CSV")
st.markdown(f"Download the updated dataset as a CSV file [here](/{file_path})")
