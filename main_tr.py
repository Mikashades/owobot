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

class OwoBot:
    def __init__(self):
        self.pencere = tk.Tk()
        self.pencere.title("Discord OwO Botu")
        self.pencere.geometry("600x800")
        
        self.stil = ttk.Style()
        self.stil.theme_use('clam')
        self.tema()
        
        self.kopya_sayisi = tk.StringVar(value="3")
        self.msgui()
        self.btn()
        self.ksl()
        
        self.calisiyor = False
        self.bot_threadleri = []
        self.son_tiklama = 0
        self.son_gonderme = [0, 0, 0]
        self.mesaj_kilidi = threading.Lock()

    def tema(self):
        self.pencere.configure(bg='#1e1e1e')
        for w in ['TFrame', 'TLabelframe', 'TLabel', 'TButton', 'TEntry']:
            self.stil.configure(w, background='#1e1e1e', foreground='white')
            if w == 'TEntry':
                self.stil.configure(w, fieldbackground='#333333')

    def msgui(self):
        self.ana_frame = ttk.Frame(self.pencere, padding="10")
        self.ana_frame.pack(fill=tk.BOTH, expand=True)
        
        self.giris_frame = ttk.LabelFrame(self.ana_frame, text="Mesaj Ayarları", padding="10")
        self.giris_frame.pack(fill=tk.X, pady=5)
        
        self.msg = []
        self.sure = []
        
        for i in range(3):
            frame = ttk.Frame(self.giris_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=f"Süre (sn):").pack(side=tk.LEFT, padx=5)
            s = ttk.Entry(frame, width=10)
            s.pack(side=tk.LEFT, padx=5)
            self.sure.append(s)
            
            ttk.Label(frame, text="Mesaj:").pack(side=tk.LEFT, padx=5)
            m = ttk.Entry(frame)
            m.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            self.msg.append(m)
        
        # Kopyalama ayarı için frame
        kopya_frame = ttk.Frame(self.giris_frame)
        kopya_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(kopya_frame, text="Kopyalama sayısı (1-5):").pack(side=tk.LEFT, padx=5)
        kopya_spin = ttk.Spinbox(kopya_frame, from_=1, to=5, width=5, 
                                textvariable=self.kopya_sayisi)
        kopya_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(kopya_frame, text="(Önerilen: 3)").pack(side=tk.LEFT, padx=5)

    def btn(self):
        self.btn_frame = ttk.Frame(self.ana_frame)
        self.btn_frame.pack(fill=tk.X, pady=10)
        
        self.basla = ttk.Button(self.btn_frame, text="Başlat", command=self.start)
        self.basla.pack(side=tk.LEFT, padx=5)
        
        self.dur = ttk.Button(self.btn_frame, text="Durdur", command=self.stop, state=tk.DISABLED)
        self.dur.pack(side=tk.LEFT, padx=5)

    def ksl(self):
        self.ksl_frame = ttk.LabelFrame(self.ana_frame, text="Konsol", padding="10")
        self.ksl_frame.pack(fill=tk.BOTH, expand=True)
        
        self.ksl_txt = tk.Text(self.ksl_frame, wrap=tk.WORD, height=10,
                            bg='#333333', fg='white', insertbackground='white',
                            state='disabled')
        self.ksl_txt.pack(fill=tk.BOTH, expand=True)
        
        scroll = ttk.Scrollbar(self.ksl_frame, orient=tk.VERTICAL, command=self.ksl_txt.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.ksl_txt.configure(yscrollcommand=scroll.set)

    def yaz(self, msg):
        zaman = datetime.now().strftime("%H:%M:%S")
        self.ksl_txt.configure(state='normal')
        self.ksl_txt.insert(tk.END, f"[{zaman}] {msg}\n")
        self.ksl_txt.see(tk.END)
        self.ksl_txt.configure(state='disabled')

    def sonmsg(self):
        try:
            pyautogui.click()
            time.sleep(0.2)
            pyautogui.tripleClick()
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.2)
            
            try:
                win32clipboard.OpenClipboard()
                metin = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
                if not metin: return ""
                metin = metin.strip()
                self.yaz(f"Kopya: {metin}")
                return metin
            except:
                win32clipboard.CloseClipboard()
                return ""
        except Exception as e:
            self.yaz(f"Hata: {str(e)}")
            return ""

    def uyari(self):
        try:
            for _ in range(5):
                winsound.Beep(1000, 300)
                winsound.Beep(2000, 300)
                winsound.Beep(3000, 300)
                time.sleep(0.1)
            
            import os
            os.system('msg * "CAPTCHA TESPİT EDİLDİ - BOT DURDURULDU!"')
        except:
            pass

    def kont(self, msg):
        if not msg: return True
        try:
            org = msg
            msg = msg.lower()
            
            if "⚠️" in org and "are you a real human?" in msg:
                self.yaz("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                self.yaz("!!!   CAPTCHA BULUNDU!!!     !!!")
                self.yaz("!!!     BOT DURDURULUYOR     !!!")
                self.yaz("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                self.yaz(f"Mesaj: {org}")
                
                self.calisiyor = False
                self.uyari()
                
                self.pencere.lift()
                self.pencere.focus_force()
                self.ksl_txt.configure(bg='red')
                self.pencere.after(1000, lambda: self.ksl_txt.configure(bg='#333333'))
                self.pencere.after(0, self.stop)
                return False

            caplar = [
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

            for cap in caplar:
                if cap in msg:
                    self.yaz("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    self.yaz("!!!   CAPTCHA BULUNDU!!!     !!!")
                    self.yaz("!!!     BOT DURDURULUYOR     !!!")
                    self.yaz("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    self.yaz(f"Mesaj: {org}")
                    self.yaz(f"Cap: {cap}")
                    
                    self.calisiyor = False
                    self.uyari()
                    
                    self.pencere.lift()
                    self.pencere.focus_force()
                    self.ksl_txt.configure(bg='red')
                    self.pencere.after(1000, lambda: self.ksl_txt.configure(bg='#333333'))
                    self.pencere.after(0, self.stop)
                    return False
            return True
        except Exception as e:
            self.yaz(f"Hata: {str(e)}")
            return True

    def mesaj_dongusu(self, index):
        try:
            mesaj = self.msg[index].get().strip()
            sure_str = self.sure[index].get().strip()
            
            if not mesaj:
                self.yaz(f"{index+1}. mesaj kutusu boş bırakılamaz!")
                return
            
            try:
                sure = float(sure_str)
                if sure <= 0:
                    self.yaz(f"{index+1}. süre 0'dan büyük olmalıdır!")
                    return
            except ValueError:
                self.yaz(f"{index+1}. süre geçerli bir sayı olmalıdır!")
                return
            
            while self.calisiyor:
                try:
                    with self.mesaj_kilidi:
                        if time.time() - self.son_gonderme[index] >= sure:
                            try:
                                kopya_sayisi = int(self.kopya_sayisi.get())
                                if not 1 <= kopya_sayisi <= 5:
                                    raise ValueError("Kopyalama sayısı 1-5 arasında olmalıdır!")
                            except ValueError as e:
                                self.yaz(f"Hata: {str(e)}")
                                self.calisiyor = False
                                self.pencere.after(0, self.stop)
                                return
                            
                            for _ in range(kopya_sayisi):
                                son_mesaj = self.sonmsg()
                                if not self.kont(son_mesaj):
                                    self.calisiyor = False
                                    self.pencere.after(0, self.stop)
                                    return
                                time.sleep(0.3)
                            
                            pyautogui.write(mesaj)
                            pyautogui.press('enter')
                            self.yaz(f"Mesaj gönderildi: {mesaj}")
                            
                            time.sleep(0.7)
                            
                            for _ in range(kopya_sayisi):
                                son_mesaj = self.sonmsg()
                                if not self.kont(son_mesaj):
                                    self.calisiyor = False
                                    self.pencere.after(0, self.stop)
                                    return
                                time.sleep(0.3)
                            
                            self.son_gonderme[index] = time.time()
                    
                    time.sleep(0.1)
                    
                except Exception as e:
                    self.yaz(f"Döngü hatası: {str(e)}")
                    continue
        except Exception as e:
            self.yaz(f"Kritik hata: {str(e)}")
            self.calisiyor = False
            self.pencere.after(0, self.stop)

    def start(self):
        try:
            if not self.calisiyor:
                valid_inputs = False
                for i in range(3):
                    msg = self.msg[i].get().strip()
                    time_str = self.sure[i].get().strip()
                    
                    if msg or time_str:
                        if not msg:
                            self.yaz(f"{i+1}. mesaj kutusu boş bırakılamaz!")
                            return
                        if not time_str:
                            self.yaz(f"{i+1}. süre kutusu boş bırakılamaz!")
                            return
                        
                        try:
                            sure = float(time_str)
                            if sure <= 0:
                                self.yaz(f"{i+1}. süre 0'dan büyük olmalıdır!")
                                return
                            valid_inputs = True
                        except ValueError:
                            self.yaz(f"{i+1}. süre geçerli bir sayı olmalıdır!")
                            return

                if not valid_inputs:
                    self.yaz("En az bir mesaj ve süre girmelisiniz!")
                    return
                
                try:
                    kopya_sayisi = int(self.kopya_sayisi.get())
                    if not 1 <= kopya_sayisi <= 5:
                        self.yaz("Kopyalama sayısı 1-5 arasında olmalıdır!")
                        return
                except ValueError:
                    self.yaz("Kopyalama sayısı geçerli bir sayı olmalıdır!")
                    return

                self.calisiyor = True
                self.yaz("Bot başlatılıyor...")
                time.sleep(3)
                
                pyautogui.click()
                time.sleep(0.5)
                
                for i in range(3):
                    if self.msg[i].get().strip() and float(self.sure[i].get().strip()) > 0:
                        t = threading.Thread(target=self.mesaj_dongusu, args=(i,))
                        t.daemon = True
                        self.bot_threadleri.append(t)
                        t.start()
                        time.sleep(0.5)
                
                self.basla.configure(state=tk.DISABLED)
                self.dur.configure(state=tk.NORMAL)
        except Exception as e:
            self.yaz(f"Başlatma hatası: {str(e)}")
            self.calisiyor = False

    def stop(self):
        self.calisiyor = False
        time.sleep(0.5)
        
        try:
            for thread in self.bot_threadleri:
                if thread.is_alive():
                    thread.join(0)
        except:
            pass
            
        self.bot_threadleri.clear()
        
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
        except:
            pass
            
        self.basla.configure(state=tk.NORMAL)
        self.dur.configure(state=tk.DISABLED)
        self.yaz("Bot durduruldu")

    def baslat(self):
        self.pencere.mainloop()

bot = OwoBot()
bot.baslat()
