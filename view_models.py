import tkinter as tk
import numpy
import bisect

class DisplayedTime:
    def __init__(self, controller, t, dt):
        self.controller = controller
        self.t = t
        self.view_t = tk.DoubleVar(t)
        self.dt = dt

    def next(self):
        self.t = self.t + self.dt
        self.view_t.set(round(self.t, 1))

    def change_time(self, time):
        self.t = time
        self.update()

    def update(self):
        self.controller.update_view_time()


    def start_value(self):
        self.t = 0


class AnimationPlot:
    def __init__(self):
        self.time_start = 0
        self.time_finish = 100
        self.dt = 0.05

        self.start_x = 0
        self.end_x = 10
        dx = self.get_dx()
        self.num_x = int((self.end_x - self.start_x) / dx)

        self.y = list()
        self.x = numpy.linspace(self.start_x, self.end_x, self.num_x)
        self.t = numpy.linspace(self.time_start, self.time_finish, self.get_num_time_step())

    def get_dx(self):
        return (self.get_dt() * 2) ** 0.5

    def get_dt(self):
        return self.dt
        # return (self.time_finish - self.time_start) / self.num_time_step

    def get_num_time_step(self):
        return int((self.time_finish - self.time_start) / self.dt)

    def clean_result_part(self):
        self.y = list()

    def change_time_finish(self, time_finish):
        self.time_finish = time_finish
        self.t = numpy.linspace(self.time_start, self.time_finish, self.get_num_time_step())

    def get_index_by_time(self, time):
        return bisect.bisect_left(self.t, time)



class ChangerAnimationPlot:
    def __init__(self):
        self.animation_plot = AnimationPlot()

    def start_new(self, input_data):
        self.input_data = input_data
        from library_equation.library_equation import gui_main_one_dimensional__equation
        self.animation_plot = gui_main_one_dimensional__equation(self.animation_plot, input_data)
        return self.animation_plot

    def change_finish_time(self, time_finish):
        self.animation_plot.change_time_finish(time_finish)
        if hasattr(self, "input_data"):
            self.restart()

    def restart(self):
        from library_equation.library_equation import gui_main_one_dimensional__equation
        self.animation_plot = gui_main_one_dimensional__equation(self.animation_plot, self.input_data)
