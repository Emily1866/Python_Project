'''
V3.0 release note:
1.与V2.0版本相比, V3.0用tkinter实现了 UI界面
2.用类对各个模块进行了封装
'''
from tkinter import *
import tkinter.font as tkFont
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

LARGE_FONT = ("Verdana", 20)
filename = 'employee_list.txt'
lst_key = ['id', 'name', 'gender', 'age', 'phone', 'dept', 'salary', 'hiredate']

class Employee:
    def __init__(self):
        pass

    def get_employee_lst(self):
        employee_lst = []
        with open(filename, 'r') as f:
            for line in f:
                lst_value = line.strip('\n').split(',')
                employee = dict(zip(lst_key, lst_value))
                employee_lst.append(employee)
        f.close()
        return employee_lst

    def clear_file_blankline(self, filename):
        with open(filename, 'r+') as f, open('temp.txt', 'w+') as f1:
            f_lst = f.readlines()
            # Modify: for i = n - 1, i > 0, i--:
            for i in range(len(f_lst) - 1, 0, -1):
                if f_lst[i] == '\n':
                    f_lst.remove('\n')
            f1.writelines(f_lst)
            f.close()
            f1.close()
            os.remove(filename)  # 需要把源文件删除
            os.rename('temp.txt', filename)  # 把temp.txt文件重命名成filename

    # 获取新入职员工的ID
    def get_new_id(self,filename):
        f = open(filename, 'r')
        employee_lst = []
        lst_id = []
        # 读取文件并转成字典列表
        for line in f:
            lst_value = line.strip('\n').split(',')
            employee = dict(zip(lst_key, lst_value))
            employee_lst.append(employee)
        # 获取所有员工的工号
        for i in range(len(employee_lst)):
            lst_id.append(employee_lst[i]['id'])

        # lst_id.remove('')#当文件指针在末尾空行时，会多读取一条空记录，删除该空记录
        # print(lst_id)
        # 获取员工工号的最大值
        for i in range(len(lst_id)):
            max_id = 0
            if lst_id[i] != '' and int(lst_id[i]) > max_id:
                max_id = int(lst_id[i])
        return str(max_id + 1)



class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wm_title("员工信息管理系统")
        container = tk.Frame(self)
        container.pack(side = 'top', fill = 'both', expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        #循环功能界面
        for F in (LoginPage, StartPage, AddPage, DeletePage, ModifyPage, QueryPage, ModifyAgePage, ModifyDeptPage, QueryAgePage, QueryDeptPage, QueryHireDatePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ='nsew')
        self.show_frame(LoginPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()#切换，提升当前tk.Frame z轴顺序（使可见）


class LoginPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        # self.root = root
        ft3 = tkFont.Font(size=14)
        ft4 = tkFont.Font(size=12)
        lab1 = Label(self, text='User name:',font = ft3).grid(row=0, column=0, sticky='nsew')
        global ent1
        ent1 = StringVar()
        Entry(self, width=30, textvariable=ent1, font=ft3, bg='Ivory').grid(row=0, column=1, sticky='W')
        lab2 = Label(self, text='Password:', font = ft3).grid(row=1, column=0, sticky='W')
        global ent2
        ent2 = StringVar()
        Entry(self, width=30, textvariable=ent2, show='*', font = ft3).grid(row=1, column=1, sticky='W')
        btn1 = Button(self, text='登录', command=lambda: self.submit(ent1.get(), ent2.get(), root)).grid(row=4, column=1, sticky='W')
        btn2 = Button(self, text='取消', command=self.quit).grid(row=4, column=2, sticky='W')
        # btn3 = Button(self, text='进入系统', command=lambda: root.show_frame(StartPage)).grid(row=5, column=1, sticky='W')

    def submit(self, e1, e2, root):
        if e1 == 'admin' and e2 == '123456':
            messagebox.showinfo(message='Welcome! admin')
            root.show_frame(StartPage)
        else:
            messagebox.showerror(message='User name or Password is invalid')


#主页
class StartPage(tk.Frame):
    '''主页'''
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text = '员工信息管理系统', font = LARGE_FONT)
        label.pack(pady = 100)
        ft2 = tkFont.Font(size = 16)
        Button(self, text = '增加员工信息', font = ft2, command = lambda:root.show_frame(AddPage),
               width = 30, height = 2, fg = 'white', bg = 'gray', activebackground = 'black', activeforeground = 'white').pack()
        Button(self, text = '删除员工信息', font = ft2, command = lambda:root.show_frame(DeletePage),
               width = 30, height = 2, fg = 'white', bg = 'gray').pack()
        Button(self, text = '修改员工信息', font = ft2, command = lambda:root.show_frame(ModifyPage),
               width = 30, height = 2, fg = 'white', bg = 'gray', activebackground = 'black', activeforeground = 'white').pack()
        Button(self, text= '查询员工信息', font = ft2, command = lambda: root.show_frame(QueryPage),
               width = 30, height = 2, fg = 'white', bg = 'gray', activebackground = 'black', activeforeground = 'white').pack()
        Button(self, text ='退出系统', font = ft2, command = exit,width = 30, height = 2, fg = 'white', bg = 'gray',
               activebackground = 'black', activeforeground = 'white').pack()

#添加员工信息
class AddPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)

        label = tk.Label(self, text = '增加员工信息', font = LARGE_FONT)
        label.pack(pady = 100)
        ft3 = tkFont.Font(size = 14)
        ft4 = tkFont.Font(size = 12)
        Label(self, text = '添加格式：Alex Li,Male,22,13651054608,IT,12000,2013-04-01',font = ft3).pack(side = 'top')
        global e1
        e1 = StringVar()
        Entry(self, width = 45, textvariable = e1, font = ft3, bg = 'Ivory').pack(side = 'top')
        Button(self, text="确定添加", width=8, font=ft4, command=self.add_info).pack(side ='top')
        Button(self, text='返回首页', width=8, font=ft4, command=lambda: root.show_frame(StartPage)).pack(pady=20)

    # 对添加的员工信息进行有效性判断：不允许为空， 不允许有相同的手机号
    def verify_info(self, string):
        employee_lst = []
        if str != '':
            employee_lst = Employee().get_employee_lst()
            for i in range(0, len(employee_lst)):
                if employee_lst[i]['phone'] in string:
                    messagebox.showerror(message='Phone already exists')
                    return False
            return True
        else:
            return False

    # 添加员工信息记录
    def add_info(self):
        count = 0
        string = e1.get()
        if self.verify_info(string):
            count += 1
            f = open(filename, 'a')  # ?有时候在文件行末尾添加，有时候会在文件行末尾换行添加
            f.write('\n' + Employee().get_new_id(filename) + ',' + string)
            f.close()
            Employee().clear_file_blankline(filename)
            content = '已添加: %d 条记录' % count
            t = Text(self)
            t.insert(END,content)
            t.pack(side = 'bottom')
        else:
            messagebox.showerror(message='Please input valid information')

#删除员工信息
class DeletePage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text = '删除员工信息', font = LARGE_FONT)
        label.pack(pady = 100)
        ft3 = tkFont.Font(size = 14)
        ft4 = tkFont.Font(size = 12)
        Label(self, text='请输入要删除的员工号：',font=ft3).pack(side='top')
        global e2
        e2 = StringVar()
        Entry(self, width = 10, textvariable = e2, font=ft3, bg='Ivory').pack(side='top')
        Button(self, text = '确定删除', width=9, font=ft4, command = lambda: self.delete_info(e2.get())).pack(side='top')
        Button(self, text = '返回首页', width = 8, font = ft4, command = lambda: root.show_frame(StartPage)).pack(pady = 20)

    # 删除员工信息记录
    def delete_info(self, id):
        employee_lst = []
        count = 0
        flag = False
        employee_lst = Employee().get_employee_lst()
        for i in range(0, len(employee_lst)):
            if employee_lst[i]['id'] == id:
                employee_lst.pop(i)  # delete specific id of employee info
                flag = True  # id found
                count += 1
                break
            elif (i == len(employee_lst) - 1) and (employee_lst[i]['id'] != id):
                messagebox.showerror(message='the id invalid!')
        content = '已删除: %d 条记录' % count
        t = Text(self)
        t.insert(END, content)
        t.pack(side='bottom')
        while (flag):
            f = open(filename, 'w')
            for j in range(len(employee_lst)):
                la = list(employee_lst[j].values())
                sep = ','
                f.write(sep.join(la) + '\n')
            flag = False
            f.close()
            Employee().clear_file_blankline(filename)

#修改员工信息
class ModifyPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text = '修改员工信息', font = LARGE_FONT)
        label.pack(pady = 100)
        ft3 = tkFont.Font(size = 14)
        ft4 = tkFont.Font(size = 12)
        Button(self, text = '部门名字重命名', width = 20, font = ft3, fg = 'white', bg = 'gray',
               activebackground = 'black', activeforeground = 'white', command=lambda: root.show_frame(ModifyDeptPage)).pack(pady = 30)
        Button(self, text= '修改员工的年龄', width = 20, font = ft3, fg = 'white', bg = 'gray',
               activebackground = 'black', activeforeground = 'white', command=lambda: root.show_frame(ModifyAgePage)).pack(pady = 30)
        Button(self, text = '返回首页', width = 8, font = ft4, command = lambda: root.show_frame(StartPage)).pack(pady = 20)

class ModifyDeptPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text = '部门名字重命名', font = LARGE_FONT)
        label.pack(pady = 100)
        ft3 = tkFont.Font(size = 14)
        ft4 = tkFont.Font(size = 12)
        Label(self, text = '请输入部门名字:',font = ft3).pack(side = 'top')
        global e3
        e3 = StringVar()
        Entry(self, width = 10, textvariable = e3, font = ft3, bg = 'Ivory').pack(side = 'top')
        Label(self, text ='请输入新部门名字:', font = ft3).pack(side = 'top')
        global e4
        e4 = StringVar()
        Entry(self, width = 10, textvariable = e4, font = ft3, bg='Ivory').pack(side = 'top')
        Button(self, text ='确定修改', width = 9, font = ft4, command = lambda: self.update_dept(e3.get(), e4.get())).pack(side = 'top')
        Button(self, text = '返回上一页', width = 10, font = ft4, command = lambda: root.show_frame(ModifyPage)).pack(pady = 20)
    #替换部门的名字
    def update_dept(self, old_dept, new_dept):
        employee_lst = []
        count = 0
        flag = False
        employee_lst = Employee().get_employee_lst()
        for i in range(len(employee_lst)):
            if employee_lst[i]['dept'] == old_dept:
                employee_lst[i]['dept'] = new_dept
                # employee_lst[i]['dept'].replace(old_dept, new_dept)
                count += 1
                flag = True
        content = '已修改: %d 条记录' % count
        t = Text(self)
        t.insert(END, content)
        t.pack(side='bottom')
        while(flag):
            f = open(filename, 'w')
            for j in range(len(employee_lst)):
                la = list(employee_lst[j].values())
                sep = ','
                f.write(sep.join(la) + '\n')
            flag = False
            f.close()
            Employee().clear_file_blankline(filename)


class ModifyAgePage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text = '修改员工年龄', font = LARGE_FONT)
        label.pack(pady = 100)
        ft3 = tkFont.Font(size = 14)
        ft4 = tkFont.Font(size = 12)
        Label(self, text = '输入员工的姓名：',font=ft3).pack(side='top')
        global e5
        e5 = StringVar()
        print(e5.get())
        Entry(self, width = 10, textvariable = e5, font=ft3, bg='Ivory').pack(side='top')
        Label(self, text='请输入修改的年龄：', font = ft3).pack(side='top')
        global e6
        e6 = StringVar()
        print(e6.get())
        Entry(self, width=10, textvariable = e6, font = ft3, bg='Ivory').pack(side='top')
        Button(self, text='确定修改', width = 9, font = ft4, command = lambda: self.update_age_by_name(e5.get(), e6.get())).pack(side='top')
        Button(self, text = '返回上一页', width = 10, font = ft4, command = lambda: root.show_frame(ModifyPage)).pack(pady = 20)

    # 按照员工姓名修改员工的年龄
    def update_age_by_name(self, name, age):
        employee_lst = []
        count = 0
        flag = False
        employee_lst = Employee().get_employee_lst()
        for i in range(len(employee_lst)):
            if employee_lst[i]['name'] == name:
                employee_lst[i]['age'] = age
                # employee_lst[i]['dept'].replace(old_dept, new_dept)
                count += 1
                flag = True
                # print(','.join(list(employee_lst[i].values())))
        content = '已修改: %d 条记录' % count
        t = Text(self)
        t.insert(END, content)
        t.pack(side = 'bottom')
        while (flag):
            f = open(filename, 'w')
            for j in range(len(employee_lst)):
                la = list(employee_lst[j].values())
                sep = ','
                f.write(sep.join(la) + '\n')
            flag = False
            f.close()
            Employee().clear_file_blankline(filename)

class QueryPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text = '员工信息查询', font = LARGE_FONT)
        label.pack(pady = 100)
        ft3 = tkFont.Font(size = 14)
        ft4 = tkFont.Font(size = 12)
        Button(self, text = '员工年龄查询', width = 20, font = ft3, fg = 'white', bg = 'gray',
               activebackground = 'black', activeforeground = 'white', command=lambda: root.show_frame(QueryAgePage)).pack(pady = 30)
        Button(self, text= '员工部门查询', width = 20, font = ft3, fg = 'white', bg = 'gray',
               activebackground = 'black', activeforeground = 'white', command=lambda: root.show_frame(QueryDeptPage)).pack(pady = 30)
        Button(self, text='员工入职年份查询', width=20, font=ft3, fg='white', bg='gray',
               activebackground='black', activeforeground='white', command=lambda: root.show_frame(QueryHireDatePage)).pack(
            pady=30)
        Button(self, text = '返回首页', width = 8, font = ft4, command = lambda: root.show_frame(StartPage)).pack(pady = 20)

class QueryAgePage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text = '员工年龄查询', font = LARGE_FONT)
        label.pack(pady = 100)
        ft3 = tkFont.Font(size = 14)
        ft4 = tkFont.Font(size = 12)
        Label(self, text = '请输入age >：?',font=ft3).pack(side = 'top')
        age = StringVar()
        Entry(self, width = 10, textvariable = age, font = ft3, bg = 'Ivory').pack(side='top')
        Button(self, text = '确定查询', width = 9, font = ft4, command = lambda: self.find_by_age(age.get())).pack(side = 'top')
        Button(self, text = '返回上一页', width = 10, font = ft4, command = lambda: root.show_frame(QueryPage)).pack(pady = 20)

    # 按照年龄查询
    def find_by_age(self, age):
        employee_lst = []
        count = 0
        content = ''
        employee_lst = Employee().get_employee_lst()
        t = Text(self)
        for i in range(len(employee_lst)):
            if int(employee_lst[i]['age']) > int(age):
                count += 1
                # print(','.join(list(employee_lst[i].values())))
                content = ','.join(list(employee_lst[i].values()))
                t.insert(END, content + '\n')

        record = '\n\n查询到: %d 条记录' % count
        t.insert(END, record)
        t.pack(side='bottom')



class QueryDeptPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text = '员工部门查询', font = LARGE_FONT)
        label.pack(pady = 100)
        ft3 = tkFont.Font(size = 14)
        ft4 = tkFont.Font(size = 12)
        Label(self, text = '输入员工所在的部门：',font=ft3).pack(side = 'top')
        Dept = StringVar()
        Entry(self, width = 10, textvariable = Dept, font = ft3, bg = 'Ivory').pack(side='top')
        Button(self, text='确定查询', width=9, font=ft4, command=lambda: self.find_by_dept(Dept.get())).pack(side='top')
        Button(self, text = '返回上一页', width = 10, font = ft4, command = lambda: root.show_frame(QueryPage)).pack(pady = 20)

    # 按照部门查询
    def find_by_dept(self, dept):
        employee_lst = []
        count = 0
        employee_lst = Employee().get_employee_lst()
        t = Text(self)
        for i in range(len(employee_lst)):
            if employee_lst[i]['dept'] == dept:
                count += 1
                content = ','.join(list(employee_lst[i].values()))
                t.insert(END, content + '\n')
        record = '\n\n查询到: %d 条记录' % count
        t.insert(END, record)
        t.pack(side='bottom')


class QueryHireDatePage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text = '员工入职年份查询', font = LARGE_FONT)
        label.pack(pady = 100)
        ft3 = tkFont.Font(size = 14)
        ft4 = tkFont.Font(size = 12)
        Label(self, text = '请输入员工入职的年份:',font = ft3).pack(side = 'top')
        hireDate = StringVar()
        Entry(self, width = 10, textvariable = hireDate, font = ft3, bg = 'Ivory').pack(side='top')
        Button(self, text='确定查询', width=9, font=ft4, command=lambda: self.find_by_hiredate(hireDate.get())).pack(side='top')
        Button(self, text = '返回上一页', width = 10, font = ft4, command = lambda: root.show_frame(QueryPage)).pack(pady = 20)

    # 按照入职年份查询
    def find_by_hiredate(self, hiredate):
        employee_lst = []
        count = 0
        t = Text(self)
        employee_lst = Employee().get_employee_lst()
        for i in range(len(employee_lst)):
            if hiredate in employee_lst[i]['hiredate']:
                count += 1
                content = ','.join(list(employee_lst[i].values()))
                t.insert(END, content + '\n')
        record = '\n\n查询到: %d 条记录' % count
        t.insert(END, record)
        t.pack(side='bottom')

if __name__ == '__main__':
    log = Application()
    log.mainloop()