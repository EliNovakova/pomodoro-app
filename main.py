from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"    # color hex codes
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0    # counts repetitions
timer = None    # starts out as none so we can use it globally (if it was only in a function as local variable, we wouldn't be able to cancel the timer)


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    """Resets countdown, changes title to Timer, deletes all checkmarks and sets reps to 0"""
    window.after_cancel(timer)   # cancels the timer
    title_label.config(text="Timer", fg=GREEN)  # changes title label to "Timer"
    canvas.itemconfig(timer_text, text="00:00")     # changes the time to 00:00
    checkmarks_label.config(text="")    # deletes all check marks
    global reps
    reps = 0    # sets reps to 0
# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    """Calls the function count_down."""
    global reps
    work_sec = WORK_MIN * 60    # transfer minutes to seconds
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    reps += 1

    if reps % 8 == 0:   # determine which countdown to run , after 8 runs long break
        count_down(long_break_sec)
        title_label.config(text="Break", fg=RED)    # change the Timer label
    elif reps % 2 == 0:     # after each work session short break
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)    # after each short break work session
        title_label.config(text="Work", fg=GREEN)



# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    """Starts counting down, count is the time at the beginning"""
    global timer
    count_min = math.floor(count/60)    # gives us number of minutes remaining
    count_sec = count % 60  # gives us the number of seconds remaining
    if count_sec < 10:  # we can switch from int to string in a variable thanks to dynamic typing that's allowed in Python (e.g. Java or C doesn't support it)
        count_sec = f"0{count_sec}"     # if one digit number, 0 is added as first digit

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")   # changes a canvas text (timer_text = what we change, text = what exactly we change)
    if count > 0:   # counts down only until it reaches 0
        timer = window.after(1000, count_down, count - 1)   # countdown, 1000 miliseconds = after 1 second, countdown = calls the function itself, count - 1 = subtracts from initial count number
    else:
        start_timer()   # starts another time after the previous one reaches 0
        work_sessions = math.floor(reps/2)  # reps / 2 represent work sessions (the other half are breaks)
        marks = ""
        for i in range(work_sessions):  # for each work_session a mark is added by the loop
            marks += "✔"
        checkmarks_label.config(text=marks)     # marks are passed to the checkmark_label
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW) # adds padding for the window and changes the background color

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)  # creates a canvas widget, changes bg color and border line thickness to 0
tomato_img = PhotoImage(file="tomato.png")  # takes in an image
canvas.create_image(100, 112, image=tomato_img)     # places an image to a canvas
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))  # creates a text placed on the image
canvas.grid(column=1, row=1)


title_label = Label(text="Timer", font=(FONT_NAME, 50), fg=GREEN, bg=YELLOW)    # can change label color by adding fg=color
title_label.grid(column=1, row=0)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)   # can use highlightthickness to erase white line around the button
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

checkmarks_label = Label(fg=GREEN, bg=YELLOW)
checkmarks_label.grid(column=1, row=3)

window.mainloop()