# Subscription-Manager

For frequent subscription users who need to reduce expenses on unwanted subscriptions, this product is a subscription manager mobile app that record and visualize user’s subscription information to support their financial decision making.

<br>

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Get Started](#usage)
- [Get Help](#help)
- [Contributing](#contributing)
- [License](#license)

<br>

## Description

<br>

### Project Context

This Subscription Manager application was created as part of the course project for LIBR 559C: Python Programming at the School of Information, University of British Columbia. The project development was completed in 3 weeks in June, 2023. 

<br>

### Background & Objective
As online subscription gain popularity, consumers now face the risk of overspending due to inadequate management of recurring payments. In a survey conducted by [JPMorgan Chase & Co.] (https://media.chase.com/news/survey-from-chase-reveals), 71% the respondents reported wasting over $50 per month on unnecessary recurring payments, 60% had at least once forgotten about their subscriptions, and 55% were unaware of the total expenses they were being charged each month. 

Seeking a fresh start in life where subscriptions work for you, not against you, and where you can enjoy the benefits of subscriptions without the stress?

Our Subscription Manager app is designed for frequent subscription users who have a need of keeping track of subscriptions and cutting down unnecessary expenses. Our app is the go-to-tool for organizing, recording, and visualizing all subscription information in one place. The goal is to help users stay on top of their subscription spending and make more informed financial decisions

<br>

### Main Features

- Sign up, Log in
- Submit a subscription record
- Remove or edit a subscription record
- A table view presenting all active subscription details with the next billing date
- A line chart view displaying cumulative spending in the past 6 months

<br>

### Outcome

- Python application
- [Client-server architecture](https://www.figma.com/file/2eLzioNvs3th2WTc0WT56D/Architecture?type=whiteboard&node-id=0%3A1&t=BoYV9jU0Edu1hKtb-1)
- [User flow](https://www.figma.com/file/ZgQPsUzPS0XyNXnGRyYaxm/User-Flow?type=whiteboard&node-id=0%3A1&t=LCeWiM7UPTUEN5xy-1)


<br>
<br>


## Installation

Before starting the application, use the command below to install all of the Python modules and packages in the requirements.txt file.

```
pip install -r requirements.txt
```  

<br>

## Get Started


To start using this app, run this command in the `'/server'` file path to start the server on your local machine.
```
python main.py
``` 

After the server is running, open another terminal and run this command in the `'/gui'` path to open the application window.

``` 
python gui.py
``` 

<br>

### Welcome Screen
On the welcome screen, users are presented with two options: "Log in" and "Sign up". By clicking on the "Log in" button, users will be directed to the log in screen. By clicking on the "Sign up" button, users will be directed to the sign up screen where they can create a new account. 

<br>

### Sign up
When users access the sign up screen, they will be asked to input their name, email, and password to create an account. Once finished, navigate back to the welcome screen and click on the "Log in" button to continue.

<br>

### Log in
To log into the account, users will be asked to enter their registered email and password for user authentication. Once successful, users will be directed to homepage.

<br>

### Homepage
Upon reaching the homepage, users will be prompted to select and input the subscription service name, cost, subscription starting date (first billing date), and billing cycle (frequency). By clicking on the "Submit" button, users will be able to create a subscription record, which will capture and store the relevant information provided.

<br>

### Table View
After submitting the subscription records, users can easily navigate to the "Table View" page through the bottom navigation bar. Once on the "Table View" page, users will be able to see an overview of subscription details like subscription name, cost, starting date, billing cycle, and next billing date in tabular format. 

Under the tabular data, users are presented with two button options: "Remove subscription" and "Edit subscription". 

<br>

### Remove Subscription
On the remove subscription page, users can remove the subscription records they've entered. To remove a record, users can use the dropdown selection tool to select the specific subscription name they wish to remove from the list. After selecting the desired subscription, users can then proceed to click on the "Remove" button. 

To view the updated table view, users have to navigate back to the homepage and use the bottom nav tab to open a new "Table View" window.

<br>

### Edit Subscription
On the edit subscription page, users can edit the subscription details they've recorded earlier. To edit and update the information, users are asked to select and enter the updated information of the subscription in the form. By clicking on the "Edit" button, users will be able to edit the subscription info.

<br>

### Chart View
Through the bottom navigation bar, users can access a line chart depicting the cumulative spending over the past 6 month. 

<br>
<br>

## Get help

If you have any issue running this app or questions about how to contribute to this application, please start a discussion [here](https://github.com/Zijing-Liu/Subscription-Manager/discussions/4).

<br>
<br>
 

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. Bug reports and feature requests are also welcome through the GitHub Issues page.

Here is a list of potential features we aim to prioritize: 

- Push notifications to remind users before the next billing starts
- Allow users to add back a cancelled subscription
- User authentication and user session management
- Add more subscription service name to the company table, and implement free input for subscription name
- Use web scraping to get data from email data or credit bill while ensuring data encryption

<br>
<br>

## License

This project is licensed under the MIT License - see the LICENSE file for details.
