# simple task manager program for small business
import datetime
import os

# To register a user
def reg_user(username):
    with open('user.txt', 'r') as f:
        users = [line.split(', ')[0] for line in f.read().splitlines()]
    if username in users:
        print(" The user with this name already exists. Please, choose another name")
        return False
    with open('user.txt', 'a') as f:
        f.write(f"{username}\n")

    users.append(username)  # To add new user to the file user.txt
    print("The user was registered successfully")
    return True

# To add new task 
def add_task(username, title, description):
    # Assignment of the status "In progress" for every added task
    status = 'In progress'

    while True:
        due_date = input("Enter the deadline for the task (e.g.YYYY-MM-DD):  ")
        try:
            datetime.datetime.strptime(due_date, '%Y-%m-%d')
            break
        except ValueError:
            print("Incorrect date format. Please use the format YYYY-MM-DD")

    # To assign task to yourself or other user
    assign_choice = input("Who will be in charge? (s - yourself, other - other user): ").lower()

    if assign_choice == 's':
        assigned_user = username
    else:
        with open('user.txt', 'r') as f:
            users = [line.split(', ')[0] for line in f.read().splitlines()]

        print("List of registered users: ")
        for user in users:
            print(user)

        while True:
            assigned_user = input("Please enter the full name of the user to assign the task: ")
            if assigned_user in users and assigned_user != username:
                break
            else:
                print("This user name does not exist. Try again.")

    with open('tasks.txt', 'a') as f:
        f.write(f"{assigned_user}, {title}, {description}, {due_date}, {status}\n")

    print("Task was added successfully")

# To view all tasks
def view_all():
    with open('tasks.txt', 'r') as f:
        tasks = f.read().splitlines()

    if not tasks:
        print("There are no tasks to display")
        return

    print("All tasks: ")
    for i, task in enumerate(tasks, start=1):
        task_data = task.split(', ')
        if len(task_data) == 5:
            _, title, _, _, status = task_data
            is_completed = status.strip() == 'Completed' 
            print(f"{i}. {title} - {'Completed' if is_completed else 'In progress'}")
        else:
            print(f"{i}. Not correct format in the task file: {task}")

# To view own tasks
def view_mine(current_user):
    with open('tasks.txt', 'r') as f:
        tasks = f.read().splitlines()

    user_tasks = [task for task in tasks if task.split(', ')[0] == current_user]

    if not user_tasks:
        print("There are no tasks to display")
        return

    for i, task in enumerate(user_tasks):
        _, title, _, _, status = task.split(', ')
        print(f"{i + 1}. {title} - Status: {status}")

    return user_tasks

# To mark a task as completed
def mark_complete(task_index, tasks):
    task = tasks[task_index]
    _, title, description, due_date, status = task.split(', ')
    if status.strip() != 'Completed':
        tasks[task_index] = f"{current_user}, {title}, {description}, {due_date}, Completed"
        print("Task was registered as completed")
        with open('tasks.txt', 'w') as f:
            for task_line in tasks:
                f.write(task_line + '\n')
    else:
        print("The task was already marked as completed")

# To edit task
def edit_task(task_index, tasks, current_user):
    task = tasks[task_index]
    _, title, description, due_date, status = task.split(', ')

    print(f"Task to edit: {title}")
    print(f"Description: {description}")
    print(f"Due_date: {due_date}")
    print(f"Status: {status}")

    if status == 'Completed':
        print("The task is not available for edit.")
        return

    action = input(
        "Choose to edit (u — for user in charge, d — for due date, m — for return to menu): ").lower()

    if action == 'u':
        # Change of the user in charge
        with open('user.txt', 'r') as f:
            users = [line.split(', ')[0] for line in f.read().splitlines()]

        print("List of registered users: ")
        print(", ".join(users))

        while True:
            assigned_user = input("Enter the full name of the new user in charge: ")
            if assigned_user in users and assigned_user != current_user:
                break
            else:
                print("User full name is incorrect. Please try again.")

        tasks[task_index] = f"{assigned_user}, {title}, {description}, {due_date}, {status}\n"
        print("User in charge was changed successfully.")

        # To save the changed data in the file tasks.txt
        with open('tasks.txt', 'w') as f:
            for task_line in tasks:
                f.write(task_line + '\n')

    # To change a deadline for the task
    elif action == 'd':
        new_due_date = input("Enter the new deadline (YYYY-MM-DD): ")
        try:
            datetime.datetime.strptime(new_due_date, '%Y-%m-%d')
            tasks[task_index] = f"{current_user}, {title}, {description}, {new_due_date}, {status}\n"
            print("The deadline was changed successfully")

            # To save the changed data in the file tasks.txt
            with open('tasks.txt', 'w') as f:
                for task_line in tasks:
                    f.write(task_line + '\n')

        except ValueError:
            print("Not correct format. Please use YYYY-MM-DD.")

    elif action == 'm':
        print("Return to menu")

    else:
        print("Not correct choice.Please try again.")

# To generate reports
def generate_reports():
    tasks_filename = 'tasks.txt'
    users_filename = 'user.txt'
    task_overview_filename = 'task_overview.txt'
    user_overview_filename = 'user_overview.txt'

    if not os.path.exists(tasks_filename) or not os.path.exists(users_filename):
        print("Before generating reports please register users and add tasks.")
        return

    with open(tasks_filename, 'r') as f:
        tasks = f.read().splitlines()

    with open(users_filename, 'r') as f:
        users = f.read().splitlines()

    # To calculate team tasks
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.endswith(', Completed'))
    incomplete_tasks = sum(1 for task in tasks if task.endswith(', In progress'))
    overdue_tasks = sum(1 for task in tasks if
                        len(task.split(', ')) == 5 and not task.endswith(', Completed') and datetime.datetime.strptime(
                            task.split(', ')[3], '%Y-%m-%d').date() < datetime.date.today())

    with open(task_overview_filename, 'w') as f:
        f.write(f"Total tasks: {total_tasks}\n")
        f.write(f"Completed tasks: {completed_tasks}\n")
        f.write(f"Tasks in progress: {incomplete_tasks}\n")
        f.write(f"Overdue tasks: {overdue_tasks}\n")

        # To calculate tasks in percentage 
        if total_tasks > 0:
            f.write(f"Completed tasks: {(completed_tasks / total_tasks) * 100:.2f}%\n")
            f.write(f"Tasks in progress: {(incomplete_tasks / total_tasks) * 100:.2f}%\n")
            f.write(f"Overdue tasks: {(overdue_tasks / total_tasks) * 100:.2f}%\n")
        else:
            f.write("Completed tasks: 0.00%\n")
            f.write("Tasks in progress: 0.00%\n")
            f.write("Overdue tasks: 0.00%\n")

    with open(user_overview_filename, 'w') as f:
        f.write(f"Total registered users: {len(users)}\n")

        for user in users:
            user_tasks = [task for task in tasks if task.split(', ')[0] == user]
            total_user_tasks = len(user_tasks)

            if total_user_tasks == 0:
                f.write(f"\n{user}: Total user tasks: {total_user_tasks}\n")
                continue

            # To calculate each user tasks
            completed_user_tasks = sum(1 for task in user_tasks if task.endswith(', Completed'))
            incomplete_user_tasks = total_user_tasks - completed_user_tasks
            overdue_user_tasks = sum(1 for task in user_tasks if
                                     task.endswith(', In progress') and datetime.datetime.strptime(task.split(', ')[3],
                                                                                                   '%Y-%m-%d').date() < datetime.date.today())
            # To display user tasks
            f.write(f"\n{user}:\n")
            f.write(f"Total: {total_user_tasks}\n")
            f.write(f"Out of total team tasks: {(total_user_tasks / total_tasks) * 100:.2f}%\n")
            f.write(f"Completed: {(completed_user_tasks / total_user_tasks) * 100:.2f}%\n")
            if incomplete_user_tasks > 0:
                f.write(
                    f"In progress: {(incomplete_user_tasks / total_user_tasks) * 100:.2f}%\n")
                if overdue_user_tasks > 0:
                    f.write(f"Overdue: {(overdue_user_tasks / incomplete_user_tasks) * 100:.2f}%\n")
                else:
                    f.write("No overdue tasks\n")
            else:
                f.write("No tasks in progress\n")

# To display statistics
def display_statistics():
    tasks_filename = 'tasks.txt'
    users_filename = 'user.txt'

    if not os.path.exists(tasks_filename) or not os.path.exists(users_filename):
        print("Please, add tasks and users to display statistics.")
        return

    with open(tasks_filename, 'r') as f:
        tasks = f.read().splitlines()

    with open(users_filename, 'r') as f:
        users = f.read().splitlines()

    total_tasks = len(tasks)

    if total_tasks == 0:
        print("There is no available statistics.")
        return

    for user in users:
        user_tasks = [task for task in tasks if task.split(', ')[0] == user]
        total_user_tasks = len(user_tasks)

        if total_user_tasks == 0:
            print(f"\n{user}:There are no tasks to display statistics")
            continue

        completed_user_tasks = sum(1 for task in user_tasks if task.endswith(', Completed'))
        incomplete_user_tasks = total_user_tasks - completed_user_tasks

        if incomplete_user_tasks == 0:
            incomplete_percentage = 0
        else:
            incomplete_percentage = (incomplete_user_tasks / total_user_tasks) * 100

        overdue_user_tasks = sum(1 for task in user_tasks if
                                 task.endswith(', In Progress') and datetime.datetime.strptime(task.split(', ')[3],
                                                                                               '%Y-%m-%d').date() < datetime.date.today())

        if overdue_user_tasks == 0:
            overdue_percentage = 0
        else:
            overdue_percentage = (overdue_user_tasks / incomplete_user_tasks) * 100

        # To display statistics
        print(f"\n{user}:\n")
        print(f"Total: {total_user_tasks}")
        print(f"Out of total team tasks: {(total_user_tasks / total_tasks) * 100:.2f}%")
        print(f"Completed: {(completed_user_tasks / total_user_tasks) * 100:.2f}%")
        print(f"In progress: {incomplete_percentage:.2f}%")
        print(f"Overdue: {overdue_percentage:.2f}%")

    print("\nTeam statistics:\n")
    overdue_tasks = sum(1 for task in tasks if task.endswith(', Overdue'))

    in_progress_tasks = sum(1 for task in tasks if task.endswith(', In Progress'))
    completed_tasks = sum(1 for task in tasks if task.endswith(', Completed'))

    print(f"Total tasks: {total_tasks}")
    print(f"Overdue: {overdue_tasks}")
    print(f"In progress: {in_progress_tasks}")
    print(f"Completed: {completed_tasks}")

# To display the menu for admin
current_user = 'admin'
while True:
    if current_user:
        menu = input('''Please select one out of the options below:
        r -  Register user
        a -  Add task
        va - Review all tasks
        vm - Review my tasks
        gr - Generate reports
        ds - Display statistics
        e -  To exit
        : ''').lower()
   # To display the menu for other users  
    else:
        menu = input('''Please choose out of options below:
        r -  Register user
        a -  Add task
        va - Review all tasks
        e -  To exit
        : ''').lower()

    if menu == 'r':
        username = input("Enter a new user name: ")
        reg_user(username)

    elif menu == 'a':
        title = input("Enter task title: ")
        description = input("Enter task description: ")

        add_task(current_user, title, description)

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        user_tasks = view_mine(current_user)

        if user_tasks:
            task_choice = input("Enter a number of the task to edit (0 - return to menu): ")

            if task_choice.isdigit():
                task_choice = int(task_choice)
                if 0 < task_choice <= len(user_tasks):
                    task_choice -= 1
                    action = input(
                        "Choose an action (c - to mark as completed, e - to edit, m - return to menu): ").lower()

                    if action == 'c':
                        mark_complete(task_choice, user_tasks)
                    elif action == 'e':
                        edit_task(task_choice, user_tasks, current_user)
                    elif action == 'm':
                        print("You have chosen to return to menu")
                    else:
                        print("Not correct choice")
                elif task_choice == 0:
                    print("You have chosen to return to menu")
                else:
                    print("Not correct choice")
            else:
                print("Not correct choice")
        else:
            print("There are no tasks to edit")

    elif menu == 'gr':
        generate_reports()

    elif menu == 'ds':
        display_statistics()

    elif menu == 'e':
        print('Goodbye!')