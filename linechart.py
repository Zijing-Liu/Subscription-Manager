#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 01:58:54 2023

@author: zkr
"""

import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Get the start date, cycle, end_date, and amount from the database
cursor.execute('SELECT start_date, subscription_cycle, end_date, amount FROM Subscription WHERE user_id = 1')
subscription_data = cursor.fetchall()  # This is a list of tuples

#prepare a dictionary to use key to calculalate the amount of payment by month/year
pay_payday = {} 


for start_date, cycle, end_date, amount in subscription_data:
    
    #turn start_date as a string to a date
    start_DATE = datetime.strptime(start_date, '%Y-%m-%d') #keep day here for weekly calculation
    #if subscription already cancled and there is an end_date
    if end_date:
        end_DATE = datetime.strptime(end_date, '%Y-%m-%d') 
    #if subscription is still going on and no end_date, take today as the end date
    else:
        end_DATE = datetime.now()
        
    #calculate based on different types of cycle

    if cycle == 'weekly':
        while end_DATE and start_DATE <= end_DATE:#use while loop to add amount each time a subscription start its new cycle
            month_year = start_DATE.strftime('%Y-%m')  # extract the month and year for dictionary key
            pay_payday[month_year] = pay_payday.get(month_year, 0) + amount #counting with get()
            start_DATE = start_DATE + timedelta(weeks=1)
    if cycle == 'monthly':
        while end_DATE and start_DATE <= end_DATE:
            month_year = start_DATE.strftime('%Y-%m')  
            pay_payday[month_year] = pay_payday.get(month_year, 0) + amount
            start_DATE = start_DATE + relativedelta(months=1)
    if cycle == '3-months':
        while end_DATE and start_DATE <= end_DATE:
            month_year = start_DATE.strftime('%Y-%m')  
            pay_payday[month_year] = pay_payday.get(month_year, 0) + amount
            start_DATE = start_DATE + relativedelta(months=3)
    if cycle == '6-months':
        while end_DATE and start_DATE <= end_DATE:
            month_year = start_DATE.strftime('%Y-%m')  
            pay_payday[month_year] = pay_payday.get(month_year, 0) + amount
            start_DATE = start_DATE + relativedelta(months=6)
    if cycle == 'annually':
        while end_DATE and start_DATE <= end_DATE:
            month_year = start_DATE.strftime('%Y-%m')  
            pay_payday[month_year] = pay_payday.get(month_year, 0) + amount
            start_DATE = start_DATE + relativedelta(years=1)
    
# Extract data for x axis and y axis
x_monthyear = sorted(pay_payday.keys())  # Sort x attributes by the month_year keys
y_amount = [pay_payday[month] for month in x_monthyear]


# Create the line chart

plt.plot(x_monthyear, y_amount, marker='s')
plt.xlabel('Month-Year')
plt.ylabel('Total Amount')
plt.title('Subscription Payments Over Time (Cash-based Accounting)')
plt.xticks(rotation=90)


# Adding value annotations to each point
for i, j in zip(x_monthyear, y_amount):
    plt.annotate(str(j), xy=(i, j), xytext=(0, -15),
                 textcoords='offset points', ha='center')

plt.show()


