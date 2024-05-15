# Simple task manager program for small business
import datetime
import os


# Login to program
def login():
    while True:
        action = input('''Please choose an action
        login - to log in
        register - to register
        exit - to exit
        : ''').lower()

        if action == 'login':
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            if check_user_exists(username):
                if check_password(username, password):
                    return username
                else:
                    print("Incorrect password. Please try again.")
            else:
                print("User not found. Please try again.")

        elif action == 'register':
            while True:
                username = input("Enter a new username: ")
                password = input("Enter a password: ")

                if check_user_exists(username):
                    print("The username already exists. Please choose another one.")
                else:
                    reg_user(username, password)
                    break

        elif action == 'exit':
            print('Goodbye!')
            exit()

        else:
            print("Invalid choice. Please try again.")


# Check the password
def check_password(username, password):
    with open('user.txt', 'r') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split(',')
        if len(parts) == 2:
            stored_username, stored_password = parts
            if username == stored_username:
                return password == stored_password

    return False


def check_user_exists(username):
    with open('user.txt', 'r') as f:
        # Reads only the usernames from the file
        users = [line.strip().split(',')[0] for line in f]

    return username in users


# To register a user
def reg_user(username, password):
    with open('user.txt', 'r') as f:
        users = [line.strip() for line in f]

    if username in users:
        print(" The user already exists. Please, choose another name")
        return False
    with open('user.txt', 'a') as f:
        f.write(f"{username},{password}\n")
    print("The user was registered successfully")

    return True


# To add new task
def add_task(username, title, description):
    # Assignment of the status "In progress" for every added task
    status = 'In progress'

    while True:
        due_date = input("Enter the deadline for the task (e.g. YYYY-MM-DD): ")
        try:
            datetime.datetime.strptime(due_date, '%Y-%m-%d')
            break
        except ValueError:
            print("Incorrect date format. Please use the format YYYY-MM-DD")

    # To assign task to yourself or other user
    assign_choice = input('''Who will be in charge?:
    s - yourself
    other - other user
    : ''').lower()

    if assign_choice == 's':
        assigned_user = username
    else:
        with open('user.txt', 'r') as f:
            users = [line.strip() for line in f]

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
        tasks = f.readlines()

    if not tasks:
        print("There are no tasks to display.")
        return

    print("Tasks:")
    print("_" * 50)
    for task in tasks:
        parts = task.strip().split(', ')

        if len(parts) == 5:
            assigned_user, title, description, due_date, status = parts
            print("Task: {}".format(title))
            print("Description: {}".format(description))
            print("In charge: {}".format(assigned_user))
            print("Due date: {}".format(due_date))
            print("Status: {}".format(status))
            print("_" * 50)
        else:
            print("Incorrect format in the tasks file: {}".format(task))


def view_mine(current_user):
    with open('tasks.txt', 'r') as f:
        tasks = f.readlines()

    user_tasks = [task for task in tasks if task.split(', ')[0] == current_user]

    if not user_tasks:
        print("There are no tasks assigned to you.")
        return

    print("Your tasks:")
    print("_" * 50)
    for task in user_tasks:
        parts = task.strip().split(', ')

        if len(parts) == 5:
            _, title, description, due_date, status = parts
            print("Task: {}".format(title))
            print("Description: {}".format(description))
            print("Due date: {}".format(due_date))
            print("Status: {}".format(status))
            print("_" * 50)
        else:
            print("Incorrect format in the tasks file: {}".format(task))


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

    action = input('''Choose to edit:
    u — for user in charge
    d — for due date
    m — for return to menu
    : ''').lower()

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
current_user = login()

if current_user == 'admin':
    while True:
        menu = input('''Please select one out of the options below:
        r - Register user
        a - Add task
        va - Review all tasks
        vm - Review my tasks
        gr - Generate reports
        ds - Display statistics
        e - To exit
        : ''').lower()

        if menu == 'r':
            username = input("Enter a new user name: ")
            password = input("Enter a password: ")
            reg_user(username, password)

        elif menu == 'a':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            add_task(current_user, title, description)

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            user_tasks = view_mine(current_user)

            if user_tasks:
                task_choice = input("Choose a task number to edit (0 - to exit): ")

                if task_choice.isdigit():
                    task_choice = int(task_choice)

                    if 0 < task_choice <= len(user_tasks):
                        task_choice -= 1
                        action = input('''Choose an action:
                        c - to mark as completed
                        e - to edit
                        m - to exit
                        :''').lower()

                        if action == 'c':
                            mark_complete(task_choice, user_tasks)

                        elif action == 'e':
                            edit_task(task_choice, user_tasks, current_user)

                        elif action == 'm':
                            print("Exit to menu")

                        else:
                            print("Invalid choice")

                    elif task_choice == 0:
                        print("Exit to menu")

                    else:
                        print("Invalid choice")

                else:
                    print("Invalid choice")

            else:
                print("There are no tasks to display")

        elif menu == 'gr':
            generate_reports()

        elif menu == 'ds':
            display_statistics()

        elif menu == 'e':
            print('Goodbye!')
            break

        else:
            print("Invalid choice. Please try again.")

else:
    while True:
        menu = input('''Please choose out of options below:
        r - Register user
        a - Add task
        va - Review all tasks
        e - To exit
        vm - Review my tasks 
        : ''').lower()

        if menu == 'r':
            username = input("Enter a new user name: ")
            password = input("Enter a password: ")
            reg_user(username, password)

        if menu == 'a':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            add_task(current_user, title, description)

        elif menu == 'vm':
            user_tasks = view_mine(current_user)

        elif menu == 'va':
            view_all()

        elif menu == 'e':
            print('Goodbye!')
            break

        else:
            print("Invalid choice. Please try again.")
