import tkinter as tk
import pymongo
from library_equation import gui_main_one_dimensional__equation
from writer_plot import WriterPlot
import gui


class Controller:

    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client.test_database

        self.window = tk.Tk()
        self.window.attributes()
        self.my_gui = gui.Gui(self.window, self)
        self.my_gui.master.maxsize(800, 600)
        self.my_gui.pack()
        self.window.mainloop()

    def run(self, *args):
        equation = gui_main_one_dimensional__equation(*args)
        self.my_gui.plot.writer_plot.print_animation(equation)

    def pause_continue(self, *args):
        if self.my_gui.plot.writer_plot.time.dt != 0:
            self.my_gui.plot.writer_plot.time.dt = 0
        else:
            self.my_gui.plot.writer_plot.time.dt = 0.05

    def get_names_saved_equations(self):
        if not self.db.equations:
            return tuple()
        return (element["name"] for element in self.db.equations.find())

    def save(self, name, input_data):
        list_equation = (
            "name",
        )
        equation = {"name": name}
        for key1, value1 in input_data.items():
            equation.update(value1)

        self.db.equations.insert_one(equation)
        self.my_gui.menu_choose_saved.listbox.insert(tk.END, equation["name"])

    def delete_equation(self, name):
        self.db.equations.delete_one({"name": name})
        self.my_gui.menu_choose_saved.listbox.delete("active")

    def insert_equation(self, name):
        equation = self.db.equations.find_one({"name": name})
        self.my_gui.menu.set(equation)

class InputData():
    def __init__(self):
        self.dict = dict()
        self.list = "supporting data", "entry_conditions", "boundary_values"

        list_supporting_data = "type_task", "type_equation"
        self.dict.update({"supporting_data": {e : None for e in list_supporting_data}})

        list_entry_conditions = "coef", "y__x_tzero", "dydt__x_tzero"
        self.dict.update({"entry_conditions": {e : None for e in list_entry_conditions}})

        list_boundary_values = "xeqa", "xeqb", "y__xeqa_t", "y__xeqb_t"
        self.dict.update({"boundary_values": {e : None for e in list_boundary_values}})

    def __getitem__(self, index):
        return self.dict[index]

    def update(self, element):
        self.dict.update(element)

    def get(self, *args):
        result = list()
        for e in args:
            for value in self.dict.values():
                if value.get(e) is not None:
                    result.append(value[e])
                    break
        if len(args) != len(result):
            raise NameError("InputData haven't the element: " + e)
        return result

    def items(self):
        return self.dict.items()


