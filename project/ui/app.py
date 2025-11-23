# ui/app.py

import sys, os
# 🔧 FIX: Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from model.student import Student
from services.student_manager import StudentManager

st.title("📚 Student Management System")

manager = StudentManager()

menu = st.sidebar.selectbox(
    "Menu",
    ["Add Student", "View Students", "Search", "Update", "Delete", "Filter", "Sort"]
)

# ADD
if menu == "Add Student":
    st.header("➕ Add Student")

    roll = st.text_input("Roll No")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    grade = st.selectbox("Grade", ["A", "B", "C", "D", "F"])

    if st.button("Add"):
        try:
            student = Student(roll, name, age, grade)
            if manager.add_student(student):
                st.success("Student added!")
            else:
                st.error("Roll number already exists!")
        except Exception as e:
            st.error(str(e))

# VIEW
elif menu == "View Students":
    st.header("📄 All Students")
    st.table(manager.view_students())

# SEARCH
elif menu == "Search":
    st.header("🔍 Search Student")
    roll = st.text_input("Enter Roll Number")
    if st.button("Search"):
        result = manager.search_student(roll)
        if result:
            st.success(result)
        else:
            st.error("Student not found!")

# UPDATE
elif menu == "Update":
    st.header("✏️ Update Student")
    roll = st.text_input("Roll No to Update")

    name = st.text_input("New Name")
    age = st.number_input("New Age", min_value=1)
    grade = st.selectbox("New Grade", ["A", "B", "C", "D", "F"])

    if st.button("Update"):
        updated = manager.update_student(
            roll,
            {"Name": name, "Age": age, "Grade": grade}
        )
        if updated:
            st.success("Updated successfully!")
        else:
            st.error("Student not found.")

# DELETE
elif menu == "Delete":
    st.header("🗑 Delete Student")
    roll = st.text_input("Roll No to Delete")

    if st.button("Delete"):
        if manager.delete_student(roll):
            st.success("Deleted successfully!")
        else:
            st.error("Student not found.")

# FILTER
elif menu == "Filter":
    st.header("🎯 Filter Students")
    grade = st.selectbox("Filter by Grade", ["", "A", "B", "C", "D", "F"])
    min_age = st.number_input("Min Age", min_value=0)
    max_age = st.number_input("Max Age", min_value=0)

    if st.button("Apply Filter"):
        results = manager.filter_students(
            grade if grade else None,
            min_age if min_age else None,
            max_age if max_age else None
        )
        st.table(results)

# SORT
elif menu == "Sort":
    st.header("📊 Sort Students")
    sort_by = st.selectbox("Sort By", ["Name", "Age", "Grade"])
    st.table(manager.sort_students(sort_by))