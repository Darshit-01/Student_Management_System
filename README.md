# 🎓 Student Management System

A lightweight, robust Student Management System built with Streamlit for the frontend, Pydantic for rigorous data validation, and Pandas/CSV for local database storage.

This application allows users to seamlessly add, view, update, and delete student records through an intuitive dark-themed web interface.




## 🛠️ Technology Stack & Requirements

To run this project, you will need Python 3.8 or higher. Below are the required external libraries.

**requirements**:

streamlit>=1.28.0
pandas>=2.0.0
pydantic>=2.0.0
email-validator>=2.0.0  # Required for Pydantic's EmailStr



### Core Libraries Used

**Streamlit** : Powers the web-based user interface, routing, and form handling.

**Pandas** : Transforms the raw CSV data into an interactive, visually appealing data table on the frontend.

**Pydantic**: Handles backend data validation (ensuring emails are properly formatted, IDs are integers, etc.) before anything touches the database.

**CSV & OS (Built-in)**: Handles reading, writing, and managing the local students.csv file.




## ✨ Application Features

The app is divided into five core operations, accessible via the sidebar navigation:

1. **View All Students**: Displays the complete database in an interactive Pandas DataFrame. The table automatically uses the id column as the index for a clean look.

2. **Add Student**: A data entry form that strictly validates Names, Internship Domains, Phone Numbers, and Emails before generating an auto-incremented ID and saving to the CSV.

3. **Update Student**: Allows for partial updates. Users provide a target ID and only fill in the fields they wish to change. Blank fields are ignored, preserving the old data.

4. **Delete Student**: Safely removes a single student record based on their ID.

5. **Delete All**: A highly destructive action hidden behind a "red-light" warning and a physical confirmation checkbox to prevent accidental database wipes.



## 📂 Code Structure & Function Documentation

1. **schemas.py (Data Validation Models)**

This file dictates the rules for what constitutes valid student data using Pydantic.

    Student: The strict schema used when adding a new student. It requires name, internship_domain, phone_no, and email to be present and correctly formatted.

    Student_Update: The flexible schema used when updating a student. All fields (except the target id) are marked as Optional, allowing partial updates without triggering validation errors.


2. **csv_storage.py (The Database Engine)**

This module acts as the bridge between the app and the students.csv file.

`initialize_storage()`

        Checks if data/students.csv exists and is not empty. If it is missing, it creates the file and writes the column headers.

`get_next_id(file_obj)`

        Opens the CSV, looks at the very last row, and returns the previous ID + 1 to ensure unique, auto-incrementing IDs.

`write_data(name, domain, phone_no, email)`

        Validates incoming data against the Student schema. If valid, it gets the next ID and appends the new row to the CSV. Returns a success/failure boolean and a message.

`display(id=None)`

        Reads the CSV and converts it into a Pandas DataFrame. It intelligently sets the "id" column as the DataFrame index so Streamlit renders a clean table.

`update(id, name, domain, phone_no, email)`

        Implements the "Read, Merge, Validate" pattern. It validates incoming changes against Student_Update, loops through the CSV to find the target ID, safely merges new data with the old data, and overwrites the CSV file.

`delete_data(id)`

        Locates a specific ID, copies all other rows into a temporary list, and overwrites the CSV without the target row.

`find(id)`

        A helper function that searches the CSV for a specific ID and returns that exact row's data.

`Delete_All()`

        Completely wipes the students.csv file and immediately rewrites just the column headers so the app doesn't break on the next load.


3. **app.py (The Frontend Interface)**

The main entry point of the application.

    Custom Styling: Injects custom CSS to create a modern, sleek dark theme (Charcoal/Matte Black) with Electric Royal Blue accents for buttons and text.

    Form Handling (st.form): Uses Streamlit forms to batch user inputs, preventing the app from rerunning prematurely while users are typing.

    Variable Cleaning: Employs the variable.strip() or None Python logic to convert empty text boxes into pure None types, ensuring Pydantic processes optional fields correctly.


**How to run the app:**
Ensure your terminal is in the project folder and run:
Bash

**streamlit run app.py**
