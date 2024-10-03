import tkinter as tk
from tkinter import messagebox
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0  # 글로벌 변수로 타이머 반복 회수 관리
timer = None  # 타이머 ID를 저장할 변수

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps, timer
    if timer:
        window.after_cancel(timer)  # 실행 중인 타이머 취소
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)
    check_marks.config(text="")
    reps = 0
    start_button.config(state="normal")  # 시작 버튼 활성화

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1

    # 타이머의 반복 회수에 따라 다른 세션을 설정
    if reps % 8 == 0:
        count_down(LONG_BREAK_MIN * 60)
        title_label.config(text="Long Break", fg=RED)
    elif reps % 2 == 0:
        count_down(SHORT_BREAK_MIN * 60)
        title_label.config(text="Short Break", fg=PINK)
    else:
        count_down(WORK_MIN * 60)
        title_label.config(text="Work", fg=GREEN)

    # 시작 버튼 비활성화
    start_button.config(state="disabled")

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        # 타이머가 0이 되었을 때, 다음 세션을 시작
        start_timer()
        # 작업 세션이 끝난 경우, 체크 표시 추가
        if reps % 2 == 0:
            marks = ""
            work_sessions = math.floor(reps / 2)
            for _ in range(work_sessions):
                marks += "✔"
            check_marks.config(text=marks)
        # 세션이 완료되면 시작 버튼을 다시 활성화 (사용자가 수동으로 다시 시작 가능하게)
        if reps % 8 == 0:
            start_button.config(state="normal")

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)

# 타이틀 라벨
title_label = tk.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

# 타이머 캔버스
canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# 시작 버튼
start_button = tk.Button(text="Start", command=start_timer, highlightthickness=0)
start_button.grid(column=0, row=2)

# 리셋 버튼
reset_button = tk.Button(text="Reset", command=reset_timer, highlightthickness=0)
reset_button.grid(column=2, row=2)

# 체크 표시 라벨
check_marks = tk.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 24))
check_marks.grid(column=1, row=3)

window.mainloop()
