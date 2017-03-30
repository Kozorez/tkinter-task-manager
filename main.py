"""TODO."""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import data

data.initialize_db()

root = Tk()
root.title("Task Manager")

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

w_id = int(w * 0.04)
w_name = int(w * 0.25)
w_priority = int(w * 0.05)
w_category = int(w * 0.2)
w_is_finished = int(w * 0.1)

tree = ttk.Treeview(root, height=36, columns=('name', 'priority', 'category', 'is_finished'))

tree.column('#0', width=w_id, anchor='center')
tree.heading('#0', text='Id')
tree.column('name', width=w_name, anchor='center')
tree.heading('name', text='Name')
tree.column('priority', width=w_priority, anchor='center')
tree.heading('priority', text='Priority')
tree.column('category', width=w_category, anchor='center')
tree.heading('category', text='Category')
tree.column('is_finished', width=w_is_finished, anchor='center')
tree.heading('is_finished', text='Is Finished')

s = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=s.set)

mainframe = ttk.Frame(root, padding="25 25 100 50")
mainframe.grid(row=0, column=2, sticky=(N, S, W, E))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

nameee = StringVar()
priorityee = StringVar()
categoryee = StringVar()
is_finishedee = StringVar()

ttk.Label(mainframe, text='Name:').grid(column=1, row=1, sticky=(W, E))
namee = ttk.Entry(mainframe, width=20, textvariable=nameee)
namee.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, text='Priority:').grid(column=1, row=2, sticky=(W, E))
prioritye = ttk.Entry(mainframe, width=20, textvariable=priorityee)
prioritye.grid(column=2, row=2, sticky=(W, E))

ttk.Label(mainframe, text='Category:').grid(column=1, row=3, sticky=(W, E))
categorye = ttk.Entry(mainframe, width=20, textvariable=categoryee)
categorye.grid(column=2, row=3, sticky=(W, E))

ttk.Label(mainframe, text='Is Finished:').grid(column=1, row=4, sticky=(W, E))
is_finishede = ttk.Checkbutton(mainframe, variable=is_finishedee, onvalue='True', offvalue='False')
is_finishede.grid(column=2, row=4, sticky=(W, E))


def calculate1():
    """TODO."""
    global nameee, priorityee, categoryee, is_finishedee
    ne = nameee.get()
    pe = priorityee.get()
    ce = categoryee.get()
    ie = is_finishedee.get()

    if validate():
        item_text = tree.item(tree.selection()[0], "text")
        item_values = (ne, pe, ce, ie)

        data.change_item(str(item_text), item_values)

        tree.item(tree.selection()[0], values=item_values)

        nameee.set("")
        priorityee.set("")
        categoryee.set("")
        is_finishedee.set("")

        global but
        but['state'] = 'disabled'
        global bt
        bt['state'] = 'normal'


def cr():
    """TODO."""
    global nameee, priorityee, categoryee, is_finishedee
    ne = nameee.get()
    pe = priorityee.get()
    ce = categoryee.get()
    ie = is_finishedee.get()

    if validate():
        item_values = (ne, pe, ce, ie)

        item_text = data.create_item(item_values)

        tree.insert('', 'end', item_text, text=item_text, values=(item_values[0], item_values[1], item_values[2], item_values[3]))

        nameee.set("")
        priorityee.set("")
        categoryee.set("")
        is_finishedee.set("")

        global but
        but['state'] = 'disabled'
        global bt
        bt['state'] = 'normal'


bt = ttk.Button(mainframe, text="Create Task", command=cr)
bt.grid(column=1, row=5, sticky=(W, E))

but = ttk.Button(mainframe, text="Change Task", command=calculate1)
but.grid(column=2, row=5, sticky=(W, E))
but['state'] = 'disabled'

for child in mainframe.winfo_children():
    child.grid_configure(padx=25, pady=25)

tree.grid(row=0, column=0, rowspan=2)
s.grid(row=0, column=1, rowspan=2, sticky=(W, N, E, S))

for item in data.get_items():
    tree.insert('', 'end', item[0], text=item[0], values=(item[1], item[2], item[3], item[4]))


def closure():
    """TODO."""
    item_text = tree.item(tree.selection()[0], "text")
    data.remove_item(str(item_text))
    tree.delete(item_text)


def closure_Change():
    """TODO."""
    global but
    but['state'] = 'normal'
    global bt
    bt['state'] = 'disabled'
    #item_text = tree.item(tree.selection()[0], "text")
    item_values = tree.item(tree.selection()[0], "values")
    #data.change_item(item_text, item_values)
    global nameee, priorityee, categoryee, is_finishedee
    nameee.set(item_values[0])
    priorityee.set(item_values[1])
    categoryee.set(item_values[2])
    is_finishedee.set(item_values[3])


menu = Menu(root, tearoff=0)
menu.add_command(label="Remove Task", command=closure)
menu.add_command(label="Change Task", command=closure_Change)


def func(event):
    """TODO."""
    popup(event, item)


tree.bind("<3>", func)


def popup(event, item):
    """TODO."""
    if tree.focus():
        menu.post(event.x + 65, event.y)


def func1(event):
    """TODO."""
    menu.unpost()


tree.bind("<1>", func1)


def on_closing():
    """TODO."""
    if messagebox.askyesno(message='Are you sure you want to quit?', icon='question', title='Quit'):
        data.shutdown_db()
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)


def validate():
    """TODO."""
    global nameee, priorityee, categoryee
    ne = nameee.get()
    pe = priorityee.get()
    ce = categoryee.get()

    if not(len(ne) > 0 and len(ne) <= 30):
        return False
    if not(int(pe) > 0 and int(pe) <= 10):
        return False
    if not(len(ce) > 0 and len(ce) <= 30):
        return False

    return True


root.mainloop()
