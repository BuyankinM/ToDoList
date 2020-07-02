from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
today = datetime.now().date()


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=today)

    def __repr__(self):
        return self.task


def print_day_tasks(day, day_name=""):
    if not day_name:
        day_name = day.strftime("%A")

    print(f"{day_name} {day.strftime('%d %b')}:")

    rows = session.query(Task).filter(Task.deadline == day).all()
    for i, row in enumerate(rows):
        print(f"{i}. {row}")
    else:
        if not rows:
            print("Nothing to do!")
        print()


def print_weeks_tasks():
    for i in range(7):
        cur_day = today + timedelta(days=i)
        print_day_tasks(cur_day)


def print_all_tasks():
    print("All tasks:")

    rows = session.query(Task).order_by(Task.deadline)
    for i, row in enumerate(rows):
        print(f"{i}. {row.task}. {row.deadline.strftime('%d %b')}")


def print_missed_tasks():
    print("Missed tasks:")

    rows = session.query(Task).filter(Task.deadline < today).order_by(Task.deadline)
    for i, row in enumerate(rows):
        print(f"{i}. {row.task}. {row.deadline.strftime('%d %b')}")
    else:
        if not rows:
            print("Nothing is missed!")
        print()


def add_new_task():
    task_name = input("Enter task\n")
    deadline_str = input("Enter deadline\n")
    deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d")

    new_row = Task(task=task_name, deadline=deadline_date)
    session.add(new_row)
    session.commit()

    print("The task has been added!\n")


def delete_task():
    print("Chose the number of the task you want to delete:")

    rows = session.query(Task).order_by(Task.deadline)
    for i, row in enumerate(rows):
        print(f"{i}. {row.task}. {row.deadline.strftime('%d %b')}")

    num_del = int(input())
    session.delete(rows[num_del])
    session.commit()

    print("The task has been deleted!\n")


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


while True:
    print("1) Today's tasks\n"
          "2) Week's tasks\n"
          "3) All tasks\n"
          "4) Missed tasks\n"
          "5) Add task\n"
          "6) Delete task\n"
          "0) Exit")
    user_input = input()
    print()

    if user_input == "1":
        print_day_tasks(today, "Today")
    elif user_input == "2":
        print_weeks_tasks()
    elif user_input == "3":
        print_all_tasks()
    elif user_input == "4":
        print_missed_tasks()
    elif user_input == "5":
        add_new_task()
    elif user_input == "6":
        delete_task()

    else:
        print("Bye!")
        break
