# Budget App
In this directory is a simple Budget App, which is created in Django Framework. For the frontend is used Bootstrap 4. The app is multilanguage, current languages are Czech and English.
The main purpose of this app is to track user expenses and incomes. Users can also change the currency of their transactions, but there is no currency converter, so if the currency is changed the amount of transactions remains in the old currency.

To use this app you have to set up an email client and install all required packages. Unit tests and selenium tests are also included.

## Home page
On the home page of the app is a basic description and links to Sign In or Sign Up. Users can also switch languages by clicking on the country flag. If the user switch language then he login or create an account in the selected language.
![Home](https://github.com/skapis/appscreenshots/blob/main/Budget%20App/Home.png)

## Dashboard
The main page of the app is the dashboard, where users can see their balance, the sum of monthly incomes and expenses and the count of transactions in a month. Users can also see incomes or expenses by category in the doughnut chart and the sum of incomes and expenses in the bar chart. At the bottom is the table of all transactions in the month. Users can also select a month to see.
![Dashboard](https://github.com/skapis/appscreenshots/blob/main/Budget%20App/Dashboard.png)

In the navbar, user can change the language of the app from Czech to English and vice versa.
![Dashboard CS](https://github.com/skapis/appscreenshots/blob/main/Budget%20App/Dashboard_cs.png)

## Transactions
On this page, users can see all their transactions in the selected month. The default is the current month.
![Transactions](https://github.com/skapis/appscreenshots/blob/main/Budget%20App/Transactions.png)

## Account
In account detail, users can see their account data and change the currency of their transactions.
![Account](https://github.com/skapis/appscreenshots/blob/main/Budget%20App/Transactions.png)
