from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

def createLineChart(subscription_data):
    # prepare a dictionary to use key to calculalate the amount of payment by month/year
    pay_payday = {} 
    for start_date, cycle, end_date, amount in subscription_data:
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
    
    # #now visualize the payment


    #create a month list for x axis
    months_x=[]
    #add last one year to the list
    today = datetime.now() #class datetime.datetime
    first_x = today-relativedelta(months=5) #class datetime.datetime
    month_x = first_x
    while month_x <= today:
        month_str = month_x.strftime('%-m/%y')
        months_x.append(month_str)
        month_x = month_x+relativedelta(months=1)

    #define x, y
    plot_data = {
        'x': months_x,
        'y': [round(pay_payday.get(month_year, 0), 2) for month_year in months_x] 
    }