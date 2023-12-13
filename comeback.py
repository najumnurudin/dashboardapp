import streamlit as st
import mysql.connector
import random
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import calendar
from datetime import datetime
years = [datetime.today().year, datetime.today().year + 1]
months = list[calendar.month_name]
st.set_page_config(layout="wide")
#ine the configuration settings for your MySQL database
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="",
database="test"
)
mycursor=mydb.cursor()
print("Connection Established")

def main():
    # Left column
    col1, col2 = st.columns([3, 7])
    with col1:
        selected = option_menu(
        menu_title=None,
        options=["ALL PATIENT'S TABLE","REGISTER A NEW PATIENT","TRACK A PATIENT'S DEVELOPMENT"," PATIENT'S MEDICAL DATA"],
        default_index=0,
        orientation="vertical",
    )               

        
        # Right column
    with col2:
        # The all patients 
        if selected == "ALL PATIENT'S TABLE":
            st.write("ALL PATIENTS TABLE") 
            cnx = mysql.connector.connect(user='root', password='',host='localhost', database='test')
            cursor = cnx.cursor()
            # Execute the query to retrieve all rows
            query = "SELECT patients_name,parents_name, date_birth, address, phone  FROM registered_patients"
            cursor.execute(query)
            # Fetch all rows
            rows = cursor.fetchall()
            # Convert the rows to a pandas dataframe
            df = pd.DataFrame(rows, columns=[ "PATIENTS NAME","PARENTS NAME",  "DATE OF BIRTH","ADDRESS",  "PHONE"])    
            # Display the dataframe using Streamlit
            st.dataframe(df)
        # Right column
        # the development
        
        if selected == "REGISTER A NEW PATIENT":
            # database configuration
            # Connect to your MySQL database
                db_connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="test"
                )

                # Create a cursor object to interact with the database
                cursor = db_connection.cursor()
                # Get user input for table name
                with st.form("entry_form", clear_on_submit=True):
                    st.info("Patient Registration")   
                    a,b,c = st.tabs(["IDENTIFICATION", "INFORMATION", "DATE"])   
                    with a:
                        st.write("")
                        patients_name = st.text_input("First Name")
                        other_names = st.text_input("SURNAME AND LAST NAME")
                        phone = st.number_input("Phone Number", value=0)
                        full_name = patients_name + "" + other_names 
                        parents_name = st.text_input("Parent's Name")
                    with b:
                        age = st.number_input("Age",value=0)  
                        address = st.text_input("Address")
                        gender = st.selectbox("Gender", ["Male", "Female"])
                    with c:
                        date_birth = st.date_input("Date of Birth")
                        first_visit = st.date_input("First Visit")
                        reg_no = st.text_input("Registration No:")     
                        submit_button = st.form_submit_button()
                if submit_button:
                        st.write(full_name)
                        query = f"CREATE TABLE {patients_name} ( attendance_date date, patients_weight int, haemoglobin_level int, body_temperature int, milk_taking varchar(200), vaccine_provided varchar(200), umbilical_condition varchar(200), escorted_by varchar(200), relation_to_patient varchar(200), attendant varchar(200), attendant_job varchar(200), documentation varchar(200), height int, patients_muac int)"
                        sql = f"insert into registered_patients(patients_name,parents_name, age,date_birth, gender,address, reg_no, phone, first_visit) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        val = (patients_name,parents_name, age,date_birth, gender,address, reg_no, phone, first_visit)
                        cursor.execute(query)
                        cursor.execute(sql, val)
                        db_connection.commit()
                        st.success("Patients registered")         
        # The nutrition
        if selected == ("TRACK A PATIENT'S DEVELOPMENT"):
            st.write("TRACK A PATIENTS DEVELOPMENT")
            cnx = mysql.connector.connect(user='root', password='',
                              host='localhost', database='test')
            cursor = cnx.cursor()

            # Execute SQL query to retrieve names from database
            query = "SELECT patients_name FROM registered_patients"
            cursor.execute(query)
            names = [name[0] for name in cursor.fetchall()]

            # Create dropdown menu of names
            selected_name = st.selectbox('Select a name', names)

            # Execute SQL query to retrieve information for selected name
            query = f"SELECT attendance_date,patients_weight, haemoglobin_level, body_temperature, height, patients_muac FROM {selected_name}"
            cursor.execute(query)
            rows = cursor.fetchall()
            df = pd.DataFrame(rows, columns=["DATE","WEIGHT", "HB LEVEL", "TEMPERATURE", "HEIGHT", "MUAC"])
            st.dataframe(df)


            
        if selected == (" PATIENT'S MEDICAL DATA"):
            st.write("PATIENT'S MEDICAL DATA")
            cnx = mysql.connector.connect(user='root', password='',
                              host='localhost', database='test')
            cursor = cnx.cursor()

            # Execute SQL query to retrieve names from database
            query = "SELECT patients_name FROM registered_patients"
            cursor.execute(query)
            names = [name[0] for name in cursor.fetchall()]

            # Create dropdown menu of names
            selected_name = st.selectbox('Select a name', names)
            with st.form("entry_form", clear_on_submit=True):
                st.info(f" {selected_name + "'s"} Clinic attendance")
                a, b,c,d = st.tabs((["OBTAINED CLINICAL DATA","NUTRITIONAL DATA","UMBILICAL AND SKIN ASSESMENT","OTHER INF0RMATION"]))
                with a:
                    first_page, second_page = st.columns([1,1])
                    with first_page:                            
                        attendance_date = st.date_input("Date of attendance")
                        patients_weight = st.number_input("Patients weight in Kg",value=0)
                        haemoglobin_level = st.number_input("Haemogglobin Level",value=0)
                    with second_page:
                        body_temperature = st.number_input("Body Temperature in °C",value=0)
                        height = st.number_input("Height (cm)", value=0)
                        patients_muac = st.text_input("MUAC")
                    
                    
                with b:
                    milk_taking = st.selectbox("Breastfeeding", ["Mom's Milk (EBF)", "Alternative Milk (RF)"])
                    vaccine_provided = st.text_input("Enter the vaccine provided to the patient")                    
                with c:
                    umbilical_condition = st.selectbox("Umbilical Condition",["Dry and Clean", "Presence of Redness", "Smelly and producing pus"])
                with d:
                    col_1, col_2 = st.columns([1,1])
                    with col_1:
                        escorted_by = st.text_input("Parent or Guardian's name")
                        relation_to_patient = st.selectbox("Relationship", ["Mother", "Father", "Aunt", "Brother", "Sister", "Others"])
                    with col_2:
                        attendant = st.text_input("Medical Personnel Attendant")
                        attendant_job = st.text_input("Attendant's")
                    documentation = st.text_area("Documentation and Other Information")
                    submit_button = st.form_submit_button() 
                    if submit_button:
                        sql_two = f"INSERT INTO {selected_name} (attendance_date, patients_weight, haemoglobin_level, body_temperature, milk_taking, vaccine_provided, umbilical_condition, escorted_by, relation_to_patient, attendant, attendant_job, documentation, height,patients_muac) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        val_three = (attendance_date, patients_weight, haemoglobin_level, body_temperature, milk_taking, vaccine_provided, umbilical_condition, escorted_by, relation_to_patient, attendant, attendant_job, documentation, height,patients_muac)
                        mycursor.execute(sql_two, val_three)
                        mydb.commit()                            
                        st.success("Data Inserted Successfully!!!")
            
if __name__ == "__main__":
    main()
