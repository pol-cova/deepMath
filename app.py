import tkinter as tk
import math
import matplotlib.pyplot as plt

app = tk.Tk()
app.geometry('400x400')
app.title('Calculator')

initialVel_var = tk.DoubleVar()
gradAngle_var = tk.DoubleVar()
duckHeight_var = tk.DoubleVar()

# x is the array for the x position
x = []
# y is the array for the y position
y = []
#

def data_process():
    initial_vel = initialVel_var.get()
    grad_angle = gradAngle_var.get()
    duck_height = duckHeight_var.get()

    # Calculus
    g = 9.81
    rad_angle = (grad_angle * math.pi) / 180
    flight_time = (2 * initial_vel * math.sin(rad_angle)) / g
    voy = initial_vel * math.sin(rad_angle)
    hmax = (voy * voy) / (2*g)

    if hmax > duck_height:
        probability = '100%'
        impact_time = (-voy - math.sqrt((voy * voy)-2*g*duck_height))/-g
    else:
        probability = '0%'
        impact_time = 'No existe impacto'

    # i definition
    i = 0
    # calculus of positions
    while i < flight_time:
        x_pos = initial_vel * math.cos(rad_angle) * i
        x.append(i)
        y_pos = (initial_vel * math.sin(rad_angle)*i)-1/2*g*i**2
        y.append(y_pos)
        i = i + 0.01

    vo_user_data_label.config(text=initial_vel)
    angle_user_data_label.config(text=grad_angle)
    duck_user_data_label.config(text=duck_height)
    flight_result_time_label.config(text=flight_time)
    hmax_data_label.config(text=hmax)
    probability_data_label.config(text=probability)
    impact_data_time_label.config(text=impact_time)


def projectile_graph():
    duck_height_y = duckHeight_var.get()
    plt.plot(x, y)
    plt.xlabel('Tiempo de vuelo')
    plt.ylabel('Altura')
    plt.title('Posición de proyectil')
    plt.axhline(y=duck_height_y, color='r', linestyle='-')
    plt.show()
    x.clear()
    y.clear()


# Data forms
vo_label = tk.Label(app, text='Velocidad Inicial', font=('calibre', 10, 'bold'))
vo_entry = tk.Entry(app, textvariable=initialVel_var, font=('calibre', 10, 'normal'))

angle_label = tk.Label(app, text='Ángulo de lanzamiento', font=('calibre', 10, 'bold'))
angle_entry = tk.Entry(app, textvariable=gradAngle_var, font=('calibre', 10, 'normal'))

duck_label = tk.Label(app, text='Altura del vuelo del pato', font=('calibre', 10, 'bold'))
duck_entry = tk.Entry(app, textvariable=duckHeight_var, font=('calibre', 10, 'normal'))

calc_btn = tk.Button(app, text='Calcular', command=data_process)
# Results data
user_data_label = tk.Label(app, text='Datos ingresados', font=('calibre', 12, 'bold'))

vo_user_label = tk.Label(app, text='Velocidad inicial: ', font=('calibre', 10, 'bold'))
vo_user_data_label = tk.Label(app, text='', font=('calibre', 10, 'normal'))

angle_user_label = tk.Label(app, text='Ángulo: ', font=('calibre', 10, 'bold'))
angle_user_data_label = tk.Label(app, text='', font=('calibre', 10, 'normal'))

duck_user_label = tk.Label(app, text='Altura del pato: ', font=('calibre', 10, 'bold'))
duck_user_data_label = tk.Label(app, text='', font=('calibre', 10, 'normal'))

# Results from calculus
results_data_label = tk.Label(app, text='Resultados calculados', font=('calibre', 12, 'bold'))

flight_time_label = tk.Label(app, text='Tiempo de vuelo: (seg) ', font=('calibre', 10, 'bold'))
flight_result_time_label = tk.Label(app, text='', font=('calibre', 10, 'normal'))

hmax_label = tk.Label(app, text='Altura maxima: (mts) ', font=('calibre', 10, 'bold'))
hmax_data_label = tk.Label(app, text='', font=('calibre', 10, 'normal'))

probability_label = tk.Label(app, text='Probabilidad de impacto: ', font=('calibre', 10, 'bold'))
probability_data_label = tk.Label(app, text='', font=('calibre', 10, 'normal'))

impact_time_label = tk.Label(app, text='Tiempo de impacto: (seg) ', font=('calibre', 10, 'bold'))
impact_data_time_label = tk.Label(app, text='', font=('calibre', 10, 'normal'))

# Graph button
graph_btn = tk.Button(app, text='Graficar', command=projectile_graph)

# Form position
vo_label.grid(row=0, column=0)
vo_entry.grid(row=0, column=1)
angle_label.grid(row=1, column=0)
angle_entry.grid(row=1, column=1)
duck_label.grid(row=2, column=0)
duck_entry.grid(row=2, column=1)
calc_btn.grid(row=3, column=1)
user_data_label.grid(row=4, column=1)
vo_user_label.grid(row=5, column=0)
vo_user_data_label.grid(row=5, column=1)
angle_user_label.grid(row=6, column=0)
angle_user_data_label.grid(row=6, column=1)
duck_user_label.grid(row=7, column=0)
duck_user_data_label.grid(row=7, column=1)
results_data_label.grid(row=9, column=1)
flight_time_label.grid(row=10, column=0)
flight_result_time_label.grid(row=10, column=1)
hmax_label.grid(row=11, column=0)
hmax_data_label.grid(row=11, column=1)
probability_label.grid(row=12, column=0)
probability_data_label.grid(row=12, column=1)
impact_time_label.grid(row=13, column=0)
impact_data_time_label.grid(row=13, column=1)
graph_btn.grid(row=15, column=1)


app.mainloop()
