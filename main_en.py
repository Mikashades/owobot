import tkinter as tk
from tkinter import ttk
import keyboard
import pyautogui
import time
import threading
import win32api
import win32con
import win32clipboard
from datetime import datetime
import winsound

class OwOBot:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Discord OwO Bot")
        self.window.geometry("600x800")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.theme()
        
        self.copy_count = tk.StringVar(value="3")
        self.msgui()
        self.btn()
        self.csl()
        
        self.running = False
        self.bot_threads = []
        self.last_click = 0
        self.last_send = [0, 0, 0]
        self.message_lock = threading.Lock()

    def theme(self):
        self.window.configure(bg='#1e1e1e')
        for w in ['TFrame', 'TLabelframe', 'TLabel', 'TButton', 'TEntry']:
            self.style.configure(w, background='#1e1e1e', foreground='white')
            if w == 'TEntry':
                self.style.configure(w, fieldbackground='#333333')

    def msgui(self):
        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Message Settings", padding="10")
        self.input_frame.pack(fill=tk.X, pady=5)
        
        self.msg = []
        self.time = []
        
        for i in range(3):
            frame = ttk.Frame(self.input_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=f"Time (sec):").pack(side=tk.LEFT, padx=5)
            t = ttk.Entry(frame, width=10)
            t.pack(side=tk.LEFT, padx=5)
            self.time.append(t)
            
            ttk.Label(frame, text="Message:").pack(side=tk.LEFT, padx=5)
            m = ttk.Entry(frame)
            m.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            self.msg.append(m)
        
        # Frame for copy settings
        copy_frame = ttk.Frame(self.input_frame)
        copy_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(copy_frame, text="Copy count (1-5):").pack(side=tk.LEFT, padx=5)
        copy_spin = ttk.Spinbox(copy_frame, from_=1, to=5, width=5, 
                               textvariable=self.copy_count)
        copy_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(copy_frame, text="(Recommended: 3)").pack(side=tk.LEFT, padx=5)

    def btn(self):
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_frame.pack(fill=tk.X, pady=10)
        
        self.start_btn = ttk.Button(self.btn_frame, text="Start", command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(self.btn_frame, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

    def csl(self):
        self.csl_frame = ttk.LabelFrame(self.main_frame, text="Console", padding="10")
        self.csl_frame.pack(fill=tk.BOTH, expand=True)
        
        self.csl_txt = tk.Text(self.csl_frame, wrap=tk.WORD, height=10,
                            bg='#333333', fg='white', insertbackground='white',
                            state='disabled')
        self.csl_txt.pack(fill=tk.BOTH, expand=True)
        
        scroll = ttk.Scrollbar(self.csl_frame, orient=tk.VERTICAL, command=self.csl_txt.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.csl_txt.configure(yscrollcommand=scroll.set)

    def write(self, msg):
        time = datetime.now().strftime("%H:%M:%S")
        self.csl_txt.configure(state='normal')
        self.csl_txt.insert(tk.END, f"[{time}] {msg}\n")
        self.csl_txt.see(tk.END)
        self.csl_txt.configure(state='disabled')

    def lastmsg(self):
        try:
            pyautogui.click()
            time.sleep(0.2)
            pyautogui.tripleClick()
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.2)
            
            try:
                win32clipboard.OpenClipboard()
                text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
                if not text: return ""
                text = text.strip()
                self.write(f"Copy: {text}")
                return text
            except:
                win32clipboard.CloseClipboard()
                return ""
        except Exception as e:
            self.write(f"Error: {str(e)}")
            return ""

    def alert(self):
        try:
            for _ in range(5):
                winsound.Beep(1000, 300)
                winsound.Beep(2000, 300)
                winsound.Beep(3000, 300)
                time.sleep(0.1)
            
            import os
            os.system('msg * "CAPTCHA DETECTED - BOT STOPPED!"')
        except:
            pass

    def check(self, msg):
        if not msg: return True
        try:
            org = msg
            msg = msg.lower()
            
            if "⚠️" in org and "are you a real human?" in msg:
                self.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                self.write("!!!   CAPTCHA DETECTED!!!    !!!")
                self.write("!!!      BOT STOPPING       !!!")
                self.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                self.write(f"Message: {org}")
                
                self.running = False
                self.alert()
                
                self.window.lift()
                self.window.focus_force()
                self.csl_txt.configure(bg='red')
                self.window.after(1000, lambda: self.csl_txt.configure(bg='#333333'))
                self.window.after(0, self.stop)
                return False

            caps = [
                "⚠️",
                ":blank: |",
                "are you a real human?",
                "please use the link below",
                "so i can check",
                "Please complete this within 10 minutes",
                "or it may result in a ban!",
                "please complete your captcha",
                "verify that you are human",
                "(1/5)", "(2/5)", "(3/5)", "(4/5)", "(5/5)"
            ]

            for cap in caps:
                if cap in msg:
                    self.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    self.write("!!!   CAPTCHA DETECTED!!!    !!!")
                    self.write("!!!      BOT STOPPING       !!!")
                    self.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    self.write(f"Message: {org}")
                    self.write(f"Cap: {cap}")
                    
                    self.running = False
                    self.alert()
                    
                    self.window.lift()
                    self.window.focus_force()
                    self.csl_txt.configure(bg='red')
                    self.window.after(1000, lambda: self.csl_txt.configure(bg='#333333'))
                    self.window.after(0, self.stop)
                    return False
            return True
        except Exception as e:
            self.write(f"Error: {str(e)}")
            return True

    def message_loop(self, index):
        try:
            message = self.msg[index].get().strip()
            time_str = self.time[index].get().strip()
            
            if not message:
                self.write(f"Message box {index+1} cannot be empty!")
                return
            
            try:
                delay = float(time_str)
                if delay <= 0:
                    self.write(f"Time {index+1} must be greater than 0!")
                    return
            except ValueError:
                self.write(f"Time {index+1} must be a valid number!")
                return
            
            while self.running:
                try:
                    with self.message_lock:
                        if time.time() - self.last_send[index] >= delay:
                            try:
                                copy_count = int(self.copy_count.get())
                                if not 1 <= copy_count <= 5:
                                    raise ValueError("Copy count must be between 1-5!")
                            except ValueError as e:
                                self.write(f"Error: {str(e)}")
                                self.running = False
                                self.window.after(0, self.stop)
                                return
                            
                            for _ in range(copy_count):
                                last_message = self.lastmsg()
                                if not self.check(last_message):
                                    self.running = False
                                    self.window.after(0, self.stop)
                                    return
                                time.sleep(0.3)
                            
                            pyautogui.write(message)
                            pyautogui.press('enter')
                            self.write(f"Message sent: {message}")
                            
                            time.sleep(0.7)
                            
                            for _ in range(copy_count):
                                last_message = self.lastmsg()
                                if not self.check(last_message):
                                    self.running = False
                                    self.window.after(0, self.stop)
                                    return
                                time.sleep(0.3)
                            
                            self.last_send[index] = time.time()
                    
                    time.sleep(0.1)
                    
                except Exception as e:
                    self.write(f"Loop error: {str(e)}")
                    continue
        except Exception as e:
            self.write(f"Critical error: {str(e)}")
            self.running = False
            self.window.after(0, self.stop)

    def start(self):
        try:
            if not self.running:
                valid_inputs = False
                for i in range(3):
                    msg = self.msg[i].get().strip()
                    time_str = self.time[i].get().strip()
                    
                    if msg or time_str:
                        if not msg:
                            self.write(f"Message box {i+1} cannot be empty!")
                            return
                        if not time_str:
                            self.write(f"Time box {i+1} cannot be empty!")
                            return
                        
                        try:
                            delay = float(time_str)
                            if delay <= 0:
                                self.write(f"Time {i+1} must be greater than 0!")
                                return
                            valid_inputs = True
                        except ValueError:
                            self.write(f"Time {i+1} must be a valid number!")
                            return

                if not valid_inputs:
                    self.write("You must enter at least one message and time!")
                    return
                
                try:
                    copy_count = int(self.copy_count.get())
                    if not 1 <= copy_count <= 5:
                        self.write("Copy count must be between 1-5!")
                        return
                except ValueError:
                    self.write("Copy count must be a valid number!")
                    return

                self.running = True
                self.write("Bot starting...")
                time.sleep(3)
                
                pyautogui.click()
                time.sleep(0.5)
                
                for i in range(3):
                    if self.msg[i].get().strip() and float(self.time[i].get().strip()) > 0:
                        t = threading.Thread(target=self.message_loop, args=(i,))
                        t.daemon = True
                        self.bot_threads.append(t)
                        t.start()
                        time.sleep(0.5)
                
                self.start_btn.configure(state=tk.DISABLED)
                self.stop_btn.configure(state=tk.NORMAL)
        except Exception as e:
            self.write(f"Start error: {str(e)}")
            self.running = False

    def stop(self):
        self.running = False
        time.sleep(0.5)
        
        try:
            for thread in self.bot_threads:
                if thread.is_alive():
                    thread.join(0)
        except:
            pass
            
        self.bot_threads.clear()
        
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
        except:
            pass
            
        self.start_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        self.write("Bot stopped")

    def run(self):
        self.window.mainloop()

bot = OwOBot()
bot.run() 
