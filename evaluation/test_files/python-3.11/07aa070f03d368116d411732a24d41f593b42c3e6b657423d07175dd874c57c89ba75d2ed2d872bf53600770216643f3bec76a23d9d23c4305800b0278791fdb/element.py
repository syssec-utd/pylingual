import math
import numpy as np

def plot_values_deflection(element, factor, linear=False):
    """
    Determine the plotting values for deflection

    :param element: (fem.Element)
    :param factor: (flt) Factor by which to multiply the plotting values perpendicular
                   to the elements axis.
    :param linear: (bool) If True, the bending in between the elements is determined.
    :return: (np.array/ list) x and y values.
    """
    ux1 = element.node_1.ux * factor
    uz1 = -element.node_1.uz * factor
    ux2 = element.node_2.ux * factor
    uz2 = -element.node_2.uz * factor
    x1 = element.vertex_1.x + ux1
    y1 = -element.vertex_1.z + uz1
    x2 = element.vertex_2.x + ux2
    y2 = -element.vertex_2.z + uz2
    if element.type == 'general' and (not linear):
        n = len(element.deflection)
        x_val = np.linspace(x1, x2, n)
        y_val = np.linspace(y1, y2, n)
        x_val = x_val + element.deflection * math.sin(element.angle) * factor
        y_val = y_val + element.deflection * -math.cos(element.angle) * factor
    else:
        x_val = np.array([x1, x2])
        y_val = np.array([y1, y2])
    return (x_val, y_val)

def plot_values_bending_moment(element, factor, n):
    """
    :param element: (object) of the Element class
    :param factor: (float) scaling the plot
    :param n: (integer) amount of x-values
    :return:
    """
    T_left = element.node_1.Ty
    T_right = -element.node_2.Ty
    sin = math.sin(-element.angle)
    cos = math.cos(-element.angle)
    x1 = element.vertex_1.x + T_left * sin * factor
    y1 = -element.vertex_1.z + T_left * cos * factor
    x2 = element.vertex_2.x + T_right * sin * factor
    y2 = -element.vertex_2.z + T_right * cos * factor
    interpolate = np.linspace(0, 1, n)
    dx = x2 - x1
    dy = y2 - y1
    x_val = x1 + interpolate * dx
    y_val = y1 + interpolate * dy
    if element.q_load or element.dead_load:
        qi = element.all_qp_load[0]
        q = element.all_qp_load[1]
        x = interpolate * element.l
        q_part = -((qi - q) / (6 * element.l)) * x ** 3 + qi / 2 * x ** 2 - (2 * qi + q) / 6 * element.l * x
        x_val += sin * q_part * factor
        y_val += cos * q_part * factor
    x_val = np.append(x_val, element.vertex_2.x)
    y_val = np.append(y_val, -element.vertex_2.z)
    x_val = np.insert(x_val, 0, element.vertex_1.x)
    y_val = np.insert(y_val, 0, -element.vertex_1.z)
    return (x_val, y_val)

def plot_values_axial_force(element, factor, n):
    """
    :param element: (object) of the Element class
    :param factor: (float) scaling the plot
    :param n: (integer) amount of x-values
    :return:
    """
    N1 = element.N_1
    N2 = element.N_2
    cos = math.cos(0.5 * math.pi + element.angle)
    sin = math.sin(0.5 * math.pi + element.angle)
    x1 = element.vertex_1.x + N1 * cos * factor
    y1 = -element.vertex_1.z + N1 * sin * factor
    x2 = element.vertex_2.x + N2 * cos * factor
    y2 = -element.vertex_2.z + N2 * sin * factor
    interpolate = np.linspace(0, 1, n)
    dx = x2 - x1
    dy = y2 - y1
    x_val = x1 + interpolate * dx
    y_val = y1 + interpolate * dy
    if element.q_load or element.dead_load:
        qni = element.all_qn_load[0]
        qn = element.all_qn_load[1]
        x = interpolate * element.l
        qn_part = (qn - qni) / (2 * element.l) * (element.l - x) * x
        x_val += cos * qn_part * factor
        y_val += sin * qn_part * factor
    x_val = np.append(x_val, element.vertex_2.x)
    y_val = np.append(y_val, -element.vertex_2.z)
    x_val = np.insert(x_val, 0, element.vertex_1.x)
    y_val = np.insert(y_val, 0, -element.vertex_1.z)
    return (x_val, y_val)

def plot_values_shear_force(element, factor):
    x1 = element.vertex_1.x
    y1 = -element.vertex_1.z
    x2 = element.vertex_2.x
    y2 = -element.vertex_2.z
    n = len(element.shear_force)
    interpolate = np.linspace(0, 1, n)
    dx = x2 - x1
    dy = y2 - y1
    x_val = x1 + interpolate * dx
    y_val = y1 + interpolate * dy
    sin = math.sin(-element.angle)
    cos = math.cos(-element.angle)
    x_val += sin * element.shear_force * factor
    y_val += cos * element.shear_force * factor
    x_val = np.append(x_val, element.vertex_2.x)
    y_val = np.append(y_val, -element.vertex_2.z)
    x_val = np.insert(x_val, 0, element.vertex_1.x)
    y_val = np.insert(y_val, 0, -element.vertex_1.z)
    return (x_val, y_val)

def plot_values_element(element):
    x_val = [element.vertex_1.x, element.vertex_2.x]
    y_val = [-element.vertex_1.z, -element.vertex_2.z]
    return (x_val, y_val)