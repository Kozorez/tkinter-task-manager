from tkinter import *
from tkinter import ttk
import data

root = Tk()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

w_id = int(w * 0.04)
w_name = int(w * 0.25)
w_priority = int(w * 0.05)
w_category = int(w * 0.2)
w_is_finished = int(w * 0.1)

tree = ttk.Treeview(root, height=36, columns=('name', 'priority', 'category', 'is_finished'))
tree.column('#0', width=w_id, anchor='center')
tree.heading('#0', text='id')
tree.column('name', width=w_name, anchor='center')
tree.heading('name', text='name')
tree.column('priority', width=w_priority, anchor='center')
tree.heading('priority', text='priority')
tree.column('category', width=w_category, anchor='center')
tree.heading('category', text='category')
tree.column('is_finished', width=w_is_finished, anchor='center')
tree.heading('is_finished', text='is_finished')

s = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=s.set)

###

def calculate1():
    pass

mainframe = ttk.Frame(root, padding="75 0 100 150", relief=SUNKEN)
mainframe.grid(row=0, column=2, sticky=(N, S, W, E))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()

feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Calculate", command=calculate1).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind('<Return>', calculate1)

###

def calculate2():
    pass

mainframe2 = ttk.Frame(root, padding="75 0 100 150", relief=SUNKEN)
mainframe2.grid(row=1, column=2, sticky=(N, S, W, E))
mainframe2.columnconfigure(0, weight=1)
mainframe2.rowconfigure(0, weight=1)

feet2 = StringVar()
meters2 = StringVar()

feet_entry2 = ttk.Entry(mainframe2, width=7, textvariable=feet2)
feet_entry2.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe2, textvariable=meters2).grid(column=2, row=2, sticky=(N, S, W, E))
ttk.Button(mainframe2, text="Calculate", command=calculate2).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe2, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe2, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe2, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe2.winfo_children():
    child.grid_configure(padx=5, pady=5)

feet_entry2.focus()
root.bind('<Return>', calculate2)

###

tree.grid(row=0, column=0, rowspan=2)
s.grid(row=0, column=1, rowspan=2, sticky=["WNES"])


# Inserted at the root, program chooses id:
#tree.insert('', 'end', 'widgets', text='Widget Tour', values=('1', '1', '1', '1'))
# Same thing, but inserted as first child:
#tree.insert('', 0, 'gallery', text='Applications', values=('2', '2', '2', '2'))

#print(data.get_items())

for item in data.get_items():
    tree.insert('', 'end', item[0], text=item[0], values=(item[1], item[2], item[3], item[4]))

global_item = None
global_itemitem = None

def closure():
    data.remove_item(global_item)
    tree.delete(global_item)

def closure_Change():
    data.change_item(global_itemitem)
    #tree.(global_item)

# create a popup menu
menu = Menu(root, tearoff=0)
menu.add_command(label="Remove Task", command = closure)
menu.add_command(label="Change Task", command = closure_Change)

def func(event):
    item = tree.identify('item', event.x, event.y)
    global global_item 
    global_item = item
    print(global_item)


    #curItem = tree.focus()
    #print(tree.item(curItem))
    #print("you clicked on", tree.item(item, "text"))
    popup(event, item)

tree.bind("<3>", func)

def popup(event, item):
    if tree.focus():
        menu.post(event.x + 65, event.y)

def func1(event):
    menu.unpost()

tree.bind("<1>", func1)

root.mainloop()
