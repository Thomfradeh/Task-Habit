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

        # Root Variables
        self.current_frame = tk.Frame()
        self.fetch_frame = None
        self.bar = None
        self.lastweek, self.lastweekdays = fetch_lastweek()

        # Fetching data
        self.daily_tasks = fetch_daily_tasks()
        for task in self.daily_tasks:
            task.append(tk.IntVar())  # Creating a completion tracker for every task
            if task[2][date.today().weekday()] == 'T' and date.isoformat(date.today()) in task[3]:
                # Investigating if the task has already been done
                task[4].set(1)

        self.habits = fetch_habits()
        for habit in self.habits:
            habit.append(tk.IntVar())  # Creating a daily hour tracker for every task
            if date.isoformat(date.today()) in habit[4]:
                # Investigating if the habit already has hours completed
                habit[5].set(habit[4].split(';')[-1].split(':')[1])
                habit[4] = habit[4][:-13]

        # Initializing Menu Bar
        menu_bar = tk.Menu(self.root)
        menu_bar.add_command(command=self.dailytask_frame, label='Daily Task Board')
        menu_bar.add_command(command=self.dailytask_config, label='Daily Task Config')
        menu_bar.add_command(command=self.habits_frame, label='Habits Board')

        self.root.config(menu=menu_bar)

        # Initializing Tab Method
        # self.dailytask_frame()

        # Root Protocols and Initialization
        self.root.protocol('WM_DELETE_WINDOW', self.save_sequence)
        self.root.mainloop()

    def dailytask_frame(self):

        # Creating Daily Task frame
        self.current_frame.destroy()
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
                                        command=self.widget_fetch(task, 'task'))
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
        recurrence = info[3].split(';')

        red_x = tk.PhotoImage(file='Red_X.png').subsample(2, 2)
        green_c = tk.PhotoImage(file='Green_Tick.png').subsample(2, 2)
        gray_o = tk.PhotoImage(file='Grey_Circle.png').subsample(2, 2)

        # Task Description add-on
        description = tk.Message(self.fetch_frame, text=str(info[1]), justify=tk.LEFT, width=200)
        description.grid(row=0, rowspan=2, column=0, padx=20)

        # Task Completion Tracker
        for c, day in enumerate(self.lastweek):
            pretty_day = day.split('-')[1]+'/'+day.split('-')[2]

            if info[2][self.lastweekdays[c]] == 'T' and self.lastweek[c] in recurrence:
                # If task was supposed to be completed and was, add green checkmark
                weekbutton = tk.Button(self.fetch_frame, text=pretty_day, image=green_c, compound=tk.TOP, width=50)
                weekbutton.image = green_c
            elif info[2][self.lastweekdays[c]] == 'T' and self.lastweek[c] not in recurrence:
                # If task was supposed to be completed but wasn't, add red X
                weekbutton = tk.Button(self.fetch_frame, text=pretty_day, image=red_x, compound=tk.TOP, width=50)
                weekbutton.image = red_x
            else:
                # If task wasn't supposed to be completed, add gray circle
                weekbutton = tk.Button(self.fetch_frame, text=pretty_day, image=gray_o, compound=tk.TOP, width=50)
                weekbutton.image = gray_o

            weekbutton.grid(row=c//3, column=(c % 3)+1)

        # isCompleted Checkbox add_on
        iscompleted_check = tk.Checkbutton(self.fetch_frame, text='Was it done today?', variable=info[4],
                                           command=self.update_bar)
        iscompleted_check.grid(row=3, column=1, columnspan=5, pady=10)

        self.fetch_frame.pack(fill='x')

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

    def dailytask_config(self):

        # Initializing New Tab
        self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root, width=500, height=500)
        self.current_frame.pack_propagate(False)
        self.fetch_frame = tk.Frame(self.current_frame)

        # Initializing options menu
        button_array = tk.Frame(self.current_frame)
        create_task_button = tk.Button(button_array, command=self.create_daily_task, text='New Task',)
        create_task_button.grid(row=0, column=0)

        button_array.pack()

        # Packing Frame
        self.current_frame.pack()

    def create_daily_task(self):

        # Initializing Widget Frame
        self.fetch_frame.destroy()
        self.fetch_frame = tk.LabelFrame(self.current_frame, text='New Task Creation Menu', height=480)
        self.fetch_frame.grid_propagate(False)

        # Variables
        weekdays_input = {'Monday': tk.BooleanVar(), 'Tuesday': tk.BooleanVar(), 'Wednesday': tk.BooleanVar(),
                          'Thursday': tk.BooleanVar(), 'Friday': tk.BooleanVar(), 'Saturday': tk.BooleanVar(),
                          'Sunday': tk.BooleanVar()}

        # Element Creation
        name_label = tk.Label(self.fetch_frame, text='Name')
        name_input_box = tk.Entry(self.fetch_frame)

        desc_label = tk.Label(self.fetch_frame, text='Description')
        desc_input_box = tk.Text(self.fetch_frame, width=40, height=5)

        weekdays_label = tk.Label(self.fetch_frame, text='Weekdays')
        weekdays_input_box = tk.Label(self.fetch_frame)
        for name, tracker in weekdays_input.items():
            weekday_tracker = tk.Checkbutton(weekdays_input_box, text=name, variable=tracker)
            weekday_tracker.pack(anchor='w')

        elements = [name_input_box, desc_input_box, weekdays_input]

        create_button = tk.Button(self.fetch_frame, text='Create Daily Task',
                                  command=lambda: self.add_new_task(elements))

        # Widget Structure
        name_label.grid(row=0, column=0, sticky='we', pady=10)
        name_input_box.grid(row=1, column=0, sticky='we')
        desc_label.grid(row=2, column=0, sticky='we', pady=10)
        desc_input_box.grid(row=3, column=0)
        weekdays_label.grid(row=0, column=1, sticky='we', pady=10)
        weekdays_input_box.grid(row=1, rowspan=3, column=1, sticky='we', padx=30)
        create_button.grid(row=4, column=0, columnspan=2, sticky='we')

        self.fetch_frame.pack(fill='x')

    def add_new_task(self, element_list):

        # Fetching Values from Elements
        name_input = element_list[0].get()
        desc_input = remove_linebreaks(element_list[1].get('1.0', tk.END))

        weekday_input = ''
        for tracker in element_list[2].values():
            tracker_out = tracker.get()
            if tracker_out is True:
                weekday_input += 'T'
            else:
                weekday_input += 'F'

        self.daily_tasks.append([name_input, desc_input, weekday_input, '', tk.IntVar()])

    def habits_frame(self):
        # Creating Daily Task frame
        self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root, width=500, height=500)
        self.current_frame.grid_propagate(False)
        self.fetch_frame = tk.Frame(self.current_frame)

        # Dashboard Widget Creation
        dashboard_base = tk.LabelFrame(self.current_frame, text='Habits Dashboard', height=500, width=150)
        dashboard_base.pack_propagate(False)

        # Title Cards Creation
        bar_label = tk.Label(dashboard_base, text='Habits', width=10)
        bar_label.pack(padx=10)

        # Due Tasks Board
        habits_board = tk.Listbox(dashboard_base, height=25)
        habits_board.pack_propagate(False)
        for habit in self.habits:
            habit_option = tk.Button(habits_board, text=habit[0],
                                     command=self.widget_fetch(habit, 'habit'))
            habit_option.pack(fill='x')

        habits_board.pack()
        dashboard_base.grid(row=0, column=0, sticky='ns')

        self.current_frame.pack()

    def habit_widget(self, info):
        # Widget Base creation
        self.fetch_frame.destroy()
        self.fetch_frame = tk.LabelFrame(self.current_frame, text=info[0], width=350)
        self.fetch_frame.grid_propagate(False)

        # Fetching data and Defining Variables
        tracked_days = info[4].split(';')

        hour_tracker = dict()
        for rawday in tracked_days[1:]:
            day, hours = rawday.split(':')
            hour_tracker[day] = float(hours)

        self.daily_hours = tk.DoubleVar()
        daily_completion = tk.IntVar()
        weekly_completion = tk.IntVar()

        # Habit Hours Tracker
        # Description
        description = tk.Label(self.fetch_frame, text=str(info[1]), height=5, width=37)
        description.grid(row=0, column=0, columnspan=4, padx=20)

        separator = ttk.Separator(self.fetch_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=4, sticky='ew', pady=20)

        # Daily Goal Progress
        daily_goal_bar = ttk.Progressbar(self.fetch_frame, orient='vertical', mode='determinate', length=150)
        daily_goal_label = tk.Label(self.fetch_frame, text='Daily Progress')
        daily_goal_tracker = tk.Label(self.fetch_frame, textvariable=daily_completion)

        daily_goal_bar.grid(row=2, rowspan=2, column=0, sticky='we')
        daily_goal_label.grid(row=2, column=1, sticky='we')
        daily_goal_tracker.grid(row=3, column=1, sticky='we')

        # Weekly Goal Progress
        weekly_goal_bar = ttk.Progressbar(self.fetch_frame, orient='vertical', mode='determinate', length=150)
        weekly_goal_label = tk.Label(self.fetch_frame, text='Weekly Progress')
        weekly_goal_tracker = tk.Label(self.fetch_frame, textvariable=weekly_completion)

        weekly_goal_bar.grid(row=2, rowspan=2, column=2, sticky='we')
        weekly_goal_label.grid(row=2, column=3, sticky='we')
        weekly_goal_tracker.grid(row=3, column=3, sticky='we')

        separator = ttk.Separator(self.fetch_frame, orient='horizontal')
        separator.grid(row=4, column=0, columnspan=4, sticky='ew', pady=20)

        # Daily Tracker
        slider = ttk.Scale(self.fetch_frame, from_=0, to=24, orient='horizontal', variable=info[5],
                           command=lambda var: self.update_habit_completion(var, hour_tracker,
                                                                            [daily_goal_bar, weekly_goal_bar],
                                                                            [daily_completion, weekly_completion],
                                                                            [int(info[2]), int(info[3])]))
        slider.grid(row=5, column=0, columnspan=4, sticky='we')

        tracker_day = tk.Label(self.fetch_frame, text='Hours Today:')
        daily_label = tk.Label(self.fetch_frame, textvariable=self.daily_hours)

        tracker_day.grid(row=6, column=0, columnspan=2)
        daily_label.grid(row=6, column=2, columnspan=2)

        self.update_habit_completion(info[5].get(), hour_tracker,
                                     [daily_goal_bar, weekly_goal_bar],
                                     [daily_completion, weekly_completion],
                                     [int(info[2]), int(info[3])])

        self.fetch_frame.grid(row=0, column=1, sticky='ns')

    def update_habit_completion(self, slider_out, info, bars, variables, goals):

        # Daily Progress Tracker
        self.daily_hours.set((float(slider_out)*10//2)/5)

        if goals[0] != 0:
            day_complete = int((self.daily_hours.get() / goals[0])*100)
            match day_complete > 100:
                case True: variables[0].set(100)
                case False: variables[0].set(day_complete)
            bars[0]['value'] = variables[0].get()

        # Weekly Progress Tracker
        week_hours = 0

        for c, day in enumerate(self.lastweek):
            if self.lastweek[c] in info.keys():
                week_hours += info[day]

        week_hours += self.daily_hours.get()

        if goals[1] != 0:
            week_complete = int((week_hours / goals[1])*100)
            match week_complete > 100:
                case True: variables[1].set(100)
                case False: variables[1].set(week_complete)
            bars[1]['value'] = variables[1].get()

    def widget_fetch(self, element=None, widget=''):
        # Temporary fix for Daily Task Dashboards

        match widget:
            case 'task':
                return lambda: self.daily_task_widget(element)
            case 'task_create':
                return lambda: self.create_daily_task()
            case 'habit':
                return lambda: self.habit_widget(element)

    def save_sequence(self):
        # Converting TK variables into numbers
        f_tasks = []
        for task in self.daily_tasks:
            f_task = task[:4]
            f_task.append(task[4].get())
            f_tasks.append(f_task)
        recreate_dailytasks(f_tasks)

        # Closing the App
        self.root.destroy()


def main():
    GUI()


if __name__ == '__main__':
    main()
