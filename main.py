# To Do application
FILE_NAME = "tasks.txt"

PENDING = "[ ]"
DONE = "[x]"

#load tasks from file
def tasks_load():
    tasks=[]
    try:
        with open(FILE_NAME,"r")as file:
            for line in file:
                line = line.strip()
                if line:              # only if line is NOT empty
                    tasks.append(line)

    except FileNotFoundError:
        pass

    return tasks

# save tasks to file
def tasks_save(tasks):
    with open(FILE_NAME,"w") as file:
        for task in tasks:
            file.write(task+"\n")

#viewing tasks:
def view_tasks(tasks):
    if not tasks:
        print("\n no tasks available\n")
        return 
    else:
        print("\n -- Your Tasks --\n ")

        for i,task in enumerate(tasks,1):# giving the task its number starting from 1
            print(f"{i}. {task}")
        print()

# add tasks
def add_tasks(tasks):
    task=input("Add new task:").strip()

    if not task:
        print("Task cannot be empty!\n")
        return

    tasks.append(PENDING +" "+ task)# adding the status code 
    # empty means not done , cross inside the bracket means done
    tasks_save(tasks)# again saving this new task

    print("\n Task Added succesfully!\n")


# delete Tasks
def delete_tasks(tasks):
    view_tasks(tasks)

    if not tasks:
        return
    try:
        task_num=int(input("\n Enter the task number to delete\n"))
    

        if 1<=task_num<=len(tasks):
            removed=tasks.pop(task_num-1)
            tasks_save(tasks)
             print(f"\nRemoved: {removed}\n")
        else:
            print("Invalid task number!\n")

    except:
        print("enter a valid number \n ")
    

# mark tasks as done 
def marks_done(tasks):
    view_tasks(tasks)
    if not tasks:# if to do list is empty
        return
    try:
        num=int(input("Enter the task number to be marked:"))
        task=tasks[num-1]# 0 index is first item of our to do list
        if task.startswith(DONE):
            print("\n already completed\n")
        else:
            tasks[num-1]=task.replace(PENDING,DONE,1)# replacing onlythe first occurence otherwise it would have replaced every bracket

            tasks_save(tasks)

            print("Task marked as done! \n")
    except ValueError:
        print("Invalid input!\n")



# Main menu
def main():
    tasks = tasks_load()   
    while True:
        print("====== TO-DO LIST ======")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Delete Task")
        print("4. Mark Task as Done")
        print("5. Exit")
        print("========================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_tasks(tasks)

        elif choice == "2":
            view_tasks(tasks)

        elif choice == "3":
            delete_tasks(tasks)

        elif choice == "4":
            marks_done(tasks)

        elif choice == "5":
           print("\nGoodbye! Have a productive day 😊")
            break

        else:
            print("Invalid choice! Try again.\n")


# Run program
if __name__ == "__main__":
    main()
       






# TESTING 
# Step 1: Load tasks
'''my_tasks = tasks_load()

print("Tasks loaded from file:")
print(my_tasks)

# Step 2: Add some test tasks
my_tasks.append("Study Python")
my_tasks.append("Do Project")

# Step 3: Save tasks
tasks_save(my_tasks)

print("Tasks saved successfully!")
'''