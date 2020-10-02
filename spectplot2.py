import matplotlib.pyplot as plt
import colorsys
from math import tan, sin, cos


plt.figure(figsize=(15, 9))
plt.grid(True)
plt.xlabel('x, м')
plt.ylabel('y, м')


B = 0.2
e = 1.602176487 * 10**(-19)
m = 9.10938215 * 10**(-31)
c = 299792458

epsil = 10**(-3)
dt = 10**(-14)

# p_min = ((0.5 * 10**6 * e / c)**2 - (m * c)**2)**0.5
# p_max = ((10 * 10**6 * e / c)**2 - (m * c)**2)**0.5

E_min = 0.5 * 10**6
E_max = 10 * 10**6
step_E = (E_max - E_min) / 40
delta = step_E / 3

x0 = 0
x_max = 0.002
step_x = x_max / 20
flag = True

a = 0.05
alp_min = -a / 2
alp_max = a / 2
step_alp = (alp_max - alp_min) / 20

alp0 = alp_min

while alp0 < alp_max:

    x0 = x_max / 2 * (1 + tan(alp0) / tan(a / 2))
    alp0 += step_alp

    E = E_min
    print(int((alp0 - alp_min) / (alp_max - alp_min) * 100), '%', sep='')
    while E < E_max:  # просчитываем для электронов с разной начальной энергией

        E += step_E

        if ((E * e / c)**2 - (m * c)**2) < 0:
            continue
        else:
            p0 = ((E * e / c)**2 - (m * c)**2)**0.5

        x = x0
        y = 0
        x_border = 0.3
        y_border = 0.5
        px = p0 * sin(alp0)
        py = p0 * cos(alp0)
        arr_gr = [[], []]
        # print(int((E - E_min) / (E_max - E_min) * 100), '%', sep='')
        while (-0.5 <= x < x_border) and (0 <= y < y_border):
            p = (px**2 + py**2)**0.5

            vx = px / (m**2 + (p / c)**2)**0.5  # просчитываем скорость
            vy = py / (m**2 + (p / c) ** 2) ** 0.5
            v = (vx**2 + vy**2)**0.5

            x += vx * dt  # просчитываем координаты
            y += vy * dt
            arr_gr[0].append(x)
            arr_gr[1].append(y)

            if (x < 0.04) and (y < 0.15):
                dpx = e * v * B * py / p  # находим изменение импульса
                dpy = -e * v * B * px / p

                px += dpx * dt  # изменяем импульс
                py += dpy * dt

        col = (E - E_min) / (E_max - E_min)
        if flag:
            plt.text(x, y, str(round(E * 10 ** (-6), 2)) + "МэВ")
        plt.plot(arr_gr[0], arr_gr[1], color=colorsys.hsv_to_rgb(col, 1, 1), linewidth=0.3)
    flag = False

plt.show()
