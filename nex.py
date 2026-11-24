import os, sys, webbrowser, speech_recognition as sr
import tkinter as tk
import threading
from tkinter import ttk
import pyttsx3



r=sr.Recognizer()
print('Некс запущен...')
assistant_active=False


window = tk.Tk()
window.title('Nex')
window.geometry("300x200")
window.resizable(True, True)
icon=tk.PhotoImage(file='nex_icon.png')
window.iconphoto(False, icon)

status=tk.Label(window,text='Nex выключен...',fg='purple',font=('arial',20))
status.place(relx=.5,rely=.15,anchor='center',height=25,width=200)


def start_nex():
    global assistant_active
    assistant_active=True
    status.config(text='Nex работает...',fg='blue')
    status.place(relx=.5,rely=.15,anchor='center',height=25,width=200)


def stop_nex():
    global assistant_active
    assistant_active=False
    status.config(text=' Nex выключен...',fg='purple')
    status.place(relx=.5, rely=.15, anchor='center', height=25, width=200)





def nex_logic():
    global is_working,assistant_active

    try:
        with sr.Microphone() as src:
            r.adjust_for_ambient_noise(src, duration=0.5)

            while is_working:
                audio=r.listen(src)

                try:

                    cmd = r.recognize_google(audio, language='ru-RU').lower()
                    print(f'Вы:{cmd}')


                    if assistant_active==True:

                        if 'браузер' in cmd:
                            webbrowser.open('https://google.com')

                        elif 'калькулятор' in cmd:
                            os.system('calc' if sys.platform == 'win32' else 'open -a Calculator')

                        elif 'хватит' in cmd or 'отдохни' in cmd:
                            window.after(0,stop_nex)

                        elif 'запиши' in cmd:
                            with open('notes.txt','a',encoding='utf-8',) as notes:
                                note=cmd.replace('запиши','')
                                notes.write(note.strip() +'\n')

                        elif 'включи музыку' in cmd:
                            os.system('"C:\Program Files\Google\Chrome\Application\chrome.exe" --app=https//:yandex.ru')


                        elif 'найди' in cmd:
                            searching=cmd.replace('найди','')
                            webbrowser.open('https://google.com/search?q='+searching.strip())


                        elif 'открой youtube' in cmd or 'открой ютуб' in cmd:
                            webbrowser.open('https://youtube.com')

                    else:
                        if 'за работу' in cmd or 'включись' in cmd:
                            window.after(0,start_nex)

                except sr.RequestError:
                    print('Нет соединения')
                except sr.UnknownValueError:
                    print('Nex вас не понял')
    except Exception as e:
            print(f'Ошибка: {e}')

# window = tk.Tk()
# window.title('Nex')
# window.geometry("300x200")
# window.resizable(True, True)
# icon=tk.PhotoImage(file='nex_icon.png')
# window.iconphoto(False, icon)

# status=tk.Label(window,text='Nex выключен...',fg='purple',font=('arial',20))
# status.place(relx=.5,rely=.15,anchor='center',height=25,width=200)

start_button=ttk.Button(text='За работу',command=start_nex)
start_button.place(relwidth=.3,relheight=.12,anchor='center',relx=.5,rely=.35)



stop_button=ttk.Button(text='Отдохнуть',command=stop_nex)
stop_button.place(relwidth=.3,relheight=.12,anchor='center',relx=.5,rely=.5)



is_working=True
nex_thread = threading.Thread(target=nex_logic,daemon=True)
nex_thread.start()

window.mainloop()