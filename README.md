# FTEC3002Project_Eduvestment
Code for FTEC3002 Final Project
![Image of Infrastracture](https://github.com/XUXiangCUHK/FTEC3002Project_Eduvestment/blob/main/3002ProjectDemo/images/Infrastructure.png)

Technical Feasibility

# Web Application Construction
The front-end web application is constructed with JavaScript, including all the four functionalities. In our demonstration, we use the python package Streamlit to construct the webpage for convenience.
# Login Methods
Lots of corporations such as Facebook, Google, provide services for developers to make it available to log in their own software with these existing accounts of users.
Take Facebook as an example. A developer is supposed to register for an account, register and configure the softwares and download Facebook SDK (Software Developing Kit) to enable the application to call Facebook login APIs. Then one can log in with his/her Facebook account to the application.
# Database Construction
AWS (Amazon Web Services) provides database services – Amazon Relational Database Service (Amazon RDS), which allow developers to construct relational databases on the cloud. Once a developer opens an account, he/she can create a DB instance and customize his/her own database configurations to fulfill different requirements.
Eduvestment uses MySQL to query the database to post and get information.
# Data Communication and APIs
The main functionalities of Eduvestment require connection to banking databases. In this case, APIs provided by banks or banking companies will be called to fulfill users’ commands. For example, in order to transfer money, Eduvestment will call the transfer API to gain connection to the banking database and the database will send back responses of the request.
In the demonstration, Eduvestment is connected through APIs to the Simnectz database as Simnectz provides the majority of banking services and it is convenient and easy to implement for simple functionality demonstration.
