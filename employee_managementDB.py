'''
release note:
1.采用database的访问方式
'''

import pymysql
from tkinter import *
import tkinter.font as tkFont
import tkinter as tk
from tkinter import messagebox
import os

LARGE_FONT = ("Verdana", 20)
# filename = 'employee_list.txt'
# lst_key = ['id', 'name', 'gender', 'age', 'phone', 'dept', 'salary', 'hiredate']
# '''
# create table
# '''
# def create_table():
#     db = pymysql.connect('localhost', 'root', '123456', 'employeedb')
#     cur = db.cursor()
#     sql = '''create table employee(
#             id char(20),
#             name char(20),
#             gender char(10),
#             age int,
#             phone char(20) not null primary key,
#             dept char(10),
#             salary int,
#             hiredate date
#             )
#         '''
#     cur.execute('Drop table if exists employee_1')
#     cur.execute(sql)
#     db.close()

# '''Generate sql file
# '''
# def make_employee_sql():
#     filename = 'employee_list.txt'
#     employee_sql = 'employee.sql'
#     lst_key = ['id', 'name', 'gender', 'age', 'phone', 'dept', 'salary', 'hiredate']
#     with open(filename, 'r') as f, open(employee_sql, 'w') as f1:
#         for line in f:
#             lst_value = line.strip('\n').split(',')
#             sql_line = 'insert into employee values' + str(tuple(lst_value)) +';\n'
#             f1.writelines(sql_line)
#     f.close()
#     f1.close()


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
        Button(self, text = '查询员工信息', font = ft2, command = lambda: root.show_frame(QueryPage),
               width = 30, height = 2, fg = 'white', bg = 'gray', activebackground = 'black', activeforeground = 'white').pack()
        Button(self, text = '退出系统', font = ft2, command = exit,width = 30, height = 2, fg = 'white', bg = 'gray',
               activebackground = 'black', activeforeground = 'white').pack()

#添加员工信息
class AddPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)

        label = tk.Label(self, text = '增加员工信息', font = LARGE_FONT)
        label.pack(pady = 100)
        ft3 = tkFont.Font(size = 14)
        ft4 = tkFont.Font(size = 12)
        self.t = Text()
        Label(self, text = '添加格式：Alex Li,Male,22,13651054608,IT,12000,2013-04-01',font = ft3).pack(side = 'top')
        global e1
        e1 = StringVar()
        Entry(self, width = 45, textvariable = e1, font = ft3, bg = 'Ivory').pack(side = 'top')
        Button(self, text="确定添加", width=8, font=ft4, command=lambda: self.insert(e1.get())).pack(side ='top')
        Button(self, text='返回首页', width=8, font=ft4, command=lambda: root.show_frame(StartPage)).pack(pady=20)

    # 添加员工信息记录
    '''
    insert record
    '''
    def insert(self, string0):
        db = pymysql.connect('localhost', 'root', '123456', 'employeedb')
        cur = db.cursor()
        string = string0.split(',')
        if len(string) == 7:
            sql = "insert into employee (name, gender, age, phone, dept, salary, hiredate) values(%s,%s,%s,%s,%s,%s,%s)"
            t = Text(self)
            try:
                count = cur.execute(sql, (string[0], string[1], string[2], string[3], string[4], string[5], string[6]))
                db.commit()
                record = '已添加: %d 条记录' % count

                t.insert(END, record)
                t.pack(side='bottom')

            except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,TypeError) as err:
                record = 'Error %s' % err
                t.insert(END, record)
                t.pack(side = 'bottom')
                db.rollback()
            db.close()
        else:
            messagebox.showerror(message='Please input valid information')

    # def back(self, root):
    #     self.t.delete(1.0, END)
    #     self.e1.set('')
    #     root.show_frame(StartPage)



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
        Button(self, text = '确定删除', width=9, font=ft4, command = lambda: self.delete(e2.get())).pack(side='top')
        Button(self, text = '返回首页', width = 8, font = ft4, command = lambda: root.show_frame(StartPage)).pack(pady = 20)

    '''
    delete record
    '''
    def delete(self, id):
        db = pymysql.connect('localhost', 'root', '123456', 'employeedb')
        cur = db.cursor()
        sql = "delete from employee where id = '%s'"
        t = Text(self)

        if id.isdigit():
            try:
                count = cur.execute(sql, int(id))
                db.commit()
                record = '已删除: %d 条记录' % count
                t.insert(END, record)
                t.pack(side='bottom')
            except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,TypeError) as err:
                record = 'Error %s' % err
                t.insert(END, record)
                t.pack(side='bottom')
                db.rollback()
            db.close()
        else:
            messagebox.showerror(message='Please input valid id(0-9)')


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
    '''
    modify info
    '''
    def update_dept(self, old_dept, new_dept):
        db = pymysql.connect('localhost', 'root', '123456', 'employeedb')
        cur = db.cursor()
        t = Text(self)
        sql = "update employee set dept = %s where dept = %s"
        try:
            count = cur.execute(sql, (new_dept,old_dept))
            record = '已修改: %d 条记录' % count
            t.insert(END, record)
            t.pack(side='bottom')
            db.commit()
        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,TypeError) as err:
            record = 'Error %s' % err
            t.insert(END, record)
            t.pack(side='bottom')
            db.rollback()
        db.close()

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
        Entry(self, width = 10, textvariable = e5, font=ft3, bg='Ivory').pack(side='top')
        Label(self, text='请输入修改的年龄：', font = ft3).pack(side='top')
        global e6
        e6 = StringVar()
        Entry(self, width=10, textvariable = e6, font = ft3, bg='Ivory').pack(side='top')
        Button(self, text='确定修改', width = 9, font = ft4, command = lambda: self.update_age_by_name(e6.get(), e5.get())).pack(side='top')
        Button(self, text = '返回上一页', width = 10, font = ft4, command = lambda: root.show_frame(ModifyPage)).pack(pady = 20)

    # 按照员工姓名修改员工的年龄
    def update_age_by_name(self, age, name):
        db = pymysql.connect('localhost', 'root', '123456', 'employeedb')
        cur = db.cursor()
        t = Text(self)
        sql = "update employee set age = %s where name = %s"
        try:
            count = cur.execute(sql, (age, name))
            record = '已修改: %d 条记录' % count
            t.insert(END, record)
            t.pack(side='bottom')
            db.commit()
        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,TypeError) as err:
            record = 'Error %s' % err
            t.insert(END, record)
            t.pack(side='bottom')
            db.rollback()
        db.close()

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
        if age.isdigit():
            db = pymysql.connect('localhost', 'root', '123456', 'employeedb')
            cur = db.cursor()
            sql = " select * from employee where age > '%s' "
            t = Text(self)
            try:
                count = cur.execute(sql, int(age))
                result = list(cur.fetchall())
                for i in range(len(result)):
                    content = ''
                    for j in range(len(result[i])):
                        content += str(result[i][j]) + ','
                    t.insert(END, content[0:-1] + '\n')
                record = '\n\n已查到: %d 条记录' % count
                t.insert(END, record)
                t.pack(side='bottom')
            except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,TypeError) as err:
                record = 'Error %s' % err
                t.insert(END, record)
                t.pack(side='bottom')
                db.rollback()
            db.close()
        else:
            messagebox.showerror(message='Please input valid id(0-9)')


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
        db = pymysql.connect('localhost', 'root', '123456', 'employeedb')
        cur = db.cursor()
        sql = "select * from employee where dept = %s"
        t = Text(self)
        try:
            count = cur.execute(sql, dept)
            result = list(cur.fetchall())
            for i in range(len(result)):
                content = ''
                for j in range(len(result[i])):
                    content += str(result[i][j]) + ','
                t.insert(END, content[0:-1] + '\n')
            record = '\n\n已查到: %d 条记录' % count
            t.insert(END, record)
            t.pack(side='bottom')
        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,TypeError) as err:
            record = 'Error %s' % err
            t.insert(END, record)
            t.pack(side='bottom')
            db.rollback()
        db.close()


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
        db = pymysql.connect('localhost', 'root', '123456', 'employeedb')
        cur = db.cursor()
        sql = " select * from employee where year(hiredate) = %s "
        t = Text(self)
        try:
            count = cur.execute(sql, hiredate)
            result = list(cur.fetchall())
            for i in range(len(result)):
                content = ''
                for j in range(len(result[i])):
                    content += str(result[i][j]) + ','
                t.insert(END, content[0:-1] + '\n')
            record = '\n\n已查到: %d 条记录' % count
            t.insert(END, record)
            t.pack(side='bottom')
        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,TypeError) as err:
            record = 'Error %s' % err
            t.insert(END, record)
            t.pack(side='bottom')
            db.rollback()
        db.close()


if __name__ == '__main__':
    log = Application()
    log.mainloop()





