'''
Version edition: V1.00.00
Date:07/27/2018
Author:Emily
'''


# from tkinter import *
#
# root = Tk()
# topString = StringVar()
# topEntry = Entry(root,
#                  width = 17,
#                  textvariable = topString,
#                  background = 'black',
#                  foreground = 'white',
#                  font=('Times New Roman', 40)
#                  )#background = 'black', foreground ='white',# topEntry['width'] = 40
#
#
# topEntry.grid(row = 0, column = 0, columnspan = 4)
#
# buttonCaptions = ['AC', '+/-', '%', '÷', \
#                   '7', '8', '9', '×', \
#                   '4', '5', '6', '-', \
#                   '1', '2', '3', '+', \
#                   '0', 'Exit', '.', '=']
# def edit(caption):
#     topString.set(topString.get() + caption)
#
# buttons = {}
# for i in range(5):
#     for j in range(4):
#         if((i * 4 + j + 1) % 4 == 0):
#             t = Button(root, text = buttonCaptions[i * 4 + j], bg = '#FF8000')
#         else:
#             t = Button(root, text=buttonCaptions[i * 4 + j], bg = '#CCCCCC')
#
#         t['width'] = 15
#         t['command'] = lambda: edit(buttonCaptions[i * 4 + j])
#         t.grid(row = i + 1, column = j)
#         buttons[buttonCaptions[i * 4 + j]] = t
#
# buttons['÷']['command'] = lambda: topString.set(topString.get() + '/')
# buttons['1']['command'] = lambda: topString.set(topString.get() + '1')
# buttons['2']['command'] = lambda: topString.set(topString.get() + '2')
# buttons['3']['command'] = lambda: topString.set(topString.get() + '3')
# buttons['4']['command'] = lambda: topString.set(topString.get() + '4')
# buttons['5']['command'] = lambda: topString.set(topString.get() + '5')
# buttons['6']['command'] = lambda: topString.set(topString.get() + '6')
# buttons['7']['command'] = lambda: topString.set(topString.get() + '7')
# buttons['8']['command'] = lambda: topString.set(topString.get() + '8')
# buttons['9']['command'] = lambda: topString.set(topString.get() + '9')
# buttons['0']['command'] = lambda: topString.set(topString.get() + '0')
# buttons['+']['command'] = lambda: topString.set(topString.get() + '+')
# buttons['-']['command'] = lambda: topString.set(topString.get() + '-')
# buttons['×']['command'] = lambda: topString.set(topString.get() + '*')
# buttons['=']['command'] = lambda: topString.set(topString.get() + '=')
#
# def clear():
#     topString.set('')
#
# buttons['AC']['command'] = clear
#
# def calculate():
#     topString.set(eval(topString.get()))
#
# buttons['=']['command'] = calculate
#
#
#
# root.mainloop()


'''
Version edition: V1.00.01
Date:08/01/2018
Author:Emily

Change list:
    1. using function to define code
'''

from tkinter import *

def frame(side):
    fm = Frame()
    fm.pack(side = side, expand = YES, fill = BOTH)

    return fm

def button(root, side, text, command = None):
    btn = Button(root, text = text, command = command)
    btn.pack(side = side, expand = YES, fill = BOTH)

    return btn

def calculator():

    display = StringVar()
    Entry(textvariable = display, relief = SUNKEN).pack(side = TOP, expand = YES, fill = BOTH)

    for key in ["123", '456', "789", "-0."]:
        fm = frame(TOP)
        for ch in key:
            button(fm, LEFT, ch,
                   lambda d = display, s = '%s'%ch: d.set(d.get() + s))
    fm = frame(TOP)
    for char in '+-*/=':
        if char == '=':
            btn = button(fm, LEFT, char,
                         lambda : display.set(eval(display.get())))
        else:
            btn = button(fm, LEFT, char,
                         lambda s ='%s'%char: display.set(display.get() + s))
    fm = frame(BOTTOM)
    btn = button(fm, LEFT, 'Clr',
                 lambda : display.set(''))

if __name__ == '__main__':

    root = Tk()
    calculator()
    root.mainloop()


