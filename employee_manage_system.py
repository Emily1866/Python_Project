import os
import string
import sys

filename = 'employee_list.txt'
lst_key = ['id', 'name', 'gender', 'age', 'phone', 'dept', 'salary', 'hiredate']
global login
login = False

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match
        raise StopIteration

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

# 获取文件行数
# def get_filelines(filename):
#     lst = []
#     f = open(filename,'r')
#     for count, line in enumerate(f):
#         pass
#     count += 1
#     f.close()
#     return count

# 获取新入职员工的ID
def clear_file_blankline(filename):
    #method1:delete file blank line
    # with open(filename, 'r+') as f:
    #     # f_lst = list(set(f.readlines()))
    #     f_list = list(f.readlines())
    #     for i in f_list:
    #         if i == '\n':
    #             f_list.remove(i)
    # f.close()
    # with open(filename, 'w+') as f:
    #     f.writelines(f_list)#writelines可以写字典类型的值。
    # f.close()

    #method2:
    with open(filename, 'r+') as f, open('temp.txt', 'w+') as f1:
        f_lst = list(f.readlines())
        for line in f_lst:
            if line == '\n':
                f_lst.remove(line)
        f1.writelines(f_lst)
        f.close()
        f1.close()
        os.remove(filename)#需要把源文件删除
        os.rename('temp.txt', filename)#把temp.txt文件重命名成filename

def get_new_id(filename):
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

#按照年龄查询
def find_by_age(age):
    employee_lst = []
    count = 0
    with open(filename, 'r') as f:
        for line in f:
            lst_value = line.strip('\n').split(',')
            employee = dict(zip(lst_key, lst_value))
            employee_lst.append(employee)
            # file_lines = f.readlines()
            # for lst_value in file_lines:
            #     employee = dict(zip(lst_key, lst_value))
            #     employee_lst.append(employee)
    f.close()
    for i in range(len(employee_lst)):
        if int(employee_lst[i]['age']) > age:
            count += 1
            print(','.join(list(employee_lst[i].values())))
    print('查询到: %d 条记录' % count)

#按照部门查询
def find_by_dept(dept):
    employee_lst = []
    count = 0
    with open(filename, 'r') as f:
        for line in f:
            lst_value = line.strip('\n').split(',')
            employee = dict(zip(lst_key, lst_value))
            employee_lst.append(employee)
            # file_lines = f.readlines()
            # for lst_value in file_lines:
            #     employee = dict(zip(lst_key, lst_value))
            #     employee_lst.append(employee)

    f.close()
    for i in range(len(employee_lst)):
        if employee_lst[i]['dept'] == dept:
            count += 1
            print(','.join(list(employee_lst[i].values())))
    print('查询到: %d 条记录' % count)

#按照入职年份查询
def find_by_hiredate(hiredate):
    employee_lst = []
    count = 0
    with open(filename, 'r') as f:
        for line in f:
            lst_value = line.strip('\n').split(',')
            employee = dict(zip(lst_key, lst_value))
            employee_lst.append(employee)
            # file_lines = f.readlines()
            # for lst_value in file_lines:
            #     employee = dict(zip(lst_key, lst_value))
            #     employee_lst.append(employee)
    f.close()
    for i in range(len(employee_lst)):
        if hiredate in employee_lst[i]['hiredate']:
            count += 1
            print(','.join(list(employee_lst[i].values())))
    print('查询到: %d 条记录' % count)

def find_info():
    print("**==========查询===========**\n")
    print("1、按照员工年龄查询")
    print("2、按照员工部门查询")
    print("3、按照员工入职年份查询")
    print("===============================\n")
    choice = input("请选择：")

    for case in switch(choice):
        if case('1'):
            age = input("age > ")
            find_by_age(int(age))
            break
        if case('2'):
            dept = input("输入员工所在的部门：")
            find_by_dept(dept)
            break
        if case('3'):
            hiredate = input("请输入员工入职的年份:")
            find_by_hiredate(hiredate)
            break
#对添加的员工信息进行有效性判断：不允许为空， 不允许有相同的手机号
def verify_info(str):
    employee_lst = []
    if str != '':
        with open(filename, 'r') as f:
            for line in f:
                lst_value = line.strip('\n').split(',')
                employee = dict(zip(lst_key, lst_value))
                employee_lst.append(employee)

            for i in range(0, len(employee_lst)):
                if employee_lst[i]['phone'] in str:
                    print('Phone already exists')
                    return False
            return True
    else:
        return False

# 添加员工信息记录
def add_info():
    print("**==========添加=================================================**")
    print("添加的内容格式请按照：Alex Li,Male,22,13651054608,IT,12000,2013-04-01")
    print("==================================================================")
    count = 0
    string = input()
    if verify_info(string):
        count += 1
        f = open(filename, 'a')#?有时候在文件行末尾添加，有时候会在文件行末尾换行添加
        f.write('\n'+ get_new_id(filename) + ',' + string)
        f.close()
        clear_file_blankline(filename)
        print('已添加: %d 条记录' % count)
    else:
        print("Please input valid information")

def delete_info():
    print("**==========删除===========**\n")
    id = input("请输入员工号：")
    f = open(filename, 'r')
    employee_lst = []
    count = 0
    flag = False
    for line in f:
        lst_value = line.strip('\n').split(',')
        employee = dict(zip(lst_key, lst_value))
        employee_lst.append(employee)
        # file_lines = f.readlines()
        # for lst_value in file_lines:
        #     employee = dict(zip(lst_key, lst_value))
        #     employee_lst.append(employee)
    for i in range(0, len(employee_lst)):
        if employee_lst[i]['id'] == id:
            employee_lst.pop(i)#delete specific id of employee info
            flag = True# id found
            count += 1
            break
        elif (i == len(employee_lst) - 1) and (employee_lst[i]['id'] != id):
            print("the id invalid!")
    print('已删除: %d 条记录' % count)
    f.close()
    while(flag):
        f = open(filename, 'w')
        for j in range(len(employee_lst)):
            la = list(employee_lst[j].values())
            sep = ','
            f.write(sep.join(la) + '\n')
        flag = False
        f.close()
        clear_file_blankline(filename)

#替换部门的名字
def update_dept(old_dept, new_dept):
    employee_lst = []
    count = 0
    flag = False
    with open(filename, 'r') as f:
        for line in f:
            lst_value = line.strip('\n').split(',')
            employee = dict(zip(lst_key, lst_value))
            employee_lst.append(employee)
            # file_lines = f.readlines()
            # for lst_value in file_lines:
            #     employee = dict(zip(lst_key, lst_value))
            #     employee_lst.append(employee)
    f.close()
    for i in range(len(employee_lst)):
        if employee_lst[i]['dept'] == old_dept:
            employee_lst[i]['dept'] = new_dept
            # employee_lst[i]['dept'].replace(old_dept, new_dept)
            count += 1
            flag = True
            # print(','.join(list(employee_lst[i].values())))
    print('已修改: %d 条记录' % count)
    while(flag):
        f = open(filename, 'w')
        for j in range(len(employee_lst)):
            la = list(employee_lst[j].values())
            sep = ','
            f.write(sep.join(la) + '\n')
        flag = False
        f.close()
        clear_file_blankline(filename)

# 替换部门的名字
def update_age_by_name(age, name):
    employee_lst = []
    count = 0
    flag = False
    with open(filename, 'r') as f:
        for line in f:
            lst_value = line.strip('\n').split(',')
            employee = dict(zip(lst_key, lst_value))
            employee_lst.append(employee)
            # file_lines = f.readlines()
            # for lst_value in file_lines:
            #     employee = dict(zip(lst_key, lst_value))
            #     employee_lst.append(employee)
    f.close()
    for i in range(len(employee_lst)):
        if employee_lst[i]['name'] == name:
            employee_lst[i]['age'] = age
            # employee_lst[i]['dept'].replace(old_dept, new_dept)
            count += 1
            flag = True
            print(','.join(list(employee_lst[i].values())))
    print('已修改: %d 条记录' % count)
    while (flag):
        f = open(filename, 'w')
        for j in range(len(employee_lst)):
            la = list(employee_lst[j].values())
            sep = ','
            f.write(sep.join(la) + '\n')
        flag = False
        f.close()
        clear_file_blankline(filename)

def update_info():
    print("**==========更新===========**\n")
    print("1、部门名字重命名")
    print("2、按照员工姓名修改员工的年龄")
    print("===============================\n")
    choice = input("请选择：")
    for case in switch(choice):
        if case('1'):
            old_dept = input("请输入部门名字：")
            new_dept = input("请输入新的名字：")
            update_dept(old_dept, new_dept)
            break
        if case('2'):
            name = input("输入员工的姓名：")
            age = input("请输入修改的年龄：")
            update_age_by_name(age, name)
            break

def get_admin():
    print("请先登录管理员账户！")
    usr = input("用户名：")
    pwd = input("密码：")
    if usr == 'admin' and pwd == '123456':
        print('Welcome! admin')
        global login
        login = True
    else:
        print('User name or Password is invalid')
        return 0

def employee_management():
    global login
    while(not login):
        get_admin()
    while(login):
       print("===========员工信息表===========\n")
       print("1、增加员工信息")
       print("2、删除员工信息")
       print("3、修改员工信息")
       print("4、查询员工信息")
       print("5、退出")
       print("===============================\n")
       choice = input("请选择：")
       for case in switch(choice):
            if case('1'):
                add_info()
                break
            if case('2'):
                delete_info()
                break
            if case('3'):
                update_info()
                break
            if case('4'):
                find_info()
                break
            if case('5'):
                login = False
                exit()
                break

if __name__ == '__main__':
    print("===========员工信息表===========\n")
    print("1、增加员工信息")
    print("2、删除员工信息")
    print("3、修改员工信息")
    print("4、查询员工信息")
    print("5、退出")
    print("===============================\n")
    input("请选择：")
    employee_management()






