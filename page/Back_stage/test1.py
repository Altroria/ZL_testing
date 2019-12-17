from tkinter import *
#初始化Tk()
myWindow = Tk()
#设置标题
myWindow.title('重建用户')

Button(
    myWindow,
    text='删除单位',
    font=('Helvetica 10 bold'),
    relief='raised',
    width=8,
    height=2).grid(
        row=0, column=0, sticky=W, padx=5, pady=5)

Button(
    myWindow,
    text='新增单位',
    font=('Helvetica 10 bold'),
    relief='raised',
    width=8,
    height=2).grid(
        row=0, column=1, sticky=W, padx=5, pady=5)

Button(
    myWindow,
    text='新增单位',
    font=('Helvetica 10 bold'),
    relief='raised',
    width=8,
    height=2).grid(
        row=0, column=1, sticky=W, padx=5, pady=5)

Button(
    myWindow,
    text='新增单位',
    font=('Helvetica 10 bold'),
    relief='raised',
    width=8,
    height=2).grid(
        row=0, column=1, sticky=W, padx=5, pady=5)

Button(
    myWindow,
    text='退出',
    font=('Helvetica 10 bold'),
    relief='raised',
    command=myWindow.quit,
    width=8,
    height=2).grid(
        row=0, column=2, sticky=W, padx=5, pady=5)
#进入消息循环
myWindow.mainloop()
