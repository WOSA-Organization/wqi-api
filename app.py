from flask import Flask, render_template, redirect, url_for, Response, request, session
import pandas as pd
import plotly.graph_objects as go
import requests
import json
import plotly
import plotly.express as px


app = Flask(__name__,template_folder='templates')

def water_graph(city):
    dp = pd.read_csv('water.csv',encoding= 'unicode_escape')
    dp2 = dp[dp['District Name']==city].reset_index()
    la = []
    la = dp2['Quality Parameter'].unique()
    val = dp2['Quality Parameter'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=la, values=val, hole=.3)])
    #fig.show()
    plot_w = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_w



df = pd.read_csv('water.csv',encoding= 'unicode_escape')

#Encoding The IteM Type Column
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
encoded_state = le.fit_transform(df['State Name'])
df['encoded_state'] = encoded_state

encoded_city = le.fit_transform(df['District Name'])
df['encoded_city'] = encoded_city

encoded_quality = le.fit_transform(df['Quality Parameter'])
df['encoded_quality'] = encoded_quality

feature_columns=['encoded_state', 'encoded_city']
x = df[feature_columns].values
y = df['encoded_quality'].values

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 3)

from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(x_train, y_train)

df2 = df.groupby('State Name').agg('first').reset_index()
df2 = df2.drop(['District Name','encoded_city','encoded_quality','Block Name','Quality Parameter','Panchayat Name', 'Village Name', 'Habitation Name', 'Year'], axis = 1)

df3 = df.groupby('District Name').agg('first').reset_index()
df3.drop(['State Name','encoded_state','encoded_quality','Block Name','Quality Parameter','Panchayat Name', 'Village Name', 'Habitation Name', 'Year'], axis = 1)

def predict(inp):
    state, city = inp
    st  = df2[df2['State Name'] == state].index[0]
    ct  = df3[df3['District Name'] == city].index[0]
    x_new=[[st,ct]]
    pred_new = classifier.predict(x_new)  
    return pred_new

def High_val(state, city):
    df = pd.read_csv('water.csv',encoding= 'unicode_escape')
    df2 = df[df['State Name'] == state]
    df2 = df2[df2['District Name'] == city]
    return df2["Quality Parameter"].value_counts().idxmax()

# ROUTES
@app.route('/')
def home():
    return render_template('main_w.html')

@app.route("/success", methods=["GET", "POST"])
def water():
    state = request.form['state']
    state = state.upper()
    city = request.form['city']
    city = city.upper()
    chem = High_val(state,city)
    plot_w = water_graph(city)
    return render_template("success_w.html", p_text='The Dominant Chemical in the Water of your Area is  {}'.format(chem), graphJSON=plot_w)    
 
if __name__ == "__main__":
    app.run(debug=True)
