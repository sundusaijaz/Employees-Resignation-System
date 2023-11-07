import customtkinter
from tkinter import messagebox,filedialog
import subprocess
import tkinter.font as tkfont
import requests 
from tkinter import DISABLED
from resignationprediction import ResignationPrediction
import cv2
from popup import popup_window
import matplotlib.pyplot as plt
from tkinter import ttk
import tkinter as tk
import pandas as pd 
import os 
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from database import Operations_window
#customtkinter.set_appearance_mode('dark')
root = customtkinter.CTk()
root.geometry("1350x550")

rp_obj = ResignationPrediction()

def browse_file():
    file_path = filedialog.askopenfilename()
    if not file_path.lower().endswith(('.xls','.xlsx')):
        messagebox.showerror("File Error","Only Excel File is Accepted")
    else:
        entry3.insert(0, file_path)
    



def execute():
    file_path = entry3.get()
    #username = entry1.get()
    #password = entry2.get()
    
    entry3.delete(0, 'end')
    print("Reading From:", file_path)
    # Call the sample function from the dynamic module
    rp_obj.preprocess(file_path)
    rp_obj.train()

def TrainFromDB():
    rp_obj.preprocess(None  )
    rp_obj.train()
def UploadToDataBase():
    file_path = entry3.get()
    #username = entry1.get()
    #password = entry2.get()
    
    entry3.delete(0, 'end')
    print("Reading From:", file_path)
    # Call the sample function from the dynamic module
    rp_obj.UploadSheetToDB(file_path)
def Predictions():
    rp_obj.predict()

def VisualizePossibleResignations():
    popup = tk.Tk()
    popup.title("All Possible Resignations")

    tree = ttk.Treeview(popup)
    possible_resignations = rp_obj.final_data[rp_obj.final_data['Predicted_Resigned']=='Yes']
    tree['columns'] = list(possible_resignations)

    for column in possible_resignations:
        tree.heading(column=column,text=str(column))
        tree.column(column,width=80)
    for index, row in possible_resignations.iterrows():
        tree.insert("","end",values = tuple(row))
    tree.pack()
    popup.mainloop()

def VoluntaryResignation(save=False):
    
    print(rp_obj.final_data.columns)
    resignation_data = rp_obj.final_data[rp_obj.final_data['Predicted_Resigned'] == 'Yes']

    #Count the number of resignations
    resignation_count = resignation_data.shape[0]

    # Create a bar chart
    plt.bar(['Employees Resigned', 'Employees Retained'], [resignation_count, rp_obj.final_data.shape[0] - resignation_count])
    plt.xlabel('Employee Status')
    plt.ylabel('Number of Employees')
    plt.title('Employees with Possible Resignation')
    if save == True:
        plt.savefig("charts/VoluntaryResignationChart.png")
        plt.clf()
    else:
        plt.show()
    
    
def AllPossibleBarCharts(save=False):
    
    resignation_data = rp_obj.final_data[rp_obj.final_data['Predicted_Resigned'] == 'Yes']
    print(resignation_data.columns)
    fig, axes = plt.subplots(3, 6, figsize=(15, 10))
    axes = axes.flatten()

    for index,col in enumerate(resignation_data.columns):
        if len(resignation_data[col].unique()) < 5:
            axes[index].barh([str(i) for i in list(resignation_data[col].value_counts().index)],
                    list(resignation_data[col].value_counts().values))
            axes[index].set_xlabel(f'{col}')
            axes[index].set_ylabel(f'{col} count')

        else:
            fig.delaxes(axes[index])
    if save == True:
        plt.savefig(f"charts/BarCharts.png")
    else:
        plt.tight_layout()
        plt.show()
        plt.clf()
    

def AllPossibleStackBarCharts(save=False):
    resignation_data = rp_obj.final_data[rp_obj.final_data['Predicted_Resigned'] == "Yes"].groupby('Gender').sum()
    cols = resignation_data.columns
    plt.bar(resignation_data.index,resignation_data[cols[0]].values,label=f'0')
    
    for index in range(1,len(cols)):
        
        plt.bar(resignation_data.index,resignation_data[cols[index]].values,
                bottom=resignation_data[cols[index-1]].values,label=f'{index}')
        plt.xlabel(f'{cols[index-1]}')
        plt.ylabel(f'{cols[index-1]} count')
        plt.show()
    if save == True:
        plt.savefig(f"charts/StackedCharts.png")
    else:

        plt.show()
def AllPossibleStackBarCharts(save=False):
    resignation_data = rp_obj.final_data[rp_obj.final_data['Predicted_Resigned'] == "Yes"]
    resignation_data.drop(columns="EmployeeNumber",inplace=True)
    resignation_data = resignation_data.groupby('Age').sum()
    #resignation_data.set_index('Age', inplace=True)
    ax = resignation_data.plot(kind='bar', stacked=True, figsize=(8, 6))
    plt.title('Stacked Bar Chart')
    plt.xlabel('Age')
    plt.ylabel('Sum')

    # Show the chart
    plt.show()

            

def AllPossiblePieCharts(save=False):
    resignation_data = rp_obj.final_data[rp_obj.final_data['Predicted_Resigned'] == 'Yes']
    fig, axes = plt.subplots(3, 6, figsize=(15, 10))
    axes = axes.flatten()
    for index,col in enumerate(resignation_data.columns):
        if len(resignation_data[col].unique()) < 5:
            axes[index].pie(list(resignation_data[col].value_counts().values),
                        labels= [str(i) for i in list(resignation_data[col].value_counts().index)],
                        )
            axes[index].set_title(f'Pie Chart {col}')

        else:
            fig.delaxes(axes[index])
    if save == True:
        plt.savefig(f"charts/PieCharts.png")
    else:
        plt.tight_layout()
        plt.show()
        plt.clf()
        
def AllPossibleLineCharts(save=False):
    resignation_data = rp_obj.final_data[rp_obj.final_data['Predicted_Resigned'] == "Yes"]
    fig, axes = plt.subplots(3, 6, figsize=(15, 10))
    axes = axes.flatten()
    for index,col in enumerate(resignation_data.columns):
        if len(resignation_data[col].unique()) < 5:
            axes[index].plot([str(i) for i in list(resignation_data[col].value_counts().index)],
                        list(resignation_data[col].value_counts().values))
            axes[index].set_xlabel(f'{col}')
            axes[index].set_ylabel(f'{col} count')
            

            
        else:
            fig.delaxes(axes[index])
    if save == True:
        plt.savefig(f"charts/LineCharts.png")
    else:
        plt.tight_layout()
        plt.show()
        plt.clf()
        

def DisplayVariables():
    
    popup = tk.Toplevel(root)
    popup.title("All Variables")

    def ShowContent(column_name):
        unique_values = rp_obj.final_data[column_name].unique()
        content = tk.Toplevel(root)
        label = tk.Label(content, text=f"{unique_values}").pack()
        content.mainloop()

    # Create multiple buttons in the popup
    for col in rp_obj.final_data.columns:
        tk.Button(popup, text=f"Click to View: {col}",
                    command= lambda col=col: ShowContent(col)).pack()
    popup.mainloop()

def DownloadAllGraphs():
    if os.path.exists("charts"):
        pass 
    else:
        os.mkdir('charts')
    print("[INFO] : Saving All Graphs to charts/")
    #AllPossibleStackBarCharts(save=True)
    AllPossiblePieCharts(save=True)
    AllPossibleLineCharts(save=True)
    VoluntaryResignation(save=True)
    AllPossibleBarCharts(save=True)
    plt.close()
    print("[INFO] : All Graphs Saved")


def DownloadPdfPredictions():
    print("[INFO] : Saving Predictions")
    pdf = SimpleDocTemplate("predictions_table.pdf", pagesize=letter)
    table_data = []
    for i, row in rp_obj.final_data.iterrows():
        table_data.append(list(row))

    table = Table(table_data)
    table_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ])

    table.setStyle(table_style)
    pdf_table = []
    pdf_table.append(table)

    pdf.build(pdf_table)
    print("[INFO] : Predictions Saved As predictions_table.pdf")
def DownloadExcelPredictions():
    temp = rp_obj.final_data.copy()
    temp['FECHA_DE_INGRESO'] = pd.to_datetime(temp['FECHA_DE_INGRESO'])
    temp['month'] =  temp['FECHA_DE_INGRESO'].dt.month
    temp['day'] =  temp['FECHA_DE_INGRESO'].dt.day
    temp['year'] =  temp['FECHA_DE_INGRESO'].dt.year
    temp.drop(columns =['FECHA_DE_INGRESO'],inplace=True)
    temp.to_excel("predictions.xlsx",index=False)
    
    print("[INFO] : Data SAVED IN EXCEL (predictions.xlsx)")


def on_hover(event):
    vis_resig_emp.configure(text_color='LightBlue',fg_color='Green',bg_color='Green')
def on_leave(event):
    vis_resig_emp.configure(text_color='Green',fg_color='Orange',bg_color='Orange')





frame = customtkinter.CTkFrame(master=root,width=2000)
frame.pack(pady=20, padx=20 ,fill='both', expand=True)



button_font = customtkinter.CTkFont(size=20)
button_font2 = customtkinter.CTkFont(size=18,weight='bold')


inner_frame = customtkinter.CTkFrame(master=frame)
inner_frame.pack()
def open_popup():
    popup_window(rp_obj)
popup_button = customtkinter.CTkButton(inner_frame, text="Search Filter", bg_color='Green', fg_color='Green',command=open_popup,)
popup_button.grid(row=0,column=2)
def Operations():
    Operations_window(rp_obj)
op_button = customtkinter.CTkButton(inner_frame, text="Operations", bg_color='Green', fg_color='Green',command=Operations)
op_button.grid(row=0,column=3)
label = customtkinter.CTkLabel(master=inner_frame, text="Employees Resignation \n Predictions", text_color='Green', font=("Arial", 40),)
label.grid(row=0, column=0, pady=20, padx=10)

entry3_variable = customtkinter.StringVar()
entry3 = customtkinter.CTkEntry(master=inner_frame, placeholder_text="File Path", textvariable=entry3_variable)
entry3.grid(row=1, column=0, pady=12, padx=10, sticky="ew")
entry3.configure(width=500)  # Set desired width of the entry widget

    
#HU-02 : Importing the database into the system
browse_button = customtkinter.CTkButton(master=inner_frame, text="Browse", command=browse_file,
                                        bg_color='Green', fg_color='Green', font=button_font)
browse_button.grid(row=1, column=1, pady=12, padx=10,sticky='ew')

entry1 = customtkinter.CTkButton(master=inner_frame, text="Add Data To DB", command=UploadToDataBase, bg_color='#0747ad', fg_color='#0747ad',)
entry1.grid(row=2, column=0, pady=12, padx=10, sticky="ew")

entry2 = customtkinter.CTkButton(master=inner_frame, text="Train From DB",command = TrainFromDB,bg_color='#0747ad', fg_color='#0747ad',)
entry2.grid(row=3, column=0, pady=12, padx=10,  sticky="ew")

#HU-04 : System to learn from the imported database
train_button = customtkinter.CTkButton(master=inner_frame, text="HU-04: Start Training", command=execute,
                                    bg_color='Green', fg_color='Green', font=button_font)
train_button.grid(row=4, column=0, columnspan=2, pady=12, padx=10, sticky="ew")


#HU-05 : System Predictions
predict_button = customtkinter.CTkButton(master=inner_frame, text='HU-05: Predict', command = Predictions,
                                        bg_color='#3d3db8',fg_color='#3d3db8', font=button_font)
predict_button.grid(row=5,column=0,columnspan=2,pady=12,padx=10,sticky='ew')

#HU-06: Visualize possible regisnation of employees from there table
vis_resig_emp = customtkinter.CTkButton(master=inner_frame,text='HU-06: Show Possible \n Resignations',command=VisualizePossibleResignations,
                                        fg_color='Orange',font=button_font2,text_color='Green')
vis_resig_emp.grid(row=1,column=2,columnspan=1,pady=12,padx=5,sticky='ew',)
vis_resig_emp.bind("<Enter>",on_hover)
vis_resig_emp.bind("<Leave>",on_leave)


#HU-07: Visualize possible regisnation of employees from there table

def on_hover1(event):
    vis_resig_emp2.configure(text_color='LightBlue',fg_color='Green',bg_color='Green')
def on_leave1(event):
    vis_resig_emp2.configure(text_color='Green',fg_color='Orange',bg_color='Orange')

vis_resig_emp2 = customtkinter.CTkButton(master=inner_frame,text='HU-07: Show Voluntary \n Resignations',command=VoluntaryResignation,
                                        fg_color='Orange',font=button_font2,text_color='Green')
vis_resig_emp2.grid(row=2,column=2,columnspan=1,pady=5,padx=5,sticky='ew',)


vis_resig_emp2.bind("<Enter>",on_hover1)
vis_resig_emp2.bind("<Leave>",on_leave1)
#HU-08: Display Predictibility Meter

def on_hover3(event):
    vis_resig_emp3.configure(text_color='LightBlue',fg_color='Green',bg_color='Green')
def on_leave3(event):
    vis_resig_emp3.configure(text_color='Green',fg_color='Orange',bg_color='Orange')

vis_resig_emp3 = customtkinter.CTkButton(master=inner_frame,text='HU-08: Display Predictibility \n Meter',command=rp_obj.ClassificationReport,
                                        fg_color='Orange',font=button_font2,text_color='Green')
vis_resig_emp3.grid(row=1,column=3,columnspan=1,pady=5,padx=5,sticky='ew',)


vis_resig_emp3.bind("<Enter>",on_hover3)
vis_resig_emp3.bind("<Leave>",on_leave3)

#HU-09: Download Table

def on_hover4(event):
    vis_resig_emp4.configure(text_color='LightBlue',fg_color='Green',bg_color='Green')
def on_leave4(event):
    vis_resig_emp4.configure(text_color='Green',fg_color='Orange',bg_color='Orange')

vis_resig_emp4 = customtkinter.CTkButton(master=inner_frame,text='HU-09: Download \n Predictions(PDF)',command=DownloadPdfPredictions,
                                        fg_color='Orange',font=button_font2,text_color='Green')
vis_resig_emp4.grid(row=2,column=3,columnspan=1,pady=5,padx=5,sticky='ew',)


vis_resig_emp4.bind("<Enter>",on_hover4)
vis_resig_emp4.bind("<Leave>",on_leave4)

#HU-10 Bar Charts
def on_hover5(event):
    vis_resig_emp5.configure(text_color='LightBlue',fg_color='Green',bg_color='Green')
def on_leave5(event):
    vis_resig_emp5.configure(text_color='Green',fg_color='Orange',bg_color='Orange')

vis_resig_emp5 = customtkinter.CTkButton(master=inner_frame,text='HU-10: Show Charts',command=AllPossibleBarCharts,
                                        fg_color='Orange',font=button_font2,text_color='Green')
vis_resig_emp5.grid(row=3,column=2,columnspan=1,pady=5,padx=5,sticky='ew',)
vis_resig_emp5.bind("<Enter>",on_hover5)
vis_resig_emp5.bind("<Leave>",on_leave5)
#HU-11 Pie  Charts

def on_hover11(event):
    vis_resig_emp11.configure(text_color='LightBlue',fg_color='Green',bg_color='Green')
def on_leave11(event):
    vis_resig_emp11.configure(text_color='Green',fg_color='Orange',bg_color='Orange')

vis_resig_emp11 = customtkinter.CTkButton(master=inner_frame,text='HU-11: Show Pie Chart',command=AllPossiblePieCharts,
                                        fg_color='Orange',font=button_font2,text_color='Green')
vis_resig_emp11.grid(row=4,column=3,columnspan=1,pady=5,padx=5,sticky='ew',)
vis_resig_emp11.bind("<Enter>",on_hover11)
vis_resig_emp11.bind("<Leave>",on_leave11)




#HU-13 Pie  Charts

def on_hover13(event):
    vis_resig_emp13.configure(text_color='LightBlue',fg_color='Green',bg_color='Green')
def on_leave13(event):
    vis_resig_emp13.configure(text_color='Green',fg_color='Orange',bg_color='Orange')

vis_resig_emp13 = customtkinter.CTkButton(master=inner_frame,text='HU-11: Show Line Chart',command=AllPossibleLineCharts,
                                        fg_color='Orange',font=button_font2,text_color='Green')
vis_resig_emp13.grid(row=5,column=3,columnspan=1,pady=5,padx=5,sticky='ew',)
vis_resig_emp13.bind("<Enter>",on_hover13)
vis_resig_emp13.bind("<Leave>",on_leave13)

#HU-14 Display Variables
def on_hover6(event):
    vis_resig_emp6.configure(text_color='LightBlue',fg_color='Green',bg_color='Green')
def on_leave6(event):
    vis_resig_emp6.configure(text_color='Green',fg_color='Orange',bg_color='Orange')

vis_resig_emp6 = customtkinter.CTkButton(master=inner_frame,text='HU-14: Display Variables',command=DisplayVariables,
                                        fg_color='Orange',font=button_font2,text_color='Green')
vis_resig_emp6.grid(row=4,column=2,columnspan=1,pady=5,padx=5,sticky='ew',)
vis_resig_emp6.bind("<Enter>",on_hover6)
vis_resig_emp6.bind("<Leave>",on_leave6)

#HU-15 Download All Charts
def on_hover7(event):
    vis_resig_emp7.configure(text_color='LightBlue',fg_color='Green',bg_color='Green')
def on_leave7(event):
    vis_resig_emp7.configure(text_color='Green',fg_color='Orange',bg_color='Orange')

vis_resig_emp7 = customtkinter.CTkButton(master=inner_frame,text='HU-15: Download Graphs',command=DownloadAllGraphs,
                                        fg_color='Orange',font=button_font2,text_color='Green')
vis_resig_emp7.grid(row=3,column=3,columnspan=1,pady=5,padx=5,sticky='ew',)
vis_resig_emp7.bind("<Enter>",on_hover7)
vis_resig_emp7.bind("<Leave>",on_leave7)



#HU-16 Download Table
def on_hover8(event):
    vis_resig_emp8.configure(text_color='LightBlue',fg_color='Green',bg_color='Green')
def on_leave8(event):
    vis_resig_emp8.configure(text_color='Green',fg_color='Orange',bg_color='Orange')

vis_resig_emp8 = customtkinter.CTkButton(master=inner_frame,text='HU-15: Download Prediction \n Table (excel)',command=DownloadExcelPredictions,
                                        fg_color='Orange',font=button_font2,text_color='Green')
vis_resig_emp8.grid(row=5,column=2,columnspan=1,pady=5,padx=5,sticky='ew',)
vis_resig_emp8.bind("<Enter>",on_hover8)
vis_resig_emp8.bind("<Leave>",on_leave8)




#HU-17 Download Table

vis_resig_emp9 = customtkinter.CTkButton(master=inner_frame,text='HU-17: Exit',command=lambda : root.destroy(),
                                        fg_color='#ed1f37',bg_color='#ed1f37',font=button_font2,text_color='White')
vis_resig_emp9.grid(row=6,column=3,columnspan=1,padx=5,sticky='ew',)


#HU-13 Download Table

vis_resig_emp9 = customtkinter.CTkButton(master=inner_frame,text='HU-17: Show Stacked Charts',command=AllPossibleStackBarCharts,
                                        fg_color='Orange',font=button_font2,text_color='Green')
vis_resig_emp9.grid(row=6,column=2,columnspan=1,padx=5,sticky='ew',)


#HU-18 Change Theme
def change_theme(event):
    selected_theme = theme.get()

    if selected_theme == "Light Theme":
        #root.tk_setPalette(background='#FFFFFF', foreground='#000000')
        customtkinter.set_appearance_mode('light')

    elif selected_theme == "Dark Theme":
        #root.tk_setPalette(background='#000000', foreground='#FFFFFF')
        customtkinter.set_appearance_mode('dark')

theme = customtkinter.CTkComboBox(master=inner_frame, values = ['Light Theme','Dark Theme'],command=change_theme,
                                    fg_color='Green',bg_color='Green',text_color='White')
theme.grid(row=2,column=1,columnspan=1,padx=5,sticky='ew',)

theme.set("Light")

#HU-20 Help Button
def displayGuide():
    img = cv2.imread("guide.png")
    cv2.imshow("System Guide",img)
    cv2.waitKey()
    cv2.destroyAllWindows()


help = customtkinter.CTkButton(master=inner_frame,text='HU-20: System Guide',command=displayGuide,
                                        fg_color='#ed1f37',bg_color='#ed1f37',font=button_font2,text_color='White')
help.grid(row=3,column=1,columnspan=1,padx=5,sticky='ew',)

root.mainloop()
