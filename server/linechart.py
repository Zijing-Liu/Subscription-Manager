#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 11:04:42 2023

@author: zkr
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 01:58:54 2023

@author: zkr
"""

import sqlite3
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
    print(start_date)
    #turn string to a date for while loop comparision
    start_DATE = datetime.strptime(start_date, '%m/%d/%y') #keep day here for weekly calculation
    #if subscription already cancled and there is an end_date
    if end_date:
        end_DATE = datetime.strptime(end_date, '%m/%d/%y') 
    #if subscription is still going on and no end_date, take today as the end date
    else:
        end_DATE = datetime.now()
        
    #calculate based on different types of cycle

    if cycle == 'weekly':
        while end_DATE and start_DATE <= end_DATE:#use while loop to add amount each time a subscription start its new cycle
            month_year = start_DATE.strftime('%-m/%y')  # extract the month and year for dictionary key
            pay_payday[month_year] = pay_payday.get(month_year, 0) + amount #counting with get()
            start_DATE = start_DATE + timedelta(weeks=1)
    if cycle == 'monthly':
        while end_DATE and start_DATE <= end_DATE:
            month_year = start_DATE.strftime('%-m/%y')  
            pay_payday[month_year] = pay_payday.get(month_year, 0) + amount
            start_DATE = start_DATE + relativedelta(months=1)
    if cycle == '3-months':
        while end_DATE and start_DATE <= end_DATE:
            month_year = start_DATE.strftime('%-m/%y')  
            pay_payday[month_year] = pay_payday.get(month_year, 0) + amount
            start_DATE = start_DATE + relativedelta(months=3)
    if cycle == '6-months':
        while end_DATE and start_DATE <= end_DATE:
            month_year = start_DATE.strftime('%-m/%y')  
            pay_payday[month_year] = pay_payday.get(month_year, 0) + amount
            start_DATE = start_DATE + relativedelta(months=6)
    if cycle == 'annually':
        while end_DATE and start_DATE <= end_DATE:
            month_year = start_DATE.strftime('%-m/%y')  
            pay_payday[month_year] = pay_payday.get(month_year, 0) + amount
            start_DATE = start_DATE + relativedelta(years=1)
  
#now visualize the payment

import matplotlib.pyplot as plt

#create a month list for x axis
months_x=[]
#add last one year to the list
today = datetime.now() #class datetime.datetime
first_x=today-relativedelta(months=11) #class datetime.datetime
month_x=first_x
while month_x <= today:
    month_str=month_x.strftime('%-m/%y')
    months_x.append(month_str)
    month_x=month_x+relativedelta(months=1)

#set the x, y

x=months_x
y = [pay_payday.get(month_year, 0) for month_year in x]#if a month has no pay show 0

plt.plot(x, y, marker='s')
plt.xlabel('Month-Year')
plt.ylabel('Total Spending')
plt.title('Subscription Payments within Last One Year (Cash-based Accounting)')
plt.xticks(rotation=90)


# Adding value annotations to each point
for i, j in zip(x, y):
    plt.annotate(str(j), xy=(i, j), xytext=(0, -15),
                 textcoords='offset points', ha='center')

plt.show()

        
        




  



