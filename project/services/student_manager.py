# services/student_manager.py

import csv
import os

class StudentManager:
    def __init__(self, filename="data/students.csv"):
        self.filename = filename
        
        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Roll No", "Name", "Age", "Grade"])

    # CREATE
    def add_student(self, student):
        if self.search_student(student.get_roll_no()):
            return False  

        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(student.to_list())
        return True

    # READ
    def view_students(self):
        with open(self.filename, "r") as file:
            return list(csv.DictReader(file))

    # SEARCH
    def search_student(self, roll_no):
        with open(self.filename, "r") as file:
            for row in csv.DictReader(file):
                if row["Roll No"] == roll_no:
                    return row
        return None

    # UPDATE
    def update_student(self, roll_no, updated_data):
        rows = self.view_students()
        updated = False

        for r in rows:
            if r["Roll No"] == roll_no:
                r.update(updated_data)
                updated = True
        
        if updated:
            with open(self.filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Roll No","Name","Age","Grade"])
                writer.writeheader()
                writer.writerows(rows)
        return updated

    # DELETE
    def delete_student(self, roll_no):
        rows = self.view_students()
        new_rows = [r for r in rows if r["Roll No"] != roll_no]

        if len(new_rows) == len(rows):
            return False

        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Roll No","Name","Age","Grade"])
            writer.writeheader()
            writer.writerows(new_rows)
        return True

    # FILTER
    def filter_students(self, grade=None, min_age=None, max_age=None):
        results = []
        for r in self.view_students():
            if grade and r["Grade"] != grade:
                continue
            if min_age and int(r["Age"]) < min_age:
                continue
            if max_age and int(r["Age"]) > max_age:
                continue
            results.append(r)
        return results

    # SORT
    def sort_students(self, by="Name"):
        return sorted(self.view_students(), key=lambda x: x[by])