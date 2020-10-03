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

epsil = 0.5 * 10**(-3)
dt = 10**(-13)

# p_min = ((0.5 * 10**6 * e / c)**2 - (m * c)**2)**0.5
# p_max = ((10 * 10**6 * e / c)**2 - (m * c)**2)**0.5

E_min = 0.5 * 10**6  # интервал энергий
E_max = 10 * 10**6
step_E = (E_max - E_min) / 80

x0 = 0  # интервал координат
x_max = 0.002
x_border = 0.3
y_border = 0.5

a = 0.05  # интервал углов
alp_min = -a / 2
alp_max = a / 2
step_alp = (alp_max - alp_min) / 20

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

        if ((E * e / c)**2 - (m * c)**2) < 0:  # проверяем, достаточна ли энергия у электрона
            continue
        else:
            p0 = ((E * e / c)**2 - (m * c)**2)**0.5

        x = x0  # выставляем начальные координаты
        y = 0
        px = p0 * sin(alp0)
        py = p0 * cos(alp0)
        arr_gr = [[], []]
        # print(int((E - E_min) / (E_max - E_min) * 100), '%', sep='')
        while (-0.5 <= x < x_border) and (0 <= y < y_border):  # просчитываем траекторию в пределах уст. границ
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

        arr_e.append(arr_gr)  # заносим в массив точек траекторий электронов с одинаковой энергией

        col = (E - E_min) / (E_max - E_min)
        if flag:
            plt.text(x, y, str(round(E * 10 ** (-6), 2)) + "МэВ")

        plt.plot(arr_gr[0], arr_gr[1], color=colorsys.hsv_to_rgb(col, 1, 1), linewidth=0.3)  # строим траекторию
        flag = False

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
