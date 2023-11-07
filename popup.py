import customtkinter
import pandas as pd
import tkinter as tk
from tkinter import ttk
df = pd.read_excel("dataemployees.xlsx")
rp_obj = None


def popup_window(rp_obj):
    def CreateTree(temp_df):
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
        tree_pop.mainloop()
    def SearchFilterByAge(_):
        value = theme.get()
        temp_df = rp_obj.final_data[rp_obj.final_data['Age'] == int(value)]
        CreateTree(temp_df=temp_df)
    def SearchFilterByResign(_):
        value = resign_theme.get()
        temp_df = rp_obj.final_data[rp_obj.final_data['Predicted_Resigned'] == value]
        CreateTree(temp_df=temp_df)
    def SearchFilterByGender(_):
        value = gender_theme.get()
        temp_df = rp_obj.final_data[rp_obj.final_data['Gender'] == value]
        CreateTree(temp_df=temp_df)
    def BrowseAgeRange():
        from_ = From_theme.get()
        to_ = To_theme.get() 
        print(from_, to_)
        temp_df = rp_obj.final_data[(rp_obj.final_data['Age'] >= int(from_)) & \
                                    (rp_obj.final_data['Age'] <= int(to_))]
        CreateTree(temp_df=temp_df)

    rp_obj = rp_obj
    popup_window = customtkinter.CTk()
    popup_window.geometry("900x200")
    frame2 = customtkinter.CTkFrame(master=popup_window,width=2000)
    frame2.pack(pady=20, padx=20 ,fill='both', expand=True)
    # inner_frame = customtkinter.CTkFrame(master=frame2)
    # inner_frame.pack()


    # HU-21 : search by Name 
    
    age_search= customtkinter.CTkLabel(master=frame2, text="Search By Age", text_color='Green', font=("Arial",16),)
    age_search.grid(row=1, column=0, columnspan=1, pady=20, padx=10)
    theme = customtkinter.CTkComboBox(master=frame2, values = sorted([str(i) for i in rp_obj.final_data['Age'].unique()]),command= SearchFilterByAge,
                                    fg_color='Green',bg_color='Green',text_color='White')
    theme.grid(row=1,column=1,columnspan=1,padx=5,sticky='ew',)
    resign_search= customtkinter.CTkLabel(master=frame2, text="Resigned (Yes/No)", text_color='Green', font=("Arial",16),)
    resign_search.grid(row=1, column=2, columnspan=1, pady=20, padx=10)
    resign_theme = customtkinter.CTkComboBox(master=frame2, values = [str(i) for i in rp_obj.final_data['Predicted_Resigned'].unique()],command=SearchFilterByResign,
                                    fg_color='Green',bg_color='Green',text_color='White')
    resign_theme.grid(row=1,column=3,columnspan=1,padx=5,sticky='ew',)

    gender_search= customtkinter.CTkLabel(master=frame2, text="Gender", text_color='Green', font=("Arial",16),)
    gender_search.grid(row=1, column=4, columnspan=1, pady=20, padx=10)
    gender_theme = customtkinter.CTkComboBox(master=frame2, values = [str(i) for i in rp_obj.final_data['Gender'].unique()],command=SearchFilterByGender,
                                    fg_color='Green',bg_color='Green',text_color='White')
    gender_theme.grid(row=1,column=5,columnspan=1,padx=5,sticky='ew',)
    #Age Range
    From_search= customtkinter.CTkLabel(master=frame2, text="Age From", text_color='Green', font=("Arial",16),)
    From_search.grid(row=2, column=0, columnspan=1, pady=20, padx=10)
    From_theme = customtkinter.CTkComboBox(master=frame2, values = sorted([str(i) for i in rp_obj.final_data['Age'].unique()]),
                                    fg_color='Green',bg_color='Green',text_color='White')
    From_theme.grid(row=2,column=1,columnspan=1,padx=5,sticky='ew',)

    To_search= customtkinter.CTkLabel(master=frame2, text="Age To", text_color='Green', font=("Arial",16),)
    To_search.grid(row=2, column=2, columnspan=1, pady=20, padx=10)
    To_theme = customtkinter.CTkComboBox(master=frame2, values = sorted([str(i) for i in rp_obj.final_data['Age'].unique()]),
                                    fg_color='Green',bg_color='Green',text_color='White')
    To_theme.grid(row=2,column=3,columnspan=1,padx=5,sticky='ew',)
    search_button = customtkinter.CTkButton(master=frame2, text="Browse", command=BrowseAgeRange,
                                        bg_color='Green', fg_color='Green',)
    search_button.grid(row=2, column=4, pady=12, padx=10)
    popup_window.mainloop()



