import tkinter as tk
from tkinter import ttk, messagebox
from playsound import playsound
import threading

class PomodoroApp:
    def __init__(self, root):
        self.root = root # Tkinter 메인창 root 설정
        self.root.title("Pomodoro Timer") # 창 제목 설정

        # 기본 설정 변수들
        self.work_minutes = tk.IntVar(value=25) # 집중 시간
        self.break_minutes = tk.IntVar(value=5) # 쉬는 시간 
        self.repetitions = tk.IntVar(value=4) # 반복 횟수
        self.current_rep = 0 # 현재까지 반복된 횟수 추적
        self.timer_running = False # 타이머의 실행 여부를 확인
        self.paused = False # 타이머가 멈춰있는지 확인
        self.remaining_time = 0 # 타이머가 멈추었을 때 남아있는 시간 저장
        self.total_time = 0 # 작업 시간 또는 쉬는 시간 동안의 총 시간 저장

        # UI 구성
        self.setup_ui()

    def setup_ui(self):
        # 메인 프레임 생성
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 집중 시간 입력 필드
        ttk.Label(main_frame, text="집중 시간 (분):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.work_entry = ttk.Entry(main_frame, textvariable=self.work_minutes, width=5)
        self.work_entry.grid(row=0, column=1, pady=5)

        # 쉬는 시간 입력 필드
        ttk.Label(main_frame, text="쉬는 시간 (분):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.break_entry = ttk.Entry(main_frame, textvariable=self.break_minutes, width=5)
        self.break_entry.grid(row=1, column=1, pady=5)

        # 반복 횟수 입력 필드
        ttk.Label(main_frame, text="반복 횟수:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.rep_entry = ttk.Entry(main_frame, textvariable=self.repetitions, width=5)
        self.rep_entry.grid(row=2, column=1, pady=5)

        # 시작/멈춤 버튼
        self.start_pause_button = tk.Button(main_frame, text="시작", command=self.toggle_start_pause, width=15, height=2)
        self.start_pause_button.grid(row=3, column=0, columnspan=2, pady=10)

        # 상태 표시 라벨
        self.status_label = ttk.Label(main_frame, text="Pomodoro Timer 준비 중...", background="white", relief="solid", padding=5)
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        # 진행 바 (Progress Bar)
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=5, column=0, columnspan=2, pady=10)

    def toggle_start_pause(self):
        if not self.timer_running:
            # 타이머가 시작되지 않은 경우 시작
            self.start_pomodoro()
            self.start_pause_button.config(text="멈춤")
        elif self.paused:
            # 타이머가 멈춰있는 경우 재개
            self.paused = False
            self.start_pause_button.config(text="멈춤")
            self.countdown(self.remaining_time, self.current_completion_message)
        else:
            # 타이머가 실행 중인 경우 멈춤
            self.pause_pomodoro()

    def start_pomodoro(self):
        if not self.timer_running:
            self.timer_running = True
            self.current_rep = 0
            self.paused = False
            self.run_session()

    def pause_pomodoro(self):
        if self.timer_running and not self.paused:
            self.paused = True
            self.start_pause_button.config(text="시작")
            self.status_label.config(background="lightyellow")

    def run_session(self):
        if self.current_rep < self.repetitions.get():
            # 작업 세션
            self.current_rep += 1
            self.status_label.config(text=f"집중 시간 (세션 {self.current_rep})", background="lightgreen")
            self.total_time = self.work_minutes.get() * 60
            self.progress.config(maximum=self.total_time)
            self.countdown(self.total_time, "집중 시간 종료! 쉬는 시간 시작!")
        else:
            messagebox.showinfo("완료", "모든 Pomodoro 세션을 완료했습니다. 수고하셨습니다!")
            self.status_label.config(text="모든 세션 완료", background="white")
            self.timer_running = False
            self.start_pause_button.config(text="시작")

    def countdown(self, count, completion_message):
        if not self.paused:
            if count >= 0:
                self.remaining_time = count
                self.current_completion_message = completion_message
                mins, secs = divmod(count, 60)
                self.status_label.config(text=f"타이머: {mins:02d}:{secs:02d}", background="lightgreen")
                self.progress["value"] = self.total_time - count
                self.root.after(1000, self.countdown, count - 1, completion_message)
            else:
                # 알림 소리 재생
                threading.Thread(target=self.play_sound).start()
                
                messagebox.showinfo("알림", completion_message)
                if "쉬는 시간" in completion_message:
                    # 쉬는 시간 후에 다음 작업 세션 시작
                    self.status_label.config(text="쉬는 시간 진행 중...", background="lightblue")
                    self.total_time = self.break_minutes.get() * 60
                    self.progress.config(maximum=self.total_time)
                    self.countdown(self.total_time, "쉬는 시간 종료! 다시 집중할 시간입니다!")
                else:
                    # 작업 세션 완료 후 쉬는 시간 시작
                    self.run_session()

    def play_sound(self):
        """소리 알림을 재생합니다."""
        try:
            playsound("Taeyeon.mp3")
        except Exception as e:
            print(f"오디오 파일 재생 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    root = tk.Tk()

    # 창의 크기 설정
    root.geometry("420x400")  # 창의 크기를 더 넓게 설정

    app = PomodoroApp(root)
    root.mainloop()
