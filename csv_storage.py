# Interacts with the csv file
import csv
from schemas import Student, Student_Update
from pydantic import ValidationError
from fileinput import filename
import pandas as pd
import os

fields = ['id', 'name', 'Internship Domain', 'Phone no.', 'email']
filename = 'data/students.csv'




def initialize_storage():
    
    # os.path.getsize returns size of file
    is_empty = not os.path.isfile(filename) or os.path.getsize(filename) == 0

    with open(filename, 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        if is_empty:
            csv_writer.writerow(fields)



# getting the id, finding the last row
def get_next_id(file_obj):
        
    with open(file_obj, 'r', encoding='utf-8') as file:
        reader = list(csv.reader(file))

        #If the file has only headers return one
        if(len(reader)) <= 1:
            return 1
        
        # Get the ID from the very last row (index -1), first column (index 0)
        last_id = int(reader[-1][0])
        return last_id+1

            


def write_data(name, domain, phone_no, email):
    try:
        # 1. Validate the incoming data against the schema
        # Pass your function arguments into the Pydantic model using keyword arguments
        # Left side: Pydantic field names | Right side: your function input variables

        data = Student(
            name=name,
            internship_domain=domain,
            phone_no=phone_no,
            email=email
        )

        # If it passes validation add to the csv:
    
        
        
        next_id = get_next_id(filename)

        new_row = [next_id, data.name, data.internship_domain, data.phone_no, data.email]

        with open(filename, 'a', newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(new_row)
    
        return True, f"Successfully added row with generated ID: {next_id}"

    except ValidationError as e:
        return False, f"❌ Data Validation Failed! \n {e}"
        


        


def display(id = None):
    # Till where user want to read data
    table_data = []  # List to store rows
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        file_reader = csv.reader(file)

        
        # 1. Grab and append the header row 
        header = next(file_reader)
        table_data.append(header)
        #print(f"{header[0]:<5} {header[1]:<27} {header[2]:<25} {header[3]:<10}")
        #print("-" * 80)

        # 2. Append data rows
        for line in file_reader:
             table_data.append(line)
            #print(f"{line[0]:<5} {line[1]:<27} {line[2]:<25} {line[3]:<10}")
            # if the target id is matched printing stops, we compare them by safely converting to strings
             if id is not None and str(line[0]) == str(id):
                 #print(f"\n[Stopping display: Reached target ID {id}]")
                 break
    df = pd.DataFrame(table_data[1:], columns=table_data[0])
    df = df.set_index(header[0])   
    return df



# To delete a row in a CSV file, we cannot simply "erase" it in place. we must read the file, filter out the row we want to delete, and then overwrite the file with the remaining rows.
def delete_data(id: int):
    updated_rows = []
    row_deleted = False

    with open(filename, 'r', encoding='utf-8') as file:
        file_reader = csv.reader(file)
        header = next(file_reader) 
        updated_rows.append(header)
        
        # traverse in that reader object
        for line in file_reader:
            # Since id is in the first column
            if line[0] == str(id):
                row_deleted = True
                continue # skips this row (deletes it)
            updated_rows.append(line)


    # Overwriting the original file with updated rows
    if row_deleted == True:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            csv.writer(file).writerows(updated_rows)

        return True, f"Successfully deleted ID {id}."

    else :
        return False, f"ID {id} not found!"




# find Student with id:
def find(id: int):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        # looping to find the id
        for line in reader:
            if line[0] == str(id):
                return line
            
        print(f"Entry with ID {id} does not exist!")



def update(id, name = None, domain = None, phone_no = None, email = None):
    # To validate our data using our Pydantic model or Schema Class, we need to instantiate the class by passing our variables as keyword arguments (key=value).
    try:
        data = Student_Update(id=id,
                              name=name,
                              internship_domain=domain,
                              phone_no=phone_no,
                              email=email,
                          
                        )
    except ValidationError as e:
        return False, f"❌ Validation Failed for the new data!\n{e}"
    
    updated_rows = []
    row_present = False
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        updated_rows.append(header)
        # looping to find the id
        for line in reader:
            if line[0] == str(id):
                row_present = True

                if data.name is not None:
                    line[1] = data.name
                
                if data.internship_domain is not None:
                    line[2] = data.internship_domain

                if data.phone_no is not None:
                    line[3] = data.phone_no

                if data.email is not None:
                    line[4] = data.email

            updated_rows.append(line)

    # overwrite file with updated data
    if row_present:
        with open(filename, 'w', encoding='utf-8') as file:
            csv.writer(file).writerows(updated_rows)
        return True, f"Successfully updated record ID {id}."

    else:
        return False, f"Record with ID {id} not found."


def Delete_All():
    is_empty = not os.path.isfile(filename) or os.path.getsize(filename) == 0

    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        if is_empty:
            csv_writer.writerow(fields)

    return "All students have been successfully deleted."




    


