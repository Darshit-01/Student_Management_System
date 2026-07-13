import streamlit as st

import csv_storage
from schemas import Student
csv_storage.initialize_storage()


st.markdown(
    """
    <style>
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #2563EB !important;
    }

    
 /* 1. Main app background (Charcoal Black) */
    .stApp {
        background-color: #0B0F19 !important;
    }
    
    /* 2. Sidebar background (Matte Black) */
    [data-testid="stSidebarContent"] {
        background-color: #111827 !important;
    }
    
    /* 3. Primary Text (Pure White) */
    h1, h2, h3, h4, h5, h6, th, strong, label, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #FFFFFF !important;
    }
    
    /* 4. Secondary Text (Light Gray) */
    p, span, td, .stMarkdown p, [data-testid="stWidgetLabel"] p {
        color: #D1D5DB !important;
    }
    
    /* 5. Electric Royal Blue Accents (Buttons) */
    div.stButton > button:first-child {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
    }

    div.stButton > button:first-child:hover {
        background-color: #3B82F6 !important;
    }
    
    /* 6. Input widgets styling */
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="textarea"] {
        background-color: #111827 !important;
        color: #FFFFFF !important;
    }

    .centered-text {
        text-align: center !important;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Student Management System")
st.text("Manage students efficiently")

# Side Bar Navigation:
choice = st.sidebar.radio("OPERATIONS:", ["View All Students", "Add Student", "Update Student", "Delete Student", "Delete All"])

#Trigger the function based on selection
if choice == "View All Students":
    
    student_data = csv_storage.display()
    # data sets the rows, columns=data sets the headers
    st.dataframe(student_data)



if choice == "Add Student":
    st.subheader("Enter All fields")

    # Creating form to batch user's inputs
    with st.form("student_entry_form"):
        Student_name = st.text_input("Name")
        Student_domain = st.text_input("Internship Domain")
        Student_phoneno = st.text_input("Phone Number")
        Student_email = st.text_input("Email")

        # Every st.form must have a submit button
        submitted = st.form_submit_button("Submit Data")

        if submitted:
            # 1. Frontend validation (Check for blanks)
            if not Student_name.strip() or not Student_domain.strip() or not Student_phoneno.strip() or not Student_email.strip():
                st.error("Please fill in all text fields.")

        # Pass to Backend / write_data function
            else:
                # Capture the two returned values from your function
                is_success, backend_message = csv_storage.write_data(Student_name, Student_domain, Student_phoneno, 
                                                                 Student_email)
                                                                 
                if is_success:
                    st.success(backend_message)

                else :
                    st.error(backend_message)


if choice == "Delete Student":
    st.subheader("Delete an entry")

    with st.form("enter id"):
        ID = st.text_input("Enter id of Student")

        # Submit button
        submitted = st.form_submit_button("Submit")

        if submitted:
            if not ID.isdigit():
                st.error("Validation Error: Student ID must contain only numbers!")
            
            else:
                is_success, backend_message = csv_storage.delete_data(ID)

                if is_success:
                    st.success(backend_message)

                else :
                    st.error(backend_message)


if choice == "Update Student":
    st.subheader("Only put the field/s to be updated")

    
    with st.form("Enter"):
        Student_id = st.text_input("ID")
        Student_name = st.text_input("Name")
        Student_domain = st.text_input("Internship Domain")
        Student_phoneno = st.text_input("Phone Number")
        Student_email = st.text_input("Email")

        # Submit button
        submitted = st.form_submit_button("Update")

        if submitted:
            #The Empty String Problem: When a user leaves a text box blank in Streamlit, st.text_input does not return None. It returns an empty string ("").
            
            # THE FIX: Convert empty strings ("") to actual None types
            # .strip() removes accidental spaces. 'or None' converts blanks to None.
            Student_name = Student_name.strip() or None
            Student_domain = Student_domain.strip() or None
            Student_phoneno = Student_phoneno.strip() or None
            Student_email = Student_email.strip() or None

            is_success, backend_message = csv_storage.update(Student_id, Student_name, Student_domain, Student_phoneno, Student_email)

            if is_success:
                st.success(backend_message)

            else:
                st.error(backend_message)

                

if choice == "Delete All":
    st.subheader("Delete Database")
    st.error("🚨 WARNING: Are you sure you want to delete all students? This action cannot be undone.")
    #A checkbox to force the user to confirm they read the warning
    confirm = st.checkbox("Yes, I understand that this will delete everything.")

    if confirm:
        st.success(csv_storage.Delete_All())


