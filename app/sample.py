import tkinter

# ウィンドウの作成
root = tkinter.Tk()
root.title("window sample!")
# root.iconbitmap('icon.ico')
root.geometry("300x800")
root.resizable(0, 1)
root.config(bg="red")

# サブウィンドウの作成
sub_window = tkinter.Toplevel()
sub_window.title("Second Window")
sub_window.config(bg="#123123")
sub_window.geometry("200x300+500+500")

# ウィンドウのループ処理
root.mainloop()
