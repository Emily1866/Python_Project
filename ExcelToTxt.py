from tkinter import*
import tkinter.filedialog as filedialog
import xlrd

'''
@Author: Emily
@Date: 07/27/2018
goal:
    针对：上线过程中会遇到bug scope个数很多，上线计划的Excel表格数据无法满足邮件SIT报告的书写格式要求，需要手动输入的问题。
    编写了一个python小脚本，将上线计划各子模块的bug scope范围转成txt格式，以便复制，方便邮件的SIT书写。
    通过UI界面可以选择任意盘符的 上线计划.excel文件，并将上线计划的bug scope输出到SIT.txt文本中。
'''
def get_file_path():
    file_path = filedialog.askopenfilename()

    return file_path

def open_excel():
    try:
        excel_file_path = get_file_path()
        data = xlrd.open_workbook(excel_file_path)

        return data

    except Exception as e:
        print(str(e))

def open_txt():
    try:
        file = open('bugScope.txt', 'w+')

        return file

    except Exception as e:
        print(str(e))

def continuous_num(lst):
    start = 0
    end = start
    str1 = ''
    if(len(lst) == 1) or (len(lst) == 0):
        str1 = str(lst[0])
        return str1
    else:
        for i in range(0, len(lst) - 1):
            if(lst[i + 1] == lst[i] + 1):
                end = i + 1
                if(i == len(lst) - 2):
                    str1 = str1 + str(lst[start]) + '-' + str(lst[end])

            else:
                if(end > start):
                    str1 = str1 + str(lst[start]) + '-' + str(lst[end]) + ','
                elif(end == start):
                    str1 = str1 + str(lst[start]) + ','
                start = end + 1
                end = start
                if(start == len(lst) -1):
                    str1 = str1 + str(lst[start])
        return str1


def handle_excel():
    data = open_excel()
    file = open_txt()
    sh = data.sheet_by_index(2)
    num = 0
    lst = []

    for n in range(0, sh.ncols, 2):  # set step=2
        str1 = ''
        lst.clear()
        for i in range(0, sh.nrows):
            text = sh.cell_value(i, n)

            if isinstance(text, float):
                lst.append(int(text))
                num = num + 1

            elif text == 'Defect ID':
                str1 = ':'

        str1 = sh.cell_value(0, n) + str1
        str2 = str1 + continuous_num(lst)
        center_text.insert(END, str2 +'\n')
        file.write(str2)
        file.write('\n')

    center_text.insert(END, '\nTotal Num:'+ str(num))
    file.close()
    data.unload_sheet(2)#close excel


if __name__ == '__main__':
    # root = Tk()
    leftMaster = Frame()
    leftMaster.pack(side ='left')

    left_label = Label(master = leftMaster, text ='Go-Live Scope:', relief ='ridge', height = 20, width = 15)
    left_label.grid(row = 1, column = 0)

    center_text = Text(master = leftMaster, relief ='sunken', height = 20, width = 100)
    center_text.config(font = ('Times', 11, 'normal'))
    center_text.grid(row = 1, column = 1)

    rightMaster = Frame()
    rightMaster.pack(side = 'right')

    button = Button(master = rightMaster, text = 'Choose file path', command = handle_excel, height = 2, width = 20)
    button.pack()

    mainloop()