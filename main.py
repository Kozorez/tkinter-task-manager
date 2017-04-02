"""TODO."""

import sys

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog

import db

password_root = Tk()
password_root.withdraw()
password = simpledialog.askstring("Password", "Enter password:", show='*')
password_root.destroy()

if password is None:
    sys.exit()

try:
    db.initialize_db(password)
except:
    print("PASSWORD IS INCORRECT. TRY AGAIN...")
    sys.exit()

root = Tk()
root.title("Task Manager")

width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("{0}x{1}+0+0".format(width, height))

width_name = int(width * 0.26)
width_priority = int(width * 0.06)
width_category = int(width * 0.21)
width_is_finished = int(width * 0.11)


def treeview_sort_column(tv, col, reverse):
    """TODO."""
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


columns = ('name', 'priority', 'category', 'is_finished')
tree = ttk.Treeview(root, height=36, columns=columns, show="headings", selectmode="browse")
for col in columns:
    tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, False))

tree.column('name', width=width_name, anchor='center')
tree.heading('name', text='Name')
tree.column('priority', width=width_priority, anchor='center')
tree.heading('priority', text='Priority')
tree.column('category', width=width_category, anchor='center')
tree.heading('category', text='Category')
tree.column('is_finished', width=width_is_finished, anchor='center')
tree.heading('is_finished', text='Is Finished')

scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

mainframe = ttk.Frame(root, padding="25 25 100 50")
mainframe.grid(row=0, column=2, sticky=(N, S, W, E))
mainframe.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)

name = StringVar()
priority = StringVar()
category = StringVar()
is_finished = BooleanVar()

ttk.Label(mainframe, text='Name:').grid(column=1, row=1, sticky=(W, E))
name_widget = ttk.Entry(mainframe, width=20, textvariable=name)
name_widget.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, text='Priority:').grid(column=1, row=2, sticky=(W, E))
priority_widget = ttk.Entry(mainframe, width=20, textvariable=priority)
priority_widget.grid(column=2, row=2, sticky=(W, E))

ttk.Label(mainframe, text='Category:').grid(column=1, row=3, sticky=(W, E))
category_widget = ttk.Entry(mainframe, width=20, textvariable=category)
category_widget.grid(column=2, row=3, sticky=(W, E))

ttk.Label(mainframe, text='Is Finished:').grid(column=1, row=4, sticky=(W, E))
is_finished_widget = ttk.Checkbutton(mainframe, variable=is_finished, onvalue=True, offvalue=False)
is_finished_widget.grid(column=2, row=4, sticky=(W, E))


def create_item():
    """TODO."""
    name_value = name.get()
    priority_value = priority.get()
    category_value = category.get()
    is_finished_value = is_finished.get()

    if validate_inputs():
        item_values = (name_value, priority_value, category_value, is_finished_value)

        item_id = db.add_task(item_values)

        tree.insert('', 'end', item_id, text=item_id, values=(item_values[0], item_values[1], item_values[2], item_values[3]))

        name.set("")
        priority.set("")
        category.set("")
        is_finished.set('False')

        create_button['state'] = 'normal'
        change_button['state'] = 'disabled'


def change_item():
    """TODO."""
    name_value = name.get()
    priority_value = priority.get()
    category_value = category.get()
    is_finished_value = is_finished.get()

    if validate_inputs():
        item_id = tree.item(tree.selection()[0], "text")
        item_values = (name_value, priority_value, category_value, is_finished_value)
        db.edit_task(str(item_id), item_values)
        tree.item(tree.selection()[0], values=item_values)

        name.set("")
        priority.set("")
        category.set("")
        is_finished.set("")

        create_button['state'] = 'normal'
        change_button['state'] = 'disabled'


create_button = ttk.Button(mainframe, text="Create Task", command=create_item)
create_button.grid(column=1, row=5, sticky=(W, E))

change_button = ttk.Button(mainframe, text="Change Task", command=change_item)
change_button.grid(column=2, row=5, sticky=(W, E))
change_button['state'] = 'disabled'

for child in mainframe.winfo_children():
    child.grid_configure(padx=25, pady=25)

tree.grid(row=0, column=0, rowspan=2)
scrollbar.grid(row=0, column=1, rowspan=2, sticky=(W, N, E, S))

for item in db.get_tasks():
    tree.insert('', 'end', item[0], text=item[0], values=(item[1], item[2], item[3], item[4]))


def remove_item_helper():
    """TODO."""
    item_id = tree.item(tree.selection()[0], "text")
    db.delete_task(str(item_id))
    tree.delete(item_id)


def change_item_helper():
    """TODO."""
    item_values = tree.item(tree.selection()[0], "values")

    name.set(item_values[0])
    priority.set(item_values[1])
    category.set(item_values[2])
    is_finished.set(item_values[3])

    create_button['state'] = 'disabled'
    change_button['state'] = 'normal'


menu = Menu(root, tearoff=0)
menu.add_command(label="Remove Task", command=remove_item_helper)
menu.add_command(label="Change Task", command=change_item_helper)


def right_click_handler(event):
    """TODO."""
    show_contextual_menu(event, item)


tree.bind("<3>", right_click_handler)


def show_contextual_menu(event, item):
    """TODO."""
    if tree.focus():
        menu.post(event.x + 65, event.y)


def left_click_handler(event):
    """TODO."""
    menu.unpost()


tree.bind("<1>", left_click_handler)


def shutdown_hook():
    """TODO."""
    if messagebox.askyesno(message='Are you sure you want to quit?', icon='question', title='Quit'):
        db.shutdown_db()
        root.destroy()


root.protocol("WM_DELETE_WINDOW", shutdown_hook)


def validate_inputs():
    """TODO."""
    name_value = name.get()
    priority_value = priority.get()
    category_value = category.get()

    if not(len(name_value) > 0 and len(name_value) <= 30):
        return False
    if not(int(priority_value) > 0 and int(priority_value) <= 10):
        return False
    if not(len(category_value) > 0 and len(category_value) <= 30):
        return False

    return True


root.mainloop()
