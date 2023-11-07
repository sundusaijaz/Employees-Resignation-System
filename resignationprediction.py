import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report
import random 
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
import sqlite3


class ResignationPrediction():
  def __init__(self):
    self.conn = sqlite3.connect('Employees.db') 
    self.cursor = self.conn.cursor()
  def UploadSheetToDB(self,filename):
    
    
    self.data = pd.read_excel(filename)
    for index,row in self.data.iterrows():
      self.cursor.execute("INSERT INTO resignations (Age, Department, Education, EducationField,EmployeeNumber,GENDER,JobLevel, JobRole, MaritalStatus, FECHA_DE_INGRESO, FECHA_DE_CESE, MonthlyIncome, Ovetime, EnvironmentSatisfaction, JobSatisfaction,PerformanceRating,WorkLifeBalance ) VALUES (?, ?, ?, ?,?,?,?, ?, ?, ?, ?, ?, ?, ?, ?,?,? );",\
                            (int(row['Age']),row['Department'],int(row['Education']),row['EducationField'],int(row['EmployeeNumber']), 
                            row['Gender'],int(row['JobLevel']),row['JobRole'],row['MaritalStatus'],row['FECHA_DE_INGRESO'],str(row['FECHA_DE_CESE']) ,float(row['MonthlyIncome']),row['Ovetime'],int(row['EnvironmentSatisfaction']),int(row['JobSatisfaction']),int(row['PerformanceRating']),int(row['WorkLifeBalance'])))
      
      self.conn.commit()
    print("[INFO] : All Data Added")
    
    self.cursor.close()
  def preprocess(self,filename=None):
    try:
      self.label_encoders = {}
      if filename == None:
        print(f"[INFO] : Reading FRROM DataBase")
        self.data = pd.read_sql_query("SELECT * from resignations",self.conn)
        self.data.drop(columns=['id'],inplace=True)
        self.data['FECHA_DE_CESE'] = pd.to_datetime(self.data['FECHA_DE_CESE'])
      else:
        print(f"[INFO] : Reading {filename}")
        self.data = pd.read_excel(filename)
      
      self.temp_data = self.data.copy()
      self.data['Ovetime'].fillna('No', inplace=True)
      self.data['Ovetime'] = self.data['Ovetime'].replace('Si', 'Yes')
      self.data['Ovetime'] = self.data['Ovetime'].replace(1000, 'No')
      
      
      #data separation
      self.data['Resigned'] = self.data['FECHA_DE_CESE'].apply(lambda x: 'Yes' if pd.notna(x) else 'No')
      self.data['Resigned'] = self.data['FECHA_DE_CESE'].apply(lambda x: 1 if pd.notna(x) else 0)
      print(self.data['Resigned'].unique())
      self.data.drop(['FECHA_DE_CESE'],inplace=True,axis=1)
      self.data = self.data[self.data['FECHA_DE_INGRESO'] != 'SOLTERO (A)']
      #self.data.drop('FECHA_DE_INGRESO',inplace=True,axis=1)
      #label encoding
      for column in self.data.columns:
        if self.data[column].dtype == 'object':
          self.label_encoders[column] = LabelEncoder()
          self.data[column] = self.label_encoders[column].fit_transform(self.data[column])
      self.preprocessed_data = self.data.copy()
      del(self.data)
      noise_prob = 0.08
      categories = self.preprocessed_data['Resigned'].unique()
      self.preprocessed_data['Resigned'] = self.preprocessed_data['Resigned'].apply(lambda x: random.choice(categories) if random.random() < noise_prob else x)
      X = self.preprocessed_data.drop('Resigned',axis=1)
      y = self.preprocessed_data['Resigned']
      print(y.unique())
      self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
      
    except Exception as e:
      print(e)
    


  
  def train(self):
    print("[INFO] : Training Started")
    self.rf_classifier = RandomForestClassifier(n_estimators=100, random_state=793,min_samples_split=5)
    self.rf_classifier.fit(self.X_train, self.y_train)
    print("[INFO] : Training Completed")



  def predict(self):
    y_pred = self.rf_classifier.predict(self.X_test)
    accuracy = accuracy_score(self.y_test, y_pred)
    print(f'Accuracy: {accuracy}')
    print(classification_report(self.y_test, y_pred))
    print("[INFO] : Saving Prediction Results -> results.xlsx")
    self.final_data = self.X_test.copy()
    self.final_data['Target_Resigned'] = self.y_test
    self.final_data['Predicted_Resigned'] = y_pred
    self.final_data = self.final_data.reset_index(drop=True)
    self.final_data['Predicted_Resigned']=self.final_data['Predicted_Resigned'].astype(str)
    self.final_data['Predicted_Resigned']=self.final_data['Predicted_Resigned'].str.replace("1",'Yes')
    self.final_data['Predicted_Resigned']=self.final_data['Predicted_Resigned'].str.replace("0",'No')
    for column in self.final_data.columns:
      if column in self.label_encoders:
        self.final_data[column] = self.label_encoders[column].inverse_transform(self.final_data[column])
    print(self.final_data.columns)
    #self.predictions.to_excel("results.xlsx")
    print("[INFO] : SAVED TO -> results.xlsx")


  def ClassificationReport(self):
    y_pred = self.rf_classifier.predict(self.X_test) 
    data = []
    report = classification_report(self.y_test, y_pred,output_dict=True)
    print(report)
    for class_name, metrics in report.items():
        if class_name not in ["accuracy", "macro avg", "weighted avg"]:
            row = [class_name, metrics["precision"], metrics["recall"], metrics["f1-score"], metrics["support"]]
            data.append(row)

    # Create a subplot for the table
    fig = make_subplots(rows=1, cols=1)
    header = ["Class", "Precision", "Recall", "F1-Score", "Support"]

    # Create a trace for the table
    trace = go.Table(
        header=dict(values=header, fill=dict(color="#C2D4FF"), align="left"),
        cells=dict(values=list(zip(*data)), fill=dict(color="#F5F8FF"), align="left")
    )

    # Add the table trace to the subplot
    fig.add_trace(trace)

    # Update layout options for the table
    table_layout = go.Layout(
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    fig.update_layout()

    # Show the table
    pyo.plot(fig)
    #pyo.iplot(fig, show_link=False)



