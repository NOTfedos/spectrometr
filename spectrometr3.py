import matplotlib.pyplot as plt
import colorsys
from math import tan, sin, cos, sqrt


plt.figure(figsize=(15, 9))
plt.grid(True)
plt.xlabel('x, м')
plt.ylabel('y, м')


def update_p(px, py, x, y):
    global e, B, m, c, dt

    if (x < 0.04) and (y < 0.15):
        k1_x = e * B * py / sqrt(m * m + (px / c) ** 2 + (py / c) ** 2) * dt
        k1_y = -e * B * px / sqrt(m * m + (px / c) ** 2 + (py / c) ** 2) * dt

        k2_x = e * B * (py + k1_y / 2) / sqrt(m * m + ((px + k1_x / 2) / c) ** 2 + ((py + k1_y / 2) / c) ** 2) * dt
        k2_y = -e * B * (px + k1_x / 2) / sqrt(m * m + ((px + k1_x / 2) / c) ** 2 + ((py + k1_y / 2) / c) ** 2) * dt

        k3_x = e * B * (py + k2_y / 2) / sqrt(m * m + ((px + k2_x / 2) / c) ** 2 + ((py + k2_y / 2) / c) ** 2) * dt
        k3_y = -e * B * (px + k2_x / 2) / sqrt(m * m + ((px + k2_x / 2) / c) ** 2 + ((py + k2_y / 2) / c) ** 2) * dt

        k4_x = e * B * (py + k3_y) / sqrt(m * m + ((px + k3_x) / c) ** 2 + ((py + k3_y) / c) ** 2) * dt
        k4_y = -e * B * (px + k3_x) / sqrt(m * m + ((px + k3_x) / c) ** 2 + ((py + k3_y) / c) ** 2) * dt

        return (k1_x + 2 * (k2_x + k3_x) + k4_x) / 6, (k1_y + 2 * (k2_y + k3_y) + k4_y) / 6
    else:
        return 0, 0


def update_coords(px, py):
    global m, c, dt

    v_x = px / sqrt(m*m + (px/c)**2 + (py/c)**2)
    v_y = py / sqrt(m*m + (px/c)**2 + (py/c)**2)
    v = sqrt(v_x**2 + v_y**2)

    dpx, dpy = update_p(px, py, x, y)
    dp = sqrt(dpx ** 2 + dpy ** 2)
    px += dpx
    py += dpy
    p = sqrt(px**2 + py**2)


    a = dp / dt / (m*v*v/(c*c*(1 - (v/c)**2)**(3/2))  +  m/sqrt(1 - (v/c)**2))

    ax = a * px / p
    ay = a * py / p

    dx = v_x * dt + ax / 2 * dt*dt
    dy = v_y * dt + ay / 2 * dt*dt

    return dx, dy, px, py



FOCUS = True

B = 0.2
e = 1.602176487 * 10**(-19)
m = 9.10938215 * 10**(-31)
c = 299792458

epsil = 5 * 10**(-3)
dt = 10**(-12)

# p_min = ((0.5 * 10**6 * e / c)**2 - (m * c)**2)**0.5
# p_max = ((10 * 10**6 * e / c)**2 - (m * c)**2)**0.5

E_min = 0.5 * 10**6  # интервал энергий
E_max = 10 * 10**6
step_E = (E_max - E_min) / 20

x0 = 0  # интервал координат
x_max = 0.002
x_border = 0.3
y_border = 0.5

a = 0.05  # интервал углов
alp_min = -a / 2
alp_max = a / 2
step_alp = (alp_max - alp_min) / 10

E = E_min
arr_fig = [[], []]  # график точек фокуса

while E < E_max:

    alp0 = alp_min
    flag = True

    arr_e = []

    print(int((E - E_min) / (E_max - E_min) * 100), '% modelling', sep='')
    while alp0 < alp_max:

        alp0 += step_alp

        x0 = x_max / 2 * (1 + tan(alp0) / tan(a / 2))

        p0 = ((E * e / c) ** 2 + 2 * E * e * m) ** 0.5

        x = x0  # выставляем начальные координаты
        y = 0
        px = p0 * sin(alp0)
        py = p0 * cos(alp0)
        arr_gr = [[], []]
        # print(int((E - E_min) / (E_max - E_min) * 100), '%', sep='')
        while (-0.5 <= x < x_border) and (0 <= y < y_border):  # просчитываем траекторию в пределах уст. границ

            dx, dy, px, py = update_coords(px, py)

            x += dx
            y += dy

            # старые вычисления
            # x += vx * dt  # просчитываем координаты
            # y += vy * dt


            # запоминаем точки для графика
            arr_gr[0].append(x)
            arr_gr[1].append(y)


            # если в зоне магнитного поля
            # if (x < 0.04) and (y < 0.15):
            #     '''
            #         старая версия
            #     '''
            #
            #     # dpx_dt = e * v * B * py / p  # находим изменение импульса
            #     # dpy_dt = -e * v * B * px / p
            #     #
            #     # px += dpx_dt * dt  # изменяем импульс
            #     # py += dpy_dt * dt
            #
            #     '''
            #         новая версия
            #     '''
            #
            #     # k1_x = e * B * py / sqrt(m*m + (px/c)**2 + (py/c)**2) * dt
            #     # k1_y = -e * B * px / sqrt(m*m + (px/c)**2 + (py/c)**2) * dt
            #     #
            #     # k2_x = e * B * (py + k1_y/2) / sqrt(m*m + ((px + k1_x/2)/c)**2 + ((py + k1_y/2)/c)**2) * dt
            #     # k2_y = -e * B * (px + k1_x/2) / sqrt(m*m + ((px + k1_x/2) / c) ** 2 + ((py + k1_y/2) / c) ** 2) * dt
            #     #
            #     # k3_x = e * B * (py + k2_y/2) / sqrt(m*m + ((px + k2_x/2)/c)**2 + ((py + k2_y/2)/c)**2) * dt
            #     # k3_y = -e * B * (px + k2_x/2) / sqrt(m*m + ((px + k2_x/2)/c)**2 + ((py + k2_y/2)/c)**2) * dt
            #     #
            #     # k4_x = e * B * (py + k3_y) / sqrt(m*m + ((px + k3_x) / c) ** 2 + ((py + k3_y) / c) ** 2) * dt
            #     # k4_y = -e * B * (px + k3_x) / sqrt(m*m + ((px + k3_x) / c) ** 2 + ((py + k3_y) / c) ** 2) * dt
            #     #
            #     # px += (k1_x + 2*(k2_x + k3_x) + k4_x)/6
            #     # py += (k1_y + 2*(k2_y + k3_y) + k4_y)/6
            #
            #     dpx, dpy = update_p(px, py)
            #     px += dpx
            #     py += dpy


        arr_e.append(arr_gr)  # заносим в массив точек траекторий электронов с одинаковой энергией

        col = (E - E_min) / (E_max - E_min)
        if flag:
            plt.text(x, y, str(round(E * 10 ** (-6), 2)) + "МэВ")

        plt.plot(arr_gr[0], arr_gr[1], color=colorsys.hsv_to_rgb(col, 1, 1), linewidth=0.3)  # строим траекторию
        flag = False


    '''
        отрисовка фокуса
    '''
    if FOCUS:
        x = 0
        x_focus = 0
        min_slope = [1, 0]

        if not arr_e:
            E += step_E
            continue

        min_len = min(map(lambda k: len(k[0]), arr_e))
        while x < x_border:  # проходим по всем координатам X
            print(int((E - E_min) / (E_max - E_min) * 100), '% modelling', sep='', end=' ')
            print(int(x / x_border * 100), '% calc focus', sep='')
            min_y = 1
            max_y = -1
            for func in arr_e:  # перебираем каждую траекторию

                for i in range(min_len):  # перебираем каждую точку
                    xf = func[0][i]
                    if abs(xf - x) < epsil:  # если попадает в эпсилон-окрестность по оси Х
                        if abs(func[1][i]) < epsil:
                            continue
                        min_y = func[1][i] if func[1][i] < min_y else min_y
                        max_y = func[1][i] if func[1][i] > max_y else max_y

            if (max_y - min_y) < (min_slope[0] - min_slope[1]):  # если размах ветвей минимален
                min_slope = [max_y, min_y]  # запоминаем эту координату
                x_focus = x
            x += epsil

        arr_fig[0].append(x_focus)
        arr_fig[1].append((min_slope[0] + min_slope[1]) / 2)

    E += step_E

plt.plot(arr_fig[0], arr_fig[1], color='k', linewidth=2)  # строим график фокусов
plt.show()
