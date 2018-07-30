import sys
import math
import numpy
import matplotlib
import scipy
import scipy.integrate
import sympy
import sympy.parsing.sympy_parser
from sympy import abc

from writer_plot import WriterPlot
from all_for_debug import debug_function_print_result, debug_input_file
from reader import input_to_sympy


def gui_main_one_dimensional__heat_equation__task_0(input_data):
    coef, y__x_tzero, external_influences = input_data.get("coef", "y__x_tzero", "external_influences")
    coef, y__x_tzero, external_influences = input_to_sympy(coef, y__x_tzero, external_influences)
    if external_influences:
        return  gui_main_one_dimensional__heat_equation__inhomogeneous(coef, y__x_tzero, external_influences)
    else:
        return gui_main_one_dimensional__heat_equation__homogeneous(coef, y__x_tzero)

def calculate(function):
    return sympy.lambdify((abc.x, abc.t), function)

def gui_main_one_dimensional__heat_equation__homogeneous(coef, y__x_tzero):
    return calculate(one_dimensional__heat_equation__homogeneous(coef, y__x_tzero))


def gui_main_one_dimensional__heat_equation__inhomogeneous(coef, y__x_tzero, external_influences):
    return calculate__one_dimensional__heat_equation__inhomogeneous(coef, y__x_tzero, external_influences)

def one_dimensional__heat_equation__homogeneous(coef, y__x_tzero):
    sqrt_coef = coef ** 0.5
    x, L = sympy.symbols('x L')
    t = sympy.Symbol('t', positive=True)
    function_for_integral = y__x_tzero.subs(x, L)
    first_multiplier = 1 / (2 * sqrt_coef * (sympy.pi * t) ** 0.5)
    test_f = function_for_integral * sympy.exp(-(x - L) ** 2 / (4 * coef * t))
    res = first_multiplier * sympy.integrate(test_f, (L, -sympy.oo, sympy.oo))
    res = sympy.simplify(res)
    res = res.subs(t, sympy.abc.t)
    return res


def calculate__one_dimensional__heat_equation__inhomogeneous(coef, y__x_tzero, external_influences):
    first_augend = one_dimensional__heat_equation__homogeneous(coef, y__x_tzero)
    lambdify_first_augend = sympy.lambdify((abc.x, abc.t), first_augend)

    def function(x_val, t_val):
        x, L = sympy.symbols("x L")
        t, S = sympy.symbols("t S")
        sqrt_coef = coef ** 0.5
        new_external_influences = external_influences.subs([(x, L), (abc.t, S)])
        function_for_integral = 1 / (2 * sqrt_coef * (sympy.pi * (t - S)) ** 0.5) * \
                                new_external_influences * \
                                sympy.exp(-(x - L) ** 2 / (4 * coef * (t - S)))


        lambdify_function_for_integral = sympy.lambdify((S, L, t, x), function_for_integral)

        second_augend, err = scipy.integrate.dblquad(lambdify_function_for_integral,
                                                     -numpy.inf, numpy.inf,
                                                     lambda S: 0, lambda S: t_val,
                                                     args=(t_val, x_val),
                                                     epsabs=0.000001, epsrel=0.000001)
        return second_augend + lambdify_first_augend(x_val, t_val)

    res = numpy.vectorize(function)
    return res

def gui_main_one_dimensional__heat_equation__task_1(input_data):
    input_data_get = input_data.get("coef", "y__x_tzero", "external_influences", "y__xzero_t", "y__xeql_t")
    args = input_to_sympy(*input_data_get)
    return calculate__one_dimensional__heat_equation__task_1(*args)


def calculate__one_dimensional__heat_equation__task_1(coef, y__x_tzero, external_influences, y__xzero_t, y__xeql_t):

    class Task():
        def __init__(self, coef, y__x_tzero, external_influences, y__xzero_t, y__xeql_t):
            self.coef, self.y__x_tzero, self.external_influences, self.y__xzero_t, self.y__xeql_t = \
            coef, y__x_tzero, external_influences, y__xzero_t, y__xeql_t
            self.y__x_tzero = calculate(self.y__x_tzero)
            self.external_influences = calculate(self.external_influences)
            self.y__xzero_t = calculate(self.y__xzero_t)
            self.y__xeql_t = calculate(self.y__xeql_t)
            self.sqrt_coef = coef ** 0.5
            self.y = self.y_next = None

        def function(self, x, t):
            n = len(x) - 1
            dx = x[1] - x[0]
            dt = 0.05
            gamma2 = dt * (1. / dx * self.sqrt_coef) ** 2

            if self.y is None:
                self.y = [0] * (n + 1)
                for i in range(0, n+1):
                    self.y[i] = self.y__x_tzero(x[i], t) + dt * self.external_influences(x[i], t)
                return self.y

            self.y_next = [0] * (n + 1)
            for i in range(1, n):
                self.y_next[i] = self.y[i] + \
                                 gamma2 * (self.y[i + 1] - 2 * self.y[i] + self.y[i - 1]) + \
                                 dt * self.external_influences(x[i], t)

            self.y_next[0] = self.y__xzero_t(x[i], t)
            self.y_next[n] = self.y__xeql_t(x[i], t)

            self.y = self.y_next
            return self.y_next

    res = Task(coef, y__x_tzero, external_influences, y__xzero_t, y__xeql_t).function
    return res


def gui_main_one_dimensional__heat_equation__task_2(input_data):
    pass

def gui_main_one_dimensional__heat_equation__task_3(input_data):
    pass