"""
Calculates Matilda's revenues from Cupcakes selling.
""" 
#Imports
import glob
import os
import codecs
import re
import pandas as pd
import datetime
import numpy as np
import calendar
import matplotlib.pyplot as plt

# Constant variables
Current_Date = datetime.datetime.today()

def get_input_folder(path):
    """
    Get the filenamesof the folder provided by the user.
    """
    # Creating an empty Dataframe 
    df = pd.DataFrame()

    #Feed the Dataframe from files
    files = glob.glob(path + "/*.txt")
    for file in files:
        if os.access(file, os.R_OK):

            base = os.path.basename(file)[:-4]
            items = []
            lines = [line.rstrip("\n") for line in codecs.open(file,"r","utf-8")]

            for line in lines:
                items.append(line)

            df[base] = items
            
    #No need the first line
    df = df.drop([0]).reset_index(drop=True)
    df = df.apply(pd.to_numeric)

    #The latest data first
    sort_ascending = df.sort_index(ascending=False)
    idx = sort_ascending.index
    sort_ascending['days_ago'] = idx
    
    #Create datetime column, based on today's date
    sort_ascending['datetime'] =  np.vectorize(calculate_date)(sort_ascending['days_ago'])

    #My problem here is that to_datetime silently failed so the dtype remained as str/object, 
    # if set param errors='coerce' then if the conversion fails for any particular string then those rows are set to NaT.
    sort_ascending['datetime'] = pd.to_datetime(sort_ascending['datetime'], errors='coerce')

    #Split date in Year and Month
    sort_ascending['Year'] = sort_ascending['datetime'].dt.strftime('%Y')
    sort_ascending['Month'] = sort_ascending['datetime'].dt.strftime('%m')

    year = sort_ascending['datetime'].dt.strftime('%Y')
    month =sort_ascending['datetime'].dt.strftime('%m')
    day = sort_ascending['datetime'].dt.strftime('%d')

    sort_ascending['WorkWeek'] =  np.vectorize(calculate_week)(year,month,day)

    print(sort_ascending)

    #Save the date in a  csv file
    sort_ascending.to_csv('Cupcakes.csv',index=False)

    #yearly_revenue = sort_ascending.groupby(sort_ascending.datetime.dt.strftime('%Y')).Total.sum()
    yearly_revenue = sort_ascending.groupby(['Year'])

    #Revenue per year

    for name_of_the_group, group in yearly_revenue:
        print("Revenue of " + name_of_the_group)
        yearly_total_revenue = group['Total'].sum()
        print("${:,}".format(yearly_total_revenue))
    
    # plot data
    data = sort_ascending.groupby(['Year']).sum()['Total']

    plotme = data.rename(columns={'Year': 'Total'})
    ax = plotme.plot.bar(rot=0, subplots=True)
    #fig, ax = plt.subplots()

    plt.xticks(rotation=45, ha='right')
    plt.title("Revenue per Year")
    plt.xlabel("Year")
    plt.ylabel("Revenue in $")

    plt.show()

    #Revenue per month
    monthly_revenue = sort_ascending.groupby(['Year','Month'])
    print("Revenue per Month and Year")
    previous = ""
    for name_of_the_group, group in monthly_revenue:
        month_name = calendar.month_name[int(name_of_the_group[1])]
        year_number = name_of_the_group[0]

        if previous != year_number:
            print(year_number)  

        print("\t" + month_name)
        print("\t\t${:,}".format(group['Total'].sum()))

        previous = year_number

    # plot data
    data = sort_ascending.groupby(['Year','Month']).sum()['Total']

    plotme = data.rename(columns={'Month-Year': 'Total'})
    ax = plotme.plot.bar(rot=0, subplots=True)
    #fig, ax = plt.subplots()

    plt.xticks(rotation=45, ha='right')
    plt.title("Revenue per Month")
    plt.xlabel("Month - Year")
    plt.ylabel("Revenue in $")

    plt.show()

    #Revenue per work week
    weekly_revenue = sort_ascending.groupby(['Year','WorkWeek'])
    print("Revenue per WorkWeek and Year")
    previous = ""
    for name_of_the_group, group in weekly_revenue:
        week_name = name_of_the_group[1]
        year_number = name_of_the_group[0]

        if previous != year_number:
            print(year_number)  

        print("\t" + week_name)
        print("\t\t${:,}".format(group['Total'].sum()))

        previous = year_number

    # plot data
    data = sort_ascending.groupby(['Year','WorkWeek']).sum()['Total']

    plotme = data.rename(columns={'Year-WorkWeek': 'Total'})
    ax = plotme.plot.bar(rot=0, subplots=True)
    #fig, ax = plt.subplots()

    plt.xticks(rotation=45, ha='right')
    plt.title("Revenue per Month")
    plt.xlabel("Month - Year")
    plt.ylabel("Revenue in $")

    plt.show()

def calculate_date(index):
    """Calculate the date based on the index, to define
    previous days
    """
    date = datetime.datetime.today() - pd.Timedelta(days=index)
    return date.strftime('%Y-%m-%d')

def calculate_week(year,month,day):
    """Calculate the week of the year based on date
    """
    workweek = datetime.date(int(year), int(month), int(day)).strftime("%V")
    return workweek
def main():
    """
    Application entry point function
    """
    path = input("Please copy and paste the path of the files: ")
    get_input_folder(path)

if __name__== "__main__":
    main()

print("--Matilda Cupcakes--")