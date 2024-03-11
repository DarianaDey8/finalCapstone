# finalCapstone
# Task Management System
This repository contains a simple task management system for small business implemented using Python.                      The task management system provides a user-friendly graphical user interface for managing tasks for a small team , including login for users, registering a new user, adding a new task,  viewing existing tasks, marking tasks as completed or editing them, and producing the reports.

# Features
- Login for users:
     1. for registered users it offers an option to register a user and to view the tasks;
     2. for admin it allows to add a user, to add a task, to view tasks, to generate and view to reports
- Add New User: Easily add new user to the system using a dialog window, system prevents double registration of the user
- Add New Task: Easily add new tasks to the system using a diaalog window, choose an option to assign a task to any other registered user or yourself
- View Tasks: View the list of tasks with status Completed / In progress
- View my tasks: View the list of your own tasks.
- Generate report: View the report on tasks , including completed and overdue
- View statistics : View the report for each user

# Getting started
To run the task management system locally,follow these steps:
1. Clone the repository:
   ```
    git clone https://github.com/DarianaDey8/finalCapstone.git
   ```
3. Navigate to the project directory:
   ```
   cd finalCapstone
   ```
4. Install the required dependencies.Ensure that you have Python installed.
   ```
   pip install pyqt5
   ```
5. Run the application:
   ```
   python finalCapstone.py
   ```
# Usage
Upon launching the application, a main window will appear, providing access to variuos functionalities:
- Login instructions :
  1. enter 'admin' to enter the full functionality
  2. enter a registered user name to enter the limited menu 
- Choose "r" to register the user
- Choose "a" to add the task
- Choose "va" to view the list of tasks
- Choose "vm" to view your own tasks
- Choose "gr" to generate reports
- Choose "gs" to generate statistics
  
Please note that users will be registered in users.txt file, tasks will be added to tasks.txt file.
Reports will be generated in separate files: usersoverview.txt and tasksoverview.txt

# Contributing
Contributions to the task management system are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

