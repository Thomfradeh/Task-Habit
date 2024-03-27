import tkinter as tk
from tkinter import ttk
from data_handler import *


class GUI:
    """
    The GUI Class is the main program class, responsible for summoning and managing the TKInter interface

    It has currently two functions:
        daily_task_widget: Static_method that creates a widget for a given task in a preset root
        dailytask_frame: method that generates the dashboard for the Daily Tasks
    """
    def __init__(self):
        self.root = tk.Tk()

        self.current_frame = None
        self.fetch_frame = None

        # Root Variables
        self.bar = None

        # Fetching data
        self.daily_tasks = fetch_daily_tasks()
        for task in self.daily_tasks:
            task.append(tk.IntVar())  # Creating a completion tracker for every task
            if task[2][date.today().weekday()] == 'T' and date.isoformat(date.today()) in task[3]:
                task[4].set(1)

        # Initializing Tab Method
        self.dailytask_frame()

        self.root.mainloop()

    def dailytask_frame(self):

        # Creating Daily Task frame
        self.current_frame = tk.Frame(self.root, width=500, height=500)
        self.current_frame.pack_propagate(False)
        self.fetch_frame = tk.Frame(self.current_frame)

        # Dashboard Widget Creation
        dashboard_base = tk.LabelFrame(self.current_frame, text='Daily Tasks Dashboard', height=300, width=500)
        dashboard_base.grid_propagate(False)

        # Title Cards Creation
        bar_label = tk.Label(dashboard_base, text='Progress', width=10)
        bar_label.grid(row=0, column=0, padx=10)

        tasks_label = tk.Label(dashboard_base, text='Due Tasks', width=45)
        tasks_label.grid(row=0, column=1, padx=10)

        # Due Tasks Board
        due_tasks_board = tk.Listbox(dashboard_base)
        due_tasks_board.pack_propagate(False)
        for task in self.daily_tasks:
            if task[2][date.today().weekday()] == 'T':
                task_option = tk.Button(due_tasks_board, text=task[0],
                                        command=self.widget_fetch(task))
                task_option.pack(fill='x')

        # Daily Progress Bar
        self.bar = ttk.Progressbar(dashboard_base, orient='vertical', mode='determinate', length=225)
        self.bar.grid(row=1, column=0, pady=15, padx=25, sticky='we')
        self.update_bar()

        due_tasks_board.grid(row=1, column=1, sticky='news')
        dashboard_base.pack(fill='x')

        self.current_frame.pack()

    def daily_task_widget(self, info):
        # Widget Base creation
        self.fetch_frame.destroy()
        self.fetch_frame = tk.LabelFrame(self.current_frame, text=info[0], height=200)
        self.fetch_frame.pack_propagate(False)

        # Fetching data and Defining Variables
        lastweek, lastweekdays = fetch_lastweek()
        recurrence = info[3].split(';')

        red_x = tk.PhotoImage(file='Red_X.png').subsample(2, 2)
        green_c = tk.PhotoImage(file='Green_Tick.png').subsample(2, 2)
        gray_o = tk.PhotoImage(file='Grey_Circle.png').subsample(2, 2)

        # Task Description add-on
        description = tk.Message(self.fetch_frame, text=str(info[1]), justify=tk.LEFT, width=200)
        description.grid(row=0, rowspan=2, column=0, padx=20)

        # Task Completion Tracker
        for c, day in enumerate(lastweek):
            pretty_day = day.split('-')[1]+'/'+day.split('-')[2]

            if info[2][lastweekdays[c]] == 'T' and lastweek[c] in recurrence:
                # If task was supposed to be completed and was, add green checkmark
                weekbutton = tk.Button(self.fetch_frame, text=pretty_day, image=green_c, compound=tk.TOP, width=50)
                weekbutton.image = green_c
            elif info[2][lastweekdays[c]] == 'T' and lastweek[c] not in recurrence:
                # If task was supposed to be completed but wasn't, add red X
                weekbutton = tk.Button(self.fetch_frame, text=pretty_day, image=red_x, compound=tk.TOP, width=50)
                weekbutton.image = red_x
            else:
                # If task wasn't supposed to be completed, add gray circle
                weekbutton = tk.Button(self.fetch_frame, text=pretty_day, image=gray_o, compound=tk.TOP, width=50,
                                       command=self.save_sequence)
                weekbutton.image = gray_o

            weekbutton.grid(row=c//3, column=(c % 3)+1)

        # isCompleted Checkbox add_on
        iscompleted_check = tk.Checkbutton(self.fetch_frame, text='Was it done today?', variable=info[4],
                                           command=self.update_bar)
        iscompleted_check.grid(row=3, column=1, columnspan=5, pady=10)

        self.fetch_frame.pack(fill='x')

    def widget_fetch(self, element, widget=''):
        # Temporary fix for Daily Task Dashboards

        return lambda: self.daily_task_widget(element)

    def fetch_done_tasks(self):
        done_tasks = []
        for task in self.daily_tasks:
            if task[4].get():
                done_tasks.append(task)

        return done_tasks

    def update_bar(self):
        done_tasks = len(self.fetch_done_tasks())
        due_tasks = 0
        for task in self.daily_tasks:
            if task[2][date.today().weekday()] == 'T':
                due_tasks += 1

        self.bar['value'] = (done_tasks/due_tasks * 100)//1

    def save_sequence(self):
        # Converting TK variables into numbers
        f_tasks = []
        for task in self.daily_tasks:
            f_task = task[:4]
            f_task.append(task[4].get())
            f_tasks.append(f_task)
        recreate_dailytasks(f_tasks)


def main():
    GUI()


if __name__ == '__main__':
    main()
