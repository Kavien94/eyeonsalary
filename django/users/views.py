from django.shortcuts import redirect, render
from django.contrib.auth import login
from eyeonsalary.settings import MEDIA_ROOT
from django.urls import reverse
from users.forms import CustomUserCreationForm

from plotly.offline import plot
from plotly.graph_objs import Scatter
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly

import numpy as np
import pandas as pd

# Create your views here.

def dashboard(request):
    query_search = request.POST.get('query')
    query_Positon= request.POST.get('query_pos')
    graph_option = request.POST.get('dropDownSelection')
    Sorting = request.POST.get('dropDownSorting')
 
    Filter_Data =""

    if query_search != None:
        query_search = query_search.lower()
    
    if query_Positon != None:
        query_Positon = query_Positon.lower()



    #Path of the data #
    file_path = MEDIA_ROOT+"/data.csv"
    df = pd.read_csv(file_path)
    #Path of the data
    data = ""
    layout = ""
    plot_div=""
    dataAv = 0 
    if Sorting == "1":
        Sorting = False 
    else:
        Sorting = True 

    #default graph
    if graph_option ==None :
        AvgStartingSal = df.groupby(['position'])['start_sal'].mean().sort_values(ascending=False)
        x_data = AvgStartingSal.index
        y_data = AvgStartingSal
        dataAv = len(AvgStartingSal)
        data = go.Bar(x = x_data, y= y_data, name="Avg", marker_color='#99edff')
        data=go.Data([data])
        layout=go.Layout(title="Average Starting Salary Offred", xaxis={'title':'Positions'}, 
        yaxis={'title':'Average Salary'},height= 1500, plot_bgcolor='rgb(255,255,255)')
    
    
    elif graph_option  == "1":
        if query_search != "" and query_Positon !="":

            AvgStartingSal = df[(df['state'].str.lower().str.contains(query_search)) & (df['position'].str.contains(query_Positon))].groupby(['position'])['start_sal'].mean().sort_values(ascending=Sorting)
            x_data = AvgStartingSal.index
            y_data = AvgStartingSal
            dataAv = len(AvgStartingSal)
            Filter_Data = " State: " + query_search.capitalize() + " Position: "+ query_Positon.capitalize()
        elif query_search != "":
            AvgStartingSal = df[df['state'].str.lower().str.contains( query_search)].groupby(['position'])['start_sal'].mean().sort_values(ascending=Sorting)
            x_data = AvgStartingSal.index
            y_data = AvgStartingSal
            dataAv = len(AvgStartingSal)
            Filter_Data = " State: " + query_search.capitalize()


        elif query_Positon !="":
            AvgStartingSal = df[df['position'].str.lower().str.contains(query_Positon)].groupby(['position'])['start_sal'].mean().sort_values(ascending=Sorting)
            x_data = AvgStartingSal.index
            y_data = AvgStartingSal
            dataAv = len(AvgStartingSal)
            Filter_Data = " Position: "+ query_Positon.capitalize()

        #No search value
        else:
            AvgStartingSal = df.groupby(['position'])['start_sal'].mean().sort_values(ascending=Sorting)
            x_data = AvgStartingSal.index
            y_data = AvgStartingSal   
            dataAv = len(AvgStartingSal)
            

        data = go.Bar(x = x_data, y= y_data, name="Avg", marker_color='#99edff')
        data=go.Data([data])
        layout=go.Layout(title="Average Starting Salary Offered " + Filter_Data, xaxis={'title':'Positions'}, 
        yaxis={'title':'Average Salary'},height= 1500, plot_bgcolor='rgb(255,255,255)')
            
        

    elif graph_option  == "2":
        if query_search != "" and query_Positon !="":
            avg_highest_Sallry_Offered = df[(df['state'].str.lower().str.contains(query_search)) & (df['position'].str.contains(query_Positon))].groupby(['position'])['end_sal'].mean().sort_values(ascending=Sorting)
            x_data = avg_highest_Sallry_Offered.index
            y_data = avg_highest_Sallry_Offered
            dataAv = len(avg_highest_Sallry_Offered)
            Filter_Data = " State: " + query_search.capitalize() + " Position: "+ query_Positon.capitalize()
        elif query_search != "":
            avg_highest_Sallry_Offered = df[df['state'].str.lower().str.contains( query_search)].groupby(['position'])['end_sal'].mean().sort_values(ascending=Sorting)
            x_data = avg_highest_Sallry_Offered.index
            y_data = avg_highest_Sallry_Offered
            dataAv = len(avg_highest_Sallry_Offered)
            Filter_Data = " State: " + query_search.capitalize()


        elif query_Positon != "":
            avg_highest_Sallry_Offered = df[df['position'].str.lower().str.contains( query_search)].groupby(['position'])['end_sal'].mean().sort_values(ascending=Sorting)
            x_data = avg_highest_Sallry_Offered.index
            y_data = avg_highest_Sallry_Offered
            dataAv = len(avg_highest_Sallry_Offered)
            Filter_Data = " Position: "+ query_Positon.capitalize()

        else:
            avg_highest_Sallry_Offered = df.groupby(['position'])['end_sal'].mean().sort_values(ascending=False)
            dataAv = len(avg_highest_Sallry_Offered)
            x_data = avg_highest_Sallry_Offered.index
            y_data = avg_highest_Sallry_Offered
            
        data = go.Bar(x = x_data, y= y_data, name="Highest Average", marker_color='#99edff')
        data=go.Data([data])
        layout=go.Layout(title="Average Highest Salary Offred", xaxis={'title':'Positions'}, 
        yaxis={'title':'Average Salary'}, height= 2050, plot_bgcolor='rgb(255,255,255)')
            
    elif graph_option == "3":
        if query_search != "" and query_Positon !="":

            MinStartingSal =   df[(df['state'].str.lower().str.contains(query_search)) & (df['position'].str.lower().str.contains(query_Positon))].groupby(['position'])['start_sal'].min().sort_values(ascending=Sorting)
            MaxStartingSal =   df[(df['state'].str.lower().str.contains(query_search)) & (df['position'].str.lower().str.contains(query_Positon))].groupby(['position'])['start_sal'].max().sort_values(ascending=Sorting)
            xMin_data = MinStartingSal.index
            yMIn_data = MinStartingSal

            xMax_data = MinStartingSal.index
            yMax_data = MaxStartingSal

            Filter_Data = " State: " + query_search.capitalize() + " Position: "+ query_Positon.capitalize()

            dataAv = len(MinStartingSal)
            data1 = go.Bar(x = xMin_data, y= yMIn_data, name="Min", marker_color='#99edff')
            data2 = go.Bar(x = xMax_data, y= yMax_data, name="Max")
            data=go.Data([data1,data2])
            

        elif query_search != "":
            MinStartingSal = df[df['state'].str.lower().str.contains( query_search)].groupby(['position'])['start_sal'].min().sort_values(ascending=Sorting)
            MaxStartingSal = df[df['state'].str.lower().str.contains( query_search)].groupby(['position'])['start_sal'].max().sort_values(ascending=Sorting)
           
            xMin_data = MinStartingSal.index
            yMIn_data = MinStartingSal

            xMax_data = MinStartingSal.index
            yMax_data = MaxStartingSal
            
            dataAv = len(MinStartingSal)

            data1 = go.Bar(x = xMin_data, y= yMIn_data, name="Min", marker_color='#99edff')
            data2 = go.Bar(x = xMax_data, y= yMax_data, name="Max")
            data=go.Data([data1,data2])
            Filter_Data = " State: " + query_search.capitalize()

        elif query_Positon !="":
            MinStartingSal = df[df['position'].str.lower().str.contains(query_Positon)].groupby(['position'])['start_sal'].min().sort_values(ascending=Sorting)
            MaxStartingSal = df[df['position'].str.lower().str.contains(query_Positon)].groupby(['position'])['start_sal'].max().sort_values(ascending=Sorting)
            xMin_data = MinStartingSal.index
            yMIn_data = MinStartingSal

            xMax_data = MinStartingSal.index
            yMax_data = MaxStartingSal

            dataAv = len(MinStartingSal)
            data1 = go.Bar(x = xMin_data, y= yMIn_data, name="Min", marker_color='#99edff')
            data2 = go.Bar(x = xMax_data, y= yMax_data, name="Max")
            data=go.Data([data1,data2])
            Filter_Data = " Position: " + query_Positon.capitalize()

        #No search value
        else:
            MinStartingSal = df.groupby(['position'])['start_sal'].min().sort_values(ascending=Sorting)
            MaxStartingSal = df.groupby(['position'])['start_sal'].max().sort_values(ascending=Sorting)
            
            xMin_data = MinStartingSal.index
            yMIn_data = MinStartingSal

            xMax_data = MinStartingSal.index
            yMax_data = MaxStartingSal

            dataAv = len(MinStartingSal)

            data1 = go.Scatter(x = xMin_data, y= yMIn_data, name="Min", marker_color='#99edff')
            data2 = go.Scatter(x = xMax_data, y= yMax_data, name="Max")
            data=go.Data([data1,data2])



        layout=go.Layout(title="Min VS Max Starting Salary Offered " + Filter_Data, xaxis={'title':'Positions'}, 
        yaxis={'title':'Salary'},height= 1500, plot_bgcolor='rgb(255,255,255)')
            

    elif graph_option == "4":
        if query_search != "" and query_Positon !="":

            MinStartingSal =   df[(df['state'].str.lower().str.contains(query_search)) & (df['position'].str.lower().contains(query_Positon))].groupby(['position'])['end_sal'].min().sort_values(ascending=Sorting)
            MaxStartingSal =   df[(df['state'].str.lower().str.contains(query_search)) & (df['position'].str.lower().contains(query_Positon))].groupby(['position'])['end_sal'].max().sort_values(ascending=Sorting)
            xMin_data = MinStartingSal.index
            yMIn_data = MinStartingSal

            xMax_data = MinStartingSal.index
            yMax_data = MaxStartingSal

            dataAv = len(MinStartingSal)
            data1 = go.Bar(x = xMin_data, y= yMIn_data, name="Min", marker_color='#99edff')
            data2 = go.Bar(x = xMax_data, y= yMax_data, name="Max")
            data=go.Data([data1,data2])
            Filter_Data = " State: " + query_search.capitalize() + " Position: "+ query_Positon.capitalize()


        elif query_search != "":
            MinStartingSal = df[df['state'].str.lower().str.contains( query_search)].groupby(['position'])['end_sal'].min().sort_values(ascending=Sorting)
            MaxStartingSal = df[df['state'].str.lower().str.contains( query_search)].groupby(['position'])['end_sal'].max().sort_values(ascending=Sorting)
           
            xMin_data = MinStartingSal.index
            yMIn_data = MinStartingSal

            xMax_data = MinStartingSal.index
            yMax_data = MaxStartingSal
            
            dataAv = len(MinStartingSal)

            data1 = go.Bar(x = xMin_data, y= yMIn_data, name="Min", marker_color='#99edff')
            data2 = go.Bar(x = xMax_data, y= yMax_data, name="Max")
            data=go.Data([data1,data2])
            Filter_Data = " State: " + query_search.capitalize()

        elif query_Positon !="":
            MinStartingSal = df[df['position'].str.lower().str.contains(query_Positon)].groupby(['position'])['end_sal'].min().sort_values(ascending=Sorting)
            MaxStartingSal =df[df['position'].str.lower().str.contains(query_Positon)].groupby(['position'])['end_sal'].max().sort_values(ascending=Sorting)
            xMin_data = MinStartingSal.index
            yMIn_data = MinStartingSal

            xMax_data = MinStartingSal.index
            yMax_data = MaxStartingSal

            dataAv = len(MinStartingSal)
            data1 = go.Bar(x = xMin_data, y= yMIn_data, name="Min", marker_color='#99edff')
            data2 = go.Bar(x = xMax_data, y= yMax_data, name="Max")
            data=go.Data([data1,data2])
            Filter_Data = " Position: " + query_Positon.capitalize()

        #No search value
        else:
            MinStartingSal = df.groupby(['position'])['end_sal'].min().sort_values(ascending=Sorting)
            MaxStartingSal = df.groupby(['position'])['end_sal'].max().sort_values(ascending=Sorting)
            
            xMin_data = MinStartingSal.index
            yMIn_data = MinStartingSal

            xMax_data = MinStartingSal.index
            yMax_data = MaxStartingSal

            dataAv = len(MinStartingSal)

            data1 = go.Scatter(x = xMin_data, y= yMIn_data, name="Min", marker_color='#99edff')
            data2 = go.Scatter(x = xMax_data, y= yMax_data, name="Max")
            data=go.Data([data1,data2])



        layout=go.Layout(title="Min VS Max Highest Salary Offered " + Filter_Data, xaxis={'title':'Positions'}, 
        yaxis={'title':'Salary'},height= 1500, plot_bgcolor='rgb(255,255,255)')
            




    #If got data only show if no wont show
    if dataAv > 1:
        figure=go.Figure(data=data,layout=layout)
        plot_div = plot(figure,output_type='div')
    else:
        plot_div = "No data found "
    
    return render(request, "users/dashboard.html", context={'plot_div': plot_div})
  
def register(request):

    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )

    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))