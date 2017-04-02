"""
File: main.py.

Module provides GUI client for interaction with user tasks,
stored in a relational database.
Db interactions are controlled by module db (File: db.py) through delegation.
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog

import db

password_root = Tk()
password_root.withdraw()
password = simpledialog.askstring("Password", "Enter password:", show="*")
password_root.destroy()

if password is None:
    sys.exit()

db.initialize_db(password)

root = Tk()
root.title("Task Manager")
columns = ("name", "priority", "category", "is_finished")
tree = ttk.Treeview(root, height=36, selectmode="browse", columns=columns, show="headings")
scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.grid(row=0, column=0, rowspan=2)
scrollbar.grid(row=0, column=1, rowspan=2, sticky=(W, N, E, S))


def treeview_sort_column(treeview, column, reverse):
    """Provide sorting on treeview columns."""
    children_list = [(treeview.set(child, column), child) for child in treeview.get_children("")]
    children_list.sort(reverse=reverse)

    for index, (value, child) in enumerate(children_list):
        treeview.move(child, "", index)

    treeview.heading(column, command=lambda: treeview_sort_column(treeview, column, not reverse))


for column in columns:
    tree.heading(column, text=column, command=lambda col=column: treeview_sort_column(tree, col, False))

width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("{0}x{1}+0+0".format(width, height))

width_name = int(width * 0.26)
tree.column("name", width=width_name, anchor="center")
tree.heading("name", text="Name")

width_priority = int(width * 0.06)
tree.column("priority", width=width_priority, anchor="center")
tree.heading("priority", text="Priority")

width_category = int(width * 0.21)
tree.column("category", width=width_category, anchor="center")
tree.heading("category", text="Category")

width_is_finished = int(width * 0.11)
tree.column("is_finished", width=width_is_finished, anchor="center")
tree.heading("is_finished", text="Is Finished")

mainframe = ttk.Frame(root, padding="25 25 100 50")
mainframe.grid(row=0, column=2, sticky=(N, S, W, E))
mainframe.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)

name = StringVar()
ttk.Label(mainframe, text="Name:").grid(column=1, row=1, sticky=(W, E))
name_widget = ttk.Entry(mainframe, width=20, textvariable=name)
name_widget.grid(column=2, row=1, sticky=(W, E))

priority = StringVar()
ttk.Label(mainframe, text="Priority:").grid(column=1, row=2, sticky=(W, E))
priority_widget = ttk.Entry(mainframe, width=20, textvariable=priority)
priority_widget.grid(column=2, row=2, sticky=(W, E))

category = StringVar()
ttk.Label(mainframe, text="Category:").grid(column=1, row=3, sticky=(W, E))
category_widget = ttk.Entry(mainframe, width=20, textvariable=category)
category_widget.grid(column=2, row=3, sticky=(W, E))

is_finished = BooleanVar()
ttk.Label(mainframe, text="Is Finished:").grid(column=1, row=4, sticky=(W, E))
is_finished_widget = ttk.Checkbutton(mainframe, variable=is_finished,
                                     onvalue=True, offvalue=False)
is_finished_widget.grid(column=2, row=4, sticky=(W, E))


def create_item():
    """Handle item creation in db and GUI."""
    name_value = name.get()
    priority_value = priority.get()
    category_value = category.get()
    is_finished_value = is_finished.get()

    if validate_inputs():
        item_values = (name_value,
                       priority_value,
                       category_value,
                       is_finished_value)

        item_id = db.add_task(item_values)

        tree.insert("", "end", item_id, text=item_id, values=(item_values[0],
                                                              item_values[1],
                                                              item_values[2],
                                                              item_values[3]))

        name.set("")
        priority.set("")
        category.set("")
        is_finished.set(False)

        create_button["state"] = "normal"
        change_button["state"] = "disabled"


def validate_inputs():
    """Validate inputs for item creation/editing."""
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


create_button = ttk.Button(mainframe, text="Create Task", command=create_item)
create_button.grid(column=1, row=5, sticky=(W, E))


def change_item():
    """Handle item editing in db and GUI."""
    name_value = name.get()
    priority_value = priority.get()
    category_value = category.get()
    is_finished_value = is_finished.get()

    if validate_inputs():
        item_id = tree.item(tree.selection()[0], "text")
        item_values = (name_value,
                       priority_value,
                       category_value,
                       is_finished_value)

        db.edit_task(item_id, item_values)
        tree.item(tree.selection()[0], values=item_values)

        name.set("")
        priority.set("")
        category.set("")
        is_finished.set(False)

        create_button["state"] = "normal"
        change_button["state"] = "disabled"


change_button = ttk.Button(mainframe, text="Change Task", command=change_item)
change_button.grid(column=2, row=5, sticky=(W, E))
change_button["state"] = "disabled"

for child in mainframe.winfo_children():
    child.grid_configure(padx=25, pady=25)

for item in db.get_tasks():
    tree.insert("", "end", item[0], text=item[0],
                values=(item[1], item[2], item[3], item[4]))

menu = Menu(root, tearoff=0)


def remove_item():
    """Handle item removing in db and GUI."""
    item_id = tree.item(tree.selection()[0], "text")
    db.delete_task(item_id)
    tree.delete(item_id)

    name.set("")
    priority.set("")
    category.set("")
    is_finished.set(False)

    create_button["state"] = "normal"
    change_button["state"] = "disabled"


menu.add_command(label="Remove Task", command=remove_item)


def change_item_helper():
    """Handle form controls for item editing."""
    item_values = tree.item(tree.selection()[0], "values")

    name.set(item_values[0])
    priority.set(item_values[1])
    category.set(item_values[2])
    is_finished.set(item_values[3])

    create_button["state"] = "disabled"
    change_button["state"] = "normal"


menu.add_command(label="Change Task", command=change_item_helper)


def right_click_handler(event):
    """Delegate to function responsible for showing the user contextual menu with further actions."""
    show_contextual_menu(event)


def show_contextual_menu(event):
    """Handle popping of contextual menu."""
    if tree.focus():
        menu.post(event.x + 65, event.y)


tree.bind("<3>", right_click_handler)


def left_click_handler(event):
    """Remove contextual menu."""
    menu.unpost()


tree.bind("<1>", left_click_handler)


def shutdown_hook():
    """Provide hook for root window shutdown event."""
    if messagebox.askyesno(message="Are you sure you want to quit?",
                           icon="question", title="Quit"):
        db.shutdown_db()
        root.destroy()


root.protocol("WM_DELETE_WINDOW", shutdown_hook)

root.mainloop()
