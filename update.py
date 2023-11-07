import customtkinter 
import sqlite3 
import pandas as pd 


def UpdateWorker(ID, db):
    def AddEntry():
        db.Update(values = (int(age_entry.get()), department_entry.get(), int(Education_entry.get()), EducationField_entry.get(),
                            int(EmployeeNumber_entry.get()), GENDER_entry.get(), int(JobLevel_entry.get()), JobRole_entry.get(),
                            MaritalStatus_entry.get(), FECHA_DE_INGRESO_entry.get(), FECHA_DE_CESE_entry.get(), float(MonthlyIncome_entry.get()),
                            Ovetime_entry.get(), int(EnvironmentSatisfaction_entry.get()),int(JobSatisfaction_entry.get()), int(PerformanceRating_entry.get()),
                            int(WorkLifeBalance_entry.get())
                            ),ID=ID)
    fields = pd.read_sql_query(f'SELECT * FROM resignations WHERE ID = {ID}',db.conn)
    insert_window = customtkinter.CTk()
    insert_window.geometry("1400x400")
    insert_window.title("Insert Data")
    frame3 = customtkinter.CTkFrame(master=insert_window,width=2000)
    frame3.pack(pady=20, padx=20 ,fill='both', expand=True)
    resign_search= customtkinter.CTkLabel(master=frame3, text="Update Worker", text_color='Red', font=("Arial",16),)
    resign_search.grid(row=0, column=0, pady=12, padx=10)

    #insert Age
    age_entry = customtkinter.CTkEntry(master=frame3, width=200,placeholder_text=' Age(INT)')
    age_entry.grid(row=1, column=0, pady=12, padx=10)
    age_entry.insert(0,fields['Age'].values[0])
    #insert Department
    department_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert Department(TEXT)")
    department_entry.grid(row=1, column=1, pady=12, padx=10)
    department_entry.insert(0,fields['Department'].values[0])
    #insert Education
    Education_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert Education(INT)")
    Education_entry.grid(row=1, column=2, pady=12, padx=10)
    Education_entry.insert(0,fields['Education'].values[0])
    #insert EducationField
    EducationField_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert Education Field(TEXT)")
    EducationField_entry.grid(row=1, column=3, pady=12, padx=10)
    EducationField_entry.insert(0,fields['EducationField'].values[0])
    #EducationField_entry EmployeeNumber
    EmployeeNumber_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert EmployeeNumber Field(INT)")
    EmployeeNumber_entry.grid(row=2, column=0, pady=12, padx=10)
    EmployeeNumber_entry.insert(0,fields['EmployeeNumber'].values[0])
    #insert GENDER
    GENDER_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert GENDER(TEXT)")
    GENDER_entry.grid(row=2, column=1, pady=12, padx=10)
    GENDER_entry.insert(0,fields['Gender'].values[0])
    #insert JobLevel
    JobLevel_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert JobLevel(INT)")
    JobLevel_entry.grid(row=2, column=2, pady=12, padx=10)
    JobLevel_entry.insert(0,fields['JobLevel'].values[0])
    #insert JobRole
    JobRole_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert JobRole(TEXT)")
    JobRole_entry.grid(row=2, column=3, pady=12, padx=10)
    JobRole_entry.insert(0,fields['JobRole'].values[0])
    #insert MaritalStatus
    MaritalStatus_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert MaritalStatus(TEXT)")
    MaritalStatus_entry.grid(row=3, column=0, pady=12, padx=10)
    MaritalStatus_entry.insert(0,fields['MaritalStatus'].values[0])
    #insert FECHA_DE_INGRESO
    FECHA_DE_INGRESO_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert FECHA_DE_INGRESO(DD/MM/YYYY)")
    FECHA_DE_INGRESO_entry.grid(row=3, column=1, pady=12, padx=10)
    FECHA_DE_INGRESO_entry.insert(0,fields['FECHA_DE_INGRESO'].values[0])
    #insert FECHA_DE_CESE
    FECHA_DE_CESE_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert FECHA_DE_CESE(DD/MM/YYYY)")
    FECHA_DE_CESE_entry.grid(row=3, column=2, pady=12, padx=10)
    FECHA_DE_CESE_entry.insert(0,fields['FECHA_DE_CESE'].values[0])
    #insert MonthlyIncome
    MonthlyIncome_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert MonthlyIncome(Float)")
    MonthlyIncome_entry.grid(row=3, column=3, pady=12, padx=10)
    MonthlyIncome_entry.insert(0,fields['MonthlyIncome'].values[0])
    #insert Overtime
    Ovetime_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert Overtime(TEXT)")
    Ovetime_entry.grid(row=4, column=0, pady=12, padx=10)
    Ovetime_entry.insert(0,fields['Ovetime'].values[0])
    #insert EnvironmentSatisfaction
    EnvironmentSatisfaction_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert EnvironmentSatisfaction(INT)")
    EnvironmentSatisfaction_entry.grid(row=4, column=1, pady=12, padx=10)
    EnvironmentSatisfaction_entry.insert(0,fields['EnvironmentSatisfaction'].values[0])
    #insert PerformanceRating
    PerformanceRating_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert PerformanceRating(INT)")
    PerformanceRating_entry.grid(row=4, column=2, pady=12, padx=10)
    PerformanceRating_entry.insert(0,fields['PerformanceRating'].values[0])
    #insert JobSatisfaction
    JobSatisfaction_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert JobSatisfaction(INT)")
    JobSatisfaction_entry.grid(row=4, column=3, pady=12, padx=10)
    JobSatisfaction_entry.insert(0,fields['JobSatisfaction'].values[0])
    #insert WorkLifeBalance

    WorkLifeBalance_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert WorkLifeBalance(INT)")
    WorkLifeBalance_entry.grid(row=5, column=0, pady=12, padx=10)
    WorkLifeBalance_entry.insert(0,fields['WorkLifeBalance'].values[0])
    Insert = customtkinter.CTkButton(master=frame3, text="Update Worker", command=AddEntry,
                                        bg_color='Green', fg_color='Green',)
    Insert.grid(row=6, column=0,columnspan = 4, pady=12, padx=10,sticky='ew')
    insert_window.mainloop()

