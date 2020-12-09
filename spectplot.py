import matplotlib.pyplot as plt
import colorsys


plt.figure(figsize=(15,9))
plt.grid(True)
plt.xlabel('x, м')
plt.ylabel('y, м')


B = 0.2
e = 1.602176487 * 10**(-19)
m = 9.10938215 * 10**(-31)
c = 299792458
dt = 10**(-12)

# p_min = ((0.5 * 10**6 * e / c)**2 - (m * c)**2)**0.5
# p_max = ((10 * 10**6 * e / c)**2 - (m * c)**2)**0.5

E_min = 0.5 * 10**6
E_max = 10 * 10**6
step_E = (E_max - E_min) / 20

x0 = 0
x_max = 0.002
step_x = x_max / 20
flag = True
while x0 < x_max:
    x0 += step_x
    E = E_min
    print(int(x0 / x_max * 100), '%', sep='')
    while E < E_max:  # просчитываем для электронов с разной начальной энергией

        E += step_E

        p0 = ((E * e / c)**2 + 2 * E * e * m)**0.5

        x = x0
        y = 0
        x_border = 0.15
        y_border = 0.5
        px = 0
        py = p0
        arr_gr = [[], []]
        # print(int((E - E_min) / (E_max - E_min) * 100), '%', sep='')
        while (0 <= x < x_border) and (0 <= y < y_border):
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
