import sqlite3
import customtkinter
import tkinter as tk
from tkinter import ttk
import pandas as pd
from update import UpdateWorker
# Create or connect to the SQLite database
rp_obj = None
class DATABASE():
    def __init__(self):
        self.conn = sqlite3.connect('Employees.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='resignations';")
        table_exists = self.cursor.fetchone()[0] == 1
        if not table_exists:
            self.cursor.execute('''
                CREATE TABLE resignations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Age INTEGER,
                    Department TEXT,
                    Education INTEGER,
                    EducationField TEXT,
                    EmployeeNumber INTEGER,
                    Gender TEXT,
                    JobLevel INTEGER,
                    JobRole TEXT,
                    MaritalStatus TEXT,
                    FECHA_DE_INGRESO TEXT,
                    FECHA_DE_CESE DATETIME,
                    MonthlyIncome REAL,
                    Ovetime TEXT,
                    EnvironmentSatisfaction INTEGER,
                    JobSatisfaction INTEGER,
                    PerformanceRating INTEGER,
                    WorkLifeBalance INTEGER
                );
            ''')
            self.conn.commit()

            print("[INFO] : DataBase resignations Created")
        else:
            print('[INFO] Table resignations EXISTS')
    
    def Insert(self,values):
        self.cursor.execute("INSERT INTO resignations (Age, Department, Education, EducationField,EmployeeNumber,GENDER,JobLevel, JobRole, MaritalStatus, FECHA_DE_INGRESO, FECHA_DE_CESE, MonthlyIncome, Ovetime, EnvironmentSatisfaction, JobSatisfaction,PerformanceRating,WorkLifeBalance ) VALUES (?, ?, ?, ?,?,?,?, ?, ?, ?, ?, ?, ?, ?, ?,?,? );",\
                            values)
        self.conn.commit()
        print("[INFO]: Data Inserted Successfully")

    def Update(self,values, ID):
        update_query = """
    UPDATE resignations
    SET
        Age = ?,
        Department = ?,
        Education = ?,
        EducationField = ?,
        EmployeeNumber = ?,
        GENDER = ?,
        JobLevel = ?,
        JobRole = ?,
        MaritalStatus = ?,
        FECHA_DE_INGRESO = ?,
        FECHA_DE_CESE = ?,
        MonthlyIncome = ?,
        Ovetime = ?,
        EnvironmentSatisfaction = ?,
        JobSatisfaction = ?,
        PerformanceRating = ?,
        WorkLifeBalance = ?
    WHERE ID = ?
"""
        self.cursor.execute(update_query,values+(ID,))
        self.conn.commit()
        print("[INFO]: Data Updaed Successfully")






    def ShowTables(self):
        temp_df = pd.read_sql_query("SELECT * from resignations",self.conn)
        tree_pop = tk.Tk()
        tree_pop.title("Search Data")
        tree = ttk.Treeview(tree_pop)
        tree['columns'] = list(temp_df)

        for column in temp_df:
            tree.heading(column=column,text=str(column))
            tree.column(column,width=80)
        for index, row in temp_df.iterrows():
            tree.insert("","end",values = tuple(row))
        tree.pack()
    def DeleteQuery(self,id):
        self.cursor.execute("DELETE FROM resignations WHERE id=?", (int(id),))
        self.conn.commit()
        #self.cursor.close()
        print("[INFO]: Data Deleted Successfully")

    def DeleteTable(self):
        self.cursor.execute(f"DROP TABLE IF EXISTS resignations;")
        self.conn.commit()
        #self.cursor.close()

db =  DATABASE()

def Insert():
    def AddEntry():
        db.Insert(values = (int(age_entry.get()), department_entry.get(), int(Education_entry.get()), EducationField_entry.get(),
                            int(EmployeeNumber_entry.get()), GENDER_entry.get(), int(JobLevel_entry.get()), JobRole_entry.get(),
                            MaritalStatus_entry.get(), FECHA_DE_INGRESO_entry.get(), FECHA_DE_CESE_entry.get(), float(MonthlyIncome_entry.get()),
                            Ovetime_entry.get(), int(EnvironmentSatisfaction_entry.get()),int(JobSatisfaction_entry.get()), int(PerformanceRating_entry.get()),
                            int(WorkLifeBalance_entry.get())
                            ))
    insert_window = customtkinter.CTk()
    insert_window.geometry("1400x400")
    insert_window.title("Insert Data")
    frame3 = customtkinter.CTkFrame(master=insert_window,width=2000)
    frame3.pack(pady=20, padx=20 ,fill='both', expand=True)
    resign_search= customtkinter.CTkLabel(master=frame3, text="Insert Worker", text_color='Red', font=("Arial",16),)
    resign_search.grid(row=0, column=0, pady=12, padx=10)
    #insert Age
    age_entry = customtkinter.CTkEntry(master=frame3, width=200,placeholder_text='Insert Age(INT)')
    age_entry.grid(row=1, column=0, pady=12, padx=10)
    #insert Department
    department_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert Department(TEXT)")
    department_entry.grid(row=1, column=1, pady=12, padx=10)
    #insert Education
    Education_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert Education(INT)")
    Education_entry.grid(row=1, column=2, pady=12, padx=10)
    
    #insert EducationField
    EducationField_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert Education Field(TEXT)")
    EducationField_entry.grid(row=1, column=3, pady=12, padx=10)
    
    #insert EmployeeNumber
    EmployeeNumber_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert EmployeeNumber Field(INT)")
    EmployeeNumber_entry.grid(row=2, column=0, pady=12, padx=10)

    #insert GENDER
    GENDER_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert GENDER(TEXT)")
    GENDER_entry.grid(row=2, column=1, pady=12, padx=10)

    #insert JobLevel
    JobLevel_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert JobLevel(INT)")
    JobLevel_entry.grid(row=2, column=2, pady=12, padx=10)

    #insert JobRole
    JobRole_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert JobRole(TEXT)")
    JobRole_entry.grid(row=2, column=3, pady=12, padx=10)

    #insert MaritalStatus
    MaritalStatus_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert MaritalStatus(TEXT)")
    MaritalStatus_entry.grid(row=3, column=0, pady=12, padx=10)

    #insert FECHA_DE_INGRESO
    FECHA_DE_INGRESO_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert FECHA_DE_INGRESO(DD/MM/YYYY)")
    FECHA_DE_INGRESO_entry.grid(row=3, column=1, pady=12, padx=10)

    #insert FECHA_DE_CESE
    FECHA_DE_CESE_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert FECHA_DE_CESE(DD/MM/YYYY)")
    FECHA_DE_CESE_entry.grid(row=3, column=2, pady=12, padx=10)

    #insert MonthlyIncome
    MonthlyIncome_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert MonthlyIncome(Float)")
    MonthlyIncome_entry.grid(row=3, column=3, pady=12, padx=10)

    #insert Overtime
    Ovetime_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert Overtime(TEXT)")
    Ovetime_entry.grid(row=4, column=0, pady=12, padx=10)

    #insert EnvironmentSatisfaction
    EnvironmentSatisfaction_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert EnvironmentSatisfaction(INT)")
    EnvironmentSatisfaction_entry.grid(row=4, column=1, pady=12, padx=10)

    #insert PerformanceRating
    PerformanceRating_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert PerformanceRating(INT)")
    PerformanceRating_entry.grid(row=4, column=2, pady=12, padx=10)

    #insert JobSatisfaction
    JobSatisfaction_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert JobSatisfaction(INT)")
    JobSatisfaction_entry.grid(row=4, column=3, pady=12, padx=10)
    #insert WorkLifeBalance
    WorkLifeBalance_entry = customtkinter.CTkEntry(master=frame3, width=300,placeholder_text="Insert WorkLifeBalance(INT)")
    WorkLifeBalance_entry.grid(row=5, column=0, pady=12, padx=10)

    Insert = customtkinter.CTkButton(master=frame3, text="Insert Worker", command=AddEntry,
                                        bg_color='Green', fg_color='Green',)
    Insert.grid(row=6, column=0,columnspan = 4, pady=12, padx=10,sticky='ew')
    insert_window.mainloop()




def DeleteWorker():
    def Delete():
        db.DeleteQuery(id = worker_id.get())
    delete_window = customtkinter.CTk()
    delete_window.geometry("900x200")
    delete_window.title("Delete Worker")
    frame4 = customtkinter.CTkFrame(master=delete_window,width=2000)
    frame4.pack(pady=20, padx=20 ,fill='both', expand=True)
    worker_id = customtkinter.CTkEntry(master=frame4, width=300,placeholder_text="Insert ID")
    worker_id.grid(row=1, column=0, pady=12, padx=10)
    delete_button = customtkinter.CTkButton(master=frame4, text="Delete", command=Delete,
                                        bg_color='Red', fg_color='Red',)
    delete_button.grid(row=1, column=1,columnspan = 4, pady=12, padx=10,sticky='ew')
    delete_window.mainloop()


def DeletedTable():
    def Drop():
        db.DeleteTable()
    delete_window = customtkinter.CTk()
    delete_window.geometry("900x200")
    delete_window.title("Delete Table")
    frame4 = customtkinter.CTkFrame(master=delete_window,width=2000)
    frame4.pack(pady=20, padx=20 ,fill='both', expand=True)
    worker_id = customtkinter.CTkLabel(master=frame4, width=300,text="Are Your Sure?")
    worker_id.grid(row=1, column=0, pady=12, padx=10)
    delete_button_yes = customtkinter.CTkButton(master=frame4, text="Yes", command=Drop,
                                        bg_color='Red', fg_color='Red',)
    delete_button_yes.grid(row=1, column=1, pady=12, padx=10)

    delete_button_no = customtkinter.CTkButton(master=frame4, text="No", command=lambda : delete_window.destroy(),
                                        bg_color='Green', fg_color='Green',)
    delete_button_no.grid(row=1, column=2, pady=12, padx=10)
    delete_window.mainloop()


def DeletedColumn(x):
    rp_obj = x
    
    def DropColumn():
        rp_obj.temp_data.drop(columns = [del_col.get()],inplace=True)
        print(f"[INFO] : Column {del_col.get()} Dropped")
        tree_pop = tk.Tk()
        tree_pop.title("Search Data")
        tree = ttk.Treeview(tree_pop)
        tree['columns'] = list(rp_obj.temp_data)

        for column in rp_obj.temp_data:
            tree.heading(column=column,text=str(column))
            tree.column(column,width=80)
        for index, row in rp_obj.temp_data.iterrows():
            tree.insert("","end",values = tuple(row))
        tree.pack()
        tree_pop.mainloop()
    delete_col_window = customtkinter.CTk()
    delete_col_window.geometry("900x200")
    delete_col_window.title("Delete Column")
    frame5 = customtkinter.CTkFrame(master=delete_col_window,width=2000)
    frame5.pack(pady=20, padx=20 ,fill='both', expand=True)
    worker_id = customtkinter.CTkLabel(master=frame5, width=300,text="Select Column To Drop")
    worker_id.grid(row=1, column=0, pady=12, padx=10)
    del_col = customtkinter.CTkComboBox(master=frame5, values = sorted([str(i) for i in rp_obj.temp_data.columns]),
                                    fg_color='Green',bg_color='Green',text_color='White')
    del_col.grid(row=1,column=1,columnspan=1,padx=5)
    delete_button_no = customtkinter.CTkButton(master=frame5, text="Delete", command=DropColumn,
                                        bg_color='Red', fg_color='Red',)
    delete_button_no.grid(row=1, column=2, pady=12, padx=10)
    delete_col_window.mainloop()

def EditWorker():
    def GetWorkerID():
        ID = ed_worker_id.get()
        UpdateWorker(ID,db)
        
    EditWorker_window = customtkinter.CTk()
    EditWorker_window.geometry("900x200")
    EditWorker_window.title("Edit Worker")
    frame6 = customtkinter.CTkFrame(master=EditWorker_window,width=2000)
    frame6.pack(pady=20, padx=20 ,fill='both', expand=True)
    ed_worker_id = customtkinter.CTkEntry(master=frame6, width=300,placeholder_text="Enter Worker ID")
    ed_worker_id.grid(row=1, column=0, pady=12, padx=10)
    button_no = customtkinter.CTkButton(master=frame6, text="Select", command=GetWorkerID,
                                        bg_color='Red', fg_color='Red',)
    button_no.grid(row=1, column=2, pady=12, padx=10)
    EditWorker_window.mainloop()
def Operations_window(rp_obj):
    rp_obj = rp_obj
    popup_window = customtkinter.CTk()
    popup_window.geometry("900x200")
    frame2 = customtkinter.CTkFrame(master=popup_window,width=2000)
    frame2.pack(pady=20, padx=20 ,fill='both', expand=True)
    Insert_button = customtkinter.CTkButton(master=frame2, text="Insert Worker", command=Insert,
                                        bg_color='Green', fg_color='Green',)
    Insert_button.grid(row=2, column=4, pady=12, padx=10)


    ShowData_button = customtkinter.CTkButton(master=frame2, text="Show Data", command=db.ShowTables,
                                        bg_color='Green', fg_color='Green',)
    ShowData_button.grid(row=2, column=5, pady=12, padx=10)

    EditData_button = customtkinter.CTkButton(master=frame2, text="Edit Worker", command=EditWorker,
                                        bg_color='Green', fg_color='Green',)
    EditData_button.grid(row=2, column=6, pady=12, padx=10)

    Delete_button = customtkinter.CTkButton(master=frame2, text="Delete Column", command=lambda x = rp_obj:DeletedColumn(x),
                                        bg_color='Red', fg_color='Green',)
    Delete_button.grid(row=2, column=7, pady=12, padx=10)
    Delete_Column = customtkinter.CTkButton(master=frame2, text="Delete Worker", command=DeleteWorker,
                                        bg_color='Red', fg_color='Green',)
    Delete_Column.grid(row=2, column=8, pady=12, padx=10)
    Delete_Table = customtkinter.CTkButton(master=frame2, text="Delete Table", command=DeletedTable,
                                        bg_color='Red', fg_color='Red',)
    Delete_Table.grid(row=2, column=9, pady=12, padx=10)
    popup_window.mainloop()