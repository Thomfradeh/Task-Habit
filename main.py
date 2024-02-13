import tkinter as tk
from data_handler import *


class GUI:
    def __init__(self):
        self.root = tk.Tk()

        self.current_frame = None

        # Fetching data
        self.daily_tasks = fetch_daily_tasks()
        for task in self.daily_tasks:
            task.append(tk.IntVar)  # Creating a completion tracker for every task

        # Initializing Tab Method
        self.dailytask_frame()

        self.root.mainloop()

    def dailytask_frame(self):
        # Creating Daily Task frame
        self.current_frame = tk.Frame(self.root)

        # Dashboard Widget Creation
        dashboard_base = tk.LabelFrame(self.current_frame, text='Daily Tasks Dashboard')

        current_task = tk.StringVar
        due_tasks_board = tk.Listbox(dashboard_base, text='Due Tasks')
        for task in self.daily_tasks:
            if task[2][date.today().weekday()] == 'T':


        due_tasks_board.pack()
        dashboard_base.pack()

        self.current_frame.pack()

    @staticmethod
    def daily_task_widget(root, info):
        # Widget Base creation
        widget_base = tk.LabelFrame(root, text=info[0])

        # Fetching data and Defining Variables
        lastweek, lastweekdays = fetch_lastweek()
        recurrence = info[3].split(';')

        red_x = tk.PhotoImage(file='Red_X.png').subsample(2, 2)
        green_c = tk.PhotoImage(file='Green_Tick.png').subsample(2, 2)
        gray_o = tk.PhotoImage(file='Grey_Circle.png').subsample(2, 2)

        # Task Description add-on
        description = tk.Message(widget_base, text=str(info[1]), justify=tk.LEFT)
        description.grid(row=0, rowspan=2, column=0, padx=20)

        # Task Completion Tracker
        for c, day in enumerate(lastweek):
            pretty_day = day.split('-')[1]+'/'+day.split('-')[2]

            if info[2][lastweekdays[c]] == 'T' and lastweek[c] in recurrence:
                # If task was supposed to be completed and was, add green checkmark
                weekbutton = tk.Button(widget_base, text=pretty_day, image=green_c, compound=tk.TOP)
                weekbutton.image = green_c
            elif info[2][lastweekdays[c]] == 'T' and lastweek[c] not in recurrence:
                # If task was supposed to be completed but wasn't, add red X
                weekbutton = tk.Button(widget_base, text=pretty_day, image=red_x, compound=tk.TOP)
                weekbutton.image = red_x
            else:
                # If task wasn't supposed to be completed, add gray circle
                weekbutton = tk.Button(widget_base, text=pretty_day, image=gray_o, compound=tk.TOP)
                weekbutton.image = gray_o

            weekbutton.grid(row=0, column=c+1)

        # isCompleted Checkbox add_on
        iscompleted_check = tk.Checkbutton(widget_base, text='Done?', variable=info[4])
        iscompleted_check.grid(row=1, column=1, columnspan=6)

        widget_base.pack()

def main():
    GUI()


if __name__ == '__main__':
    main()
