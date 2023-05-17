import tkinter as tk
from tkinter import messagebox
import customtkinter
import os
from PIL import Image
from ctypes import *
import math
import matplotlib.pyplot as plt
import numpy as np

# Set direction for .so file
open_calc = CDLL('./opencalc.so')

# Set appearance for the main application
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

x_time_piedra = []
y_pos_piedra = []
x_pos_piedra = []
vox_piedra = []
voy_piedra = []

x_time_pato = []
y_pos_pato = []
x_pos_pato = []
v_pato = []
x_pato = []
y_pato = []

# Define epsilon
epsilon = 0.01

# APP class
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Variables declaration

        # Window app presets
        self.title("DeepMath")
        self.geometry(f"{1100} x {580}")

        # Load img
        img_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), "resources")
        self.home_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(img_path, "home_light.png")),
                                               dark_image=Image.open(os.path.join(img_path, "home_light.png")),
                                               size=(20, 20))
        self.calc_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(img_path, "calc_light.png")),
                                               dark_image=Image.open(os.path.join(img_path, "calc_light.png")),
                                               size=(20, 20))
        self.brain_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(img_path, "brain_light.png")),
                                                dark_image=Image.open(os.path.join(img_path, "brain_light.png")),
                                                size=(20, 20))
        self.clean_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(img_path, "clean_light.png")),
                                                dark_image=Image.open(os.path.join(img_path, "clean_light.png")),
                                                size=(20, 20))

        # Set grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        # Sidebar preset
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Sidebar items
        # Logo header
        self.logo_header = customtkinter.CTkLabel(self.sidebar_frame, text="OpenCalc",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_header.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Buttons
        self.home_btn = customtkinter.CTkButton(self.sidebar_frame, height=40, border_spacing=10,
                                                text="Home", fg_color="#1B65A7",
                                                hover_color=("gray70", "gray30"), image=self.home_img, anchor="w",
                                                command=self.return_to_home)
        self.home_btn.grid(row=1, column=0, padx=20, pady=10)
        self.calc_btn = customtkinter.CTkButton(self.sidebar_frame, height=40, border_spacing=10,
                                                text="Calculator", fg_color="#1B65A7",
                                                hover_color=("gray70", "gray30"), image=self.calc_img, anchor="w",
                                                command=self.calculator)
        self.calc_btn.grid(row=2, column=0, padx=20, pady=10)
        self.bot_btn = customtkinter.CTkButton(self.sidebar_frame, height=40, border_spacing=10,
                                               text="Tesseract", fg_color="#1B65A7",
                                               hover_color=("gray70", "gray30"), image=self.brain_img, anchor="w",
                                               command=self.tesseract)
        self.bot_btn.grid(row=3, column=0, padx=20, pady=10)
        self.clean_btn = customtkinter.CTkButton(self.sidebar_frame, height=40, border_spacing=10,
                                                 text="Limpiar cache", fg_color="#1B65A7",
                                                 hover_color=("gray70", "gray30"), image=self.clean_img, anchor="w",
                                                 command=self.clean_cache)
        self.clean_btn.grid(row=4, column=0, padx=20, pady=10)

        # Settings section
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Apariencia: ", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Configuration
        self.config_label = customtkinter.CTkLabel(self.sidebar_frame, text="Configuración", anchor="w")
        self.config_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.config_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                       values=["Global Variables", "Settings", "Credits"],
                                                       command=self.config_menu_event)
        self.config_menu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Calculators frame

        # Calculator case 1
        self.calculator_one_frame = customtkinter.CTkFrame(self)
        self.calculator_one_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.case1_label = customtkinter.CTkLabel(self.calculator_one_frame, text="Caso 1",
                                                  font=customtkinter.CTkFont(size=16, weight="bold"))
        # List of entries of the case
        self.h_pato_label = customtkinter.CTkLabel(self.calculator_one_frame, text="Altura del pato: (mts) ",
                                                   font=customtkinter.CTkFont(size=14, weight="bold"))
        self.h_pato_entry = customtkinter.CTkEntry(self.calculator_one_frame,
                                                   font=customtkinter.CTkFont(size=14, weight="normal"))
        self.h_pato_entry.insert(0, "0.0")
        self.vel_pato_label = customtkinter.CTkLabel(self.calculator_one_frame, text="Velocidad del pato: (m/s)",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        self.vel_pato_entry = customtkinter.CTkEntry(self.calculator_one_frame,
                                                     font=customtkinter.CTkFont(size=14, weight="normal"))
        self.vel_pato_entry.insert(0, "0.0")
        self.velocidad_inicial_label = customtkinter.CTkLabel(self.calculator_one_frame,
                                                              text="Velocidad inicial del proyectil: (m/s) ",
                                                              font=customtkinter.CTkFont(size=14, weight="bold"))
        self.velocidad_inicial_entry = customtkinter.CTkEntry(self.calculator_one_frame,
                                                              font=customtkinter.CTkFont(size=14, weight="normal"))
        self.velocidad_inicial_entry.insert(0, "0.0")
        self.angulo_lanzamiento_label = customtkinter.CTkLabel(self.calculator_one_frame,
                                                               text="Ángulo de lanzamiento del proyectil: (º)",
                                                               font=customtkinter.CTkFont(size=14, weight="bold"))
        self.angulo_lanzamiento_entry = customtkinter.CTkEntry(self.calculator_one_frame,
                                                               font=customtkinter.CTkFont(size=14, weight="normal"))
        self.angulo_lanzamiento_entry.insert(0, "0.0")
        self.data_process_btn = customtkinter.CTkButton(self.calculator_one_frame, height=40, border_spacing=10,
                                                        text="Calcular", fg_color="#1B65A7",
                                                        hover_color=("gray70", "gray30"),
                                                        command=self.case_1_calculator)
        # Grids configurations list
        self.case1_label.grid(row=0, column=0)
        self.h_pato_label.grid(row=1, column=0)
        self.h_pato_entry.grid(row=2, column=0)
        self.vel_pato_label.grid(row=3, column=0)
        self.vel_pato_entry.grid(row=4, column=0)
        self.velocidad_inicial_label.grid(row=5, column=0)
        self.velocidad_inicial_entry.grid(row=6, column=0)
        self.angulo_lanzamiento_label.grid(row=7, column=0)
        self.angulo_lanzamiento_entry.grid(row=8, column=0)
        self.data_process_btn.grid(row=9, column=0, pady=15)

        # Calculator case 2
        self.calculator_two_frame = customtkinter.CTkFrame(self)
        self.calculator_two_frame.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.calculator_case_2_label = customtkinter.CTkLabel(self.calculator_two_frame, text="Caso 2",
                                                              font=customtkinter.CTkFont(size=16, weight="bold"))
        # List of entries of the case
        self.vel_pato_case_2_label = customtkinter.CTkLabel(self.calculator_two_frame,
                                                            text="Velocidad del pato: (m/s) ",
                                                            font=customtkinter.CTkFont(size=14, weight="bold"))
        self.vel_pato_case_2_entry = customtkinter.CTkEntry(self.calculator_two_frame,
                                                            font=customtkinter.CTkFont(size=14, weight="normal"))
        self.vel_pato_case_2_entry.insert(0, "0.0")

        self.h_pato_case_2_label = customtkinter.CTkLabel(self.calculator_two_frame,
                                                          text="Altura de vuelo del pato (mts):  ",
                                                          font=customtkinter.CTkFont(size=14, weight="bold"))
        self.h_pato_case_2_entry = customtkinter.CTkEntry(self.calculator_two_frame,
                                                          font=customtkinter.CTkFont(size=14, weight="normal"))
        self.h_pato_case_2_entry.insert(0, "0.0")

        self.angulo_case_2_label = customtkinter.CTkLabel(self.calculator_two_frame,
                                                          text="Ángulo de lanzamiento (º):  ",
                                                          font=customtkinter.CTkFont(size=14, weight="bold"))
        self.angulo_case_2_entry = customtkinter.CTkEntry(self.calculator_two_frame,
                                                          font=customtkinter.CTkFont(size=14, weight="normal"))
        self.angulo_case_2_entry.insert(0, "0.0")
        self.data_process_btn_2 = customtkinter.CTkButton(self.calculator_two_frame, height=40, border_spacing=10,
                                                          text="Calcular", fg_color="#1B65A7",
                                                          hover_color=("gray70", "gray30"),
                                                          command=self.case_2_calculator)

        # Grid configuration list
        self.calculator_case_2_label.grid(row=0, column=0)
        self.vel_pato_case_2_label.grid(row=1, column=0)
        self.vel_pato_case_2_entry.grid(row=2, column=0)
        self.h_pato_case_2_label.grid(row=3, column=0)
        self.h_pato_case_2_entry.grid(row=4, column=0)
        self.angulo_case_2_label.grid(row=5, column=0)
        self.angulo_case_2_entry.grid(row=6, column=0)
        self.data_process_btn_2.grid(row=7, column=0, pady=15)

        # Calculator case 3
        self.calculator_third_frame = customtkinter.CTkFrame(self)
        self.calculator_third_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.calculator_case_3_label = customtkinter.CTkLabel(self.calculator_third_frame, text="Caso 3",
                                                              font=customtkinter.CTkFont(size=16, weight="bold"))
        # List of entries of the case
        self.vel_pato_case_3_label = customtkinter.CTkLabel(self.calculator_third_frame,
                                                            text="Velocidad del pato: (m/s) ",
                                                            font=customtkinter.CTkFont(size=14, weight="bold"))
        self.vel_pato_case_3_entry = customtkinter.CTkEntry(self.calculator_third_frame,
                                                            font=customtkinter.CTkFont(size=14, weight="normal"))
        self.vel_pato_case_3_entry.insert(0, "0.0")

        self.vel_proy_case_3_label = customtkinter.CTkLabel(self.calculator_third_frame,
                                                            text="Velocidad del proyectil (m/s):  ",
                                                            font=customtkinter.CTkFont(size=14, weight="bold"))
        self.vel_proy_case_3_entry = customtkinter.CTkEntry(self.calculator_third_frame,
                                                            font=customtkinter.CTkFont(size=14, weight="normal"))
        self.vel_proy_case_3_entry.insert(0, "0.0")

        self.angulo_case_3_label = customtkinter.CTkLabel(self.calculator_third_frame,
                                                          text="Ángulo de lanzamiento (º):  ",
                                                          font=customtkinter.CTkFont(size=14, weight="bold"))
        self.angulo_case_3_entry = customtkinter.CTkEntry(self.calculator_third_frame,
                                                          font=customtkinter.CTkFont(size=14, weight="normal"))
        self.angulo_case_3_entry.insert(0, "0.0")
        self.data_process_btn_3 = customtkinter.CTkButton(self.calculator_third_frame, height=40, border_spacing=10,
                                                          text="Calcular", fg_color="#1B65A7",
                                                          hover_color=("gray70", "gray30"),
                                                          command=self.case_3_calculator)

        # Grid configuration list
        self.calculator_case_3_label.grid(row=0, column=0)
        self.vel_pato_case_3_label.grid(row=1, column=0)
        self.vel_pato_case_3_entry.grid(row=2, column=0)
        self.vel_proy_case_3_label.grid(row=3, column=0)
        self.vel_proy_case_3_entry.grid(row=4, column=0)
        self.angulo_case_3_label.grid(row=5, column=0)
        self.angulo_case_3_entry.grid(row=6, column=0)
        self.data_process_btn_3.grid(row=7, column=0, pady=15)

        # Results frame
        self.results_frame = customtkinter.CTkFrame(self)
        self.results_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.results_label = customtkinter.CTkLabel(self.results_frame, text="Resultado de los calculos",
                                                    font=customtkinter.CTkFont(size=16, weight="bold"))
        self.max_h_piedra = customtkinter.CTkLabel(self.results_frame, text="Maxima altura(mts): ",
                                                   font=customtkinter.CTkFont(size=14, weight="bold"))
        self.max_h_piedra_value = customtkinter.CTkLabel(self.results_frame, text="",
                                                         font=customtkinter.CTkFont(size=13, weight="normal"))
        self.max_alcance_piedra = customtkinter.CTkLabel(self.results_frame, text="Maximo alcance(mts): ",
                                                         font=customtkinter.CTkFont(size=14, weight="bold"))
        self.max_alcance_piedra_value = customtkinter.CTkLabel(self.results_frame, text="",
                                                               font=customtkinter.CTkFont(size=13, weight="normal"))
        self.tiempo_vuelo_piedra = customtkinter.CTkLabel(self.results_frame, text="Tiempo de vuelo (seg): ",
                                                          font=customtkinter.CTkFont(size=14, weight="bold"))
        self.tiempo_vuelo_piedra_value = customtkinter.CTkLabel(self.results_frame, text="",
                                                                font=customtkinter.CTkFont(size=13, weight="normal"))
        self.pos_impacto = customtkinter.CTkLabel(self.results_frame, text="Status de  impacto: ",
                                                  font=customtkinter.CTkFont(size=14, weight="bold"))
        self.pos_impacto_value = customtkinter.CTkLabel(self.results_frame, text="",
                                                        font=customtkinter.CTkFont(size=13, weight="normal"))

        # Grid configuration list
        self.results_label.grid(row=0, column=0)
        self.max_h_piedra.grid(row=1, column=0)
        self.max_h_piedra_value.grid(row=2, column=0)
        self.max_alcance_piedra.grid(row=3, column=0)
        self.max_alcance_piedra_value.grid(row=4, column=0)
        self.tiempo_vuelo_piedra.grid(row=5, column=0)
        self.tiempo_vuelo_piedra_value.grid(row=6, column=0)
        self.pos_impacto.grid(row=7, column=0)
        self.pos_impacto_value.grid(row=8, column=0)

        # Inserted data frame
        self.inserted_data_frame = customtkinter.CTkFrame(self)
        self.inserted_data_frame.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.inserted_label = customtkinter.CTkLabel(self.inserted_data_frame, text="Datos ingresados: ",
                                                     font=customtkinter.CTkFont(size=16, weight="bold"))
        self.h_pato_inserted_label = customtkinter.CTkLabel(self.inserted_data_frame, text="Altura de vuelo(mts): ",
                                                            font=customtkinter.CTkFont(size=14, weight="bold"))
        self.h_pato_value_label = customtkinter.CTkLabel(self.inserted_data_frame, text="",
                                                         font=customtkinter.CTkFont(size=13, weight="normal"))
        self.vel_pato_inserted_label = customtkinter.CTkLabel(self.inserted_data_frame,
                                                              text="Velocidad del pato(m/s): ",
                                                              font=customtkinter.CTkFont(size=14, weight="bold"))
        self.vel_pato_value_label = customtkinter.CTkLabel(self.inserted_data_frame, text="",
                                                           font=customtkinter.CTkFont(size=13, weight="normal"))
        self.vel_ini_inserted_label = customtkinter.CTkLabel(self.inserted_data_frame,
                                                             text="Velocidad del proyectil(m/s): ",
                                                             font=customtkinter.CTkFont(size=14, weight="bold"))
        self.vel_ini_value_label = customtkinter.CTkLabel(self.inserted_data_frame, text="",
                                                          font=customtkinter.CTkFont(size=13, weight="normal"))
        self.angle_inserted_label = customtkinter.CTkLabel(self.inserted_data_frame, text="Ángulo de lanzamiento(º): ",
                                                           font=customtkinter.CTkFont(size=14, weight="bold"))
        self.angle_value_label = customtkinter.CTkLabel(self.inserted_data_frame, text="",
                                                        font=customtkinter.CTkFont(size=13, weight="normal"))

        # Grid configuration list
        self.inserted_label.grid(row=0, column=0)
        self.h_pato_inserted_label.grid(row=1, column=0)
        self.h_pato_value_label.grid(row=2, column=0)
        self.vel_pato_inserted_label.grid(row=3, column=0)
        self.vel_pato_value_label.grid(row=4, column=0)
        self.vel_ini_inserted_label.grid(row=5, column=0)
        self.vel_ini_value_label.grid(row=6, column=0)
        self.angle_inserted_label.grid(row=7, column=0)
        self.angle_value_label.grid(row=8, column=0)

        # Graph data frame
        self.graph_data_frame = customtkinter.CTkFrame(self)
        self.graph_data_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.graph_header_label = customtkinter.CTkLabel(self.graph_data_frame, text="Graficas disponibles: ",
                                                         font=customtkinter.CTkFont(size=16, weight="bold"))

        self.graph_btn_1 = customtkinter.CTkButton(self.graph_data_frame, height=40, border_spacing=7,
                                                   text="Grafica de Altura/Tiempo", fg_color="#1B65A7",
                                                   hover_color=("gray70", "gray30"), state="disabled",
                                                   command=self.graph_case_1)

        self.graph_btn_2 = customtkinter.CTkButton(self.graph_data_frame, height=40, border_spacing=7,
                                                   text="Grafica de posición", fg_color="#1B65A7",
                                                   hover_color=("gray70", "gray30"), state="disabled",
                                                   command=self.graph_case_2)

        self.graph_btn_3 = customtkinter.CTkButton(self.graph_data_frame, height=40, border_spacing=7,
                                                   text="Grafica de impacto", fg_color="#1B65A7",
                                                   hover_color=("gray70", "gray30"), state="disabled",
                                                   command=self.graph_case_3)
        self.graph_btn_4 = customtkinter.CTkButton(self.graph_data_frame, height=40, border_spacing=7,
                                                   text="Grafica de velocidad", fg_color="#1B65A7",
                                                   hover_color=("gray70", "gray30"), state="disabled",
                                                   command=self.case_3_calculator)
        # Grid configuration list
        self.graph_header_label.grid(row=0, column=1, padx=5)
        self.graph_btn_1.grid(row=1, column=1, pady=10)
        self.graph_btn_2.grid(row=2, column=1, pady=10)
        self.graph_btn_3.grid(row=3, column=1, pady=10)
        self.graph_btn_4.grid(row=4, column=1, pady=10)

    def return_to_home(self):
        print("Your are redirected to home")

    def calculator(self):
        print("Calculator")

    def tesseract(self):
        print("AI MODEL")

    def case_1_calculator(self):
        velocidad_inicial = self.velocidad_inicial_entry.get()
        velocidad_pato = self.vel_pato_entry.get()
        altura_pato = self.h_pato_entry.get()
        angulo_lanzamiento = self.angulo_lanzamiento_entry.get()

        # Update the labels with the values
        self.h_pato_value_label.configure(text=altura_pato)
        self.vel_pato_value_label.configure(text=velocidad_pato)
        self.vel_ini_value_label.configure(text=velocidad_inicial)
        self.angle_value_label.configure(text=angulo_lanzamiento)

        # Activate btn
        self.graph_btn_1.configure(state="normal")
        self.graph_btn_2.configure(state="normal")
        self.graph_btn_3.configure(state="normal")
        self.graph_btn_4.configure(state="normal")

        # Settings for math calculus-

        velocidad_inicial = float(velocidad_inicial)

        if velocidad_inicial < 0:
            messagebox.showerror(title="DEV ERROR", message="Tu velocidad es negativa prueba otro dato!!!!")
        velocidad_pato = float(velocidad_pato)
        if velocidad_pato < 0:
            messagebox.showerror(title="DEV ERROR", message="Tu velocidad es negativa prueba otro dato!!!!")
        altura_pato = float(altura_pato)
        if altura_pato <= 0:
            messagebox.showerror(title="DEV ERROR", message="Tu altura es menor y/o igual a 0 el pato no vuela!!!!")
        angulo_lanzamiento = float(angulo_lanzamiento)

        initial_velocity = c_float(velocidad_inicial)
        duck_velocity = c_float(velocidad_pato)
        height = c_float(altura_pato)
        angle = np.radians(angulo_lanzamiento)
        rad_angle = c_float(angle)
        g_constant = c_float(9.81)

        # Functions
        maximum_height = open_calc.maximum_height
        maximum_scope = open_calc.maximum_scope
        flight_time = open_calc.flight_time
        impact_height = open_calc.height_3

        # Functions returns types
        maximum_height.restype = c_float
        maximum_scope.restype = c_float
        flight_time.restype = c_float
        impact_height.restype = c_float

        # Functions for calculate
        mh = maximum_height(initial_velocity, rad_angle, g_constant)
        ms = maximum_scope(initial_velocity, rad_angle, g_constant)
        ft = flight_time(initial_velocity, rad_angle, g_constant)
        hi = impact_height(initial_velocity, duck_velocity, rad_angle, g_constant)
        print(hi)

        # Aproximation
        difference = abs(altura_pato-hi)


        # Update the labels with the values
        self.max_h_piedra_value.configure(text=str(mh))
        self.max_alcance_piedra_value.configure(text=str(ms))
        self.tiempo_vuelo_piedra_value.configure(text=str(ft))

        if difference < epsilon:
            self.pos_impacto_value.configure(text="SI HAY IMPACTO!!!")
        else:
            self.pos_impacto_value.configure(text="NO HAY IMPACTO!!!")

        # Graph status
        i = 0
        while i < ft:
            # pos inicial pato
            x_o = (altura_pato / math.tan(angle))
            x_0 = (velocidad_inicial * math.cos(angle) - velocidad_pato) * i

            y_piedra = velocidad_inicial * math.sin(angle) * i - (1 / 2 * 9.81 * i ** 2)
            x_piedra = (velocidad_inicial * math.cos(angle)) * i
            x_pos_pato_1 = x_0 + (velocidad_pato * i)

            # Add positions to array
            x_pos_piedra.append(x_piedra)
            y_pos_piedra.append(y_piedra)
            x_time_piedra.append(i)

            x_time_pato.append(i)
            x_pos_pato.append(x_pos_pato_1)
            y_pos_pato.append(altura_pato)

            i = i + 0.01

        x_pato.append(altura_pato / math.tan(angle))
        y_pato.append(altura_pato)

        if difference < epsilon:
            messagebox.showerror(title='Estatus de impacto',
                                 message='Si impactan consulte los resultados')
        elif altura_pato > hi:
            messagebox.showerror(title='Estatus de impacto',
                                 message='No impactan, el pato vuela más alto que la piedra')
        elif hi > altura_pato:
            messagebox.showerror(title='Estatus de impacto',
                                 message='No impactan, la piedra vuela más alto que el pato')

    def case_2_calculator(self):
        velocidad_pato_2 = self.vel_pato_case_2_entry.get()
        altura_pato_2 = self.h_pato_case_2_entry.get()
        angulo_lanzamiento_2 = self.angulo_case_2_entry.get()

        # Update the labels with the values
        self.h_pato_value_label.configure(text=altura_pato_2)
        self.vel_pato_value_label.configure(text=velocidad_pato_2)
        self.angle_value_label.configure(text=angulo_lanzamiento_2)

        # Activate btn
        self.graph_btn_1.configure(state="normal")
        self.graph_btn_2.configure(state="normal")
        self.graph_btn_3.configure(state="normal")
        self.graph_btn_4.configure(state="normal")

        # Settings for math calculus-

        velocidad_pato = float(velocidad_pato_2)

        if velocidad_pato < 0:
            messagebox.showerror(title="DEV ERROR", message="Tu velocidad es negativa prueba otro dato!!!!")

        altura_pato = float(altura_pato_2)
        if altura_pato <= 0:
            messagebox.showerror(title="DEV ERROR", message="Tu altura es negativa y/o igual a 0 prueba otro dato!!!!")

        angulo_lanzamiento = float(angulo_lanzamiento_2)

        duck_velocity = c_float(velocidad_pato)
        height = c_float(altura_pato)
        angle = np.radians(angulo_lanzamiento)
        rad_angle = c_float(angle)
        g_constant = c_float(9.81)

        # Functions
        maximum_height = open_calc.maximum_height
        maximum_scope = open_calc.maximum_scope
        flight_time = open_calc.flight_time
        impact_height = open_calc.height_3
        velocity_n = open_calc.velocity_2

        # Functions returns types
        maximum_height.restype = c_float
        maximum_scope.restype = c_float
        flight_time.restype = c_float
        impact_height.restype = c_float
        velocity_n.restype = c_float

        # Test
        vn = velocity_n(height, duck_velocity, rad_angle, g_constant)
        messagebox.showinfo(title="Velocidad optima", message=f"La velocidad optima del impacto es {vn} m/s")
        self.vel_ini_value_label.configure(text=str(vn), state="disabled")
        v_ned = c_float(vn)
        # Functions
        mh = maximum_height(v_ned, rad_angle, g_constant)
        ms = maximum_scope(v_ned, rad_angle, g_constant)
        ft = flight_time(v_ned, rad_angle, g_constant)
        hi = impact_height(v_ned, rad_angle, duck_velocity, g_constant)

        # Aproximation
        difference = abs(altura_pato - hi)

        # Update the labels with the values
        self.max_h_piedra_value.configure(text=str(mh))
        self.max_alcance_piedra_value.configure(text=str(ms))
        self.tiempo_vuelo_piedra_value.configure(text=str(ft))
        self.pos_impacto_value.configure(text="IMPACTO INMINENTE")

        # Graph status
        i = 0
        while i < ft:
            # pos inicial pato
            x_o = (altura_pato / math.tan(angle))
            x_0 = (vn * math.cos(angle) - velocidad_pato) * i

            y_piedra = vn * math.sin(angle) * i - (1 / 2 * 9.81 * i ** 2)
            x_piedra = (vn * math.cos(angle)) * i
            x_pos_pato_1 = x_0 + (velocidad_pato * i)

            # Add positions to array
            x_pos_piedra.append(x_piedra)
            y_pos_piedra.append(y_piedra)
            x_time_piedra.append(i)

            x_time_pato.append(i)
            x_pos_pato.append(x_pos_pato_1)
            y_pos_pato.append(altura_pato)

            i = i + 0.01

        x_pato.append(altura_pato / math.tan(angle))
        y_pato.append(altura_pato)

    def case_3_calculator(self):
        velocidad_pato_3 = self.vel_pato_case_3_entry.get()
        velocidad_proy_3 = self.vel_proy_case_3_entry.get()
        angulo_lanzamiento_3 = self.angulo_case_3_entry.get()

        # Update the labels with the values
        self.vel_ini_value_label.configure(text=velocidad_proy_3)
        self.vel_pato_value_label.configure(text=velocidad_pato_3)
        self.angle_value_label.configure(text=angulo_lanzamiento_3)

        # Activate btn
        self.graph_btn_1.configure(state="normal")
        self.graph_btn_2.configure(state="normal")
        self.graph_btn_3.configure(state="normal")
        self.graph_btn_4.configure(state="normal")

        # Settings for math calculus-

        velocidad_pato = float(velocidad_pato_3)

        if velocidad_pato <= 0:
            messagebox.showerror(title="DEV ERROR", message="Tu velocidad es negativa y/o igual a 0 prueba otro dato!!")

        velocidad_proy = float(velocidad_proy_3)
        if velocidad_proy <= 0:
            messagebox.showerror(title="DEV ERROR", message="Tu velocidad es negativa y/o igual a 0 prueba otro dato!!")

        angulo_lanzamiento = float(angulo_lanzamiento_3)

        initial_velocity = c_float(velocidad_proy)
        duck_velocity = c_float(velocidad_pato)
        angle = np.radians(angulo_lanzamiento)
        rad_angle = c_float(angle)
        g_constant = c_float(9.81)

        # Functions
        maximum_height = open_calc.maximum_height
        maximum_scope = open_calc.maximum_scope
        flight_time = open_calc.flight_time
        impact_height = open_calc.height_3
        velocity_n = open_calc.velocity_2

        # Functions returns types
        maximum_height.restype = c_float
        maximum_scope.restype = c_float
        flight_time.restype = c_float
        impact_height.restype = c_float
        velocity_n.restype = c_float

        # Return result
        hi = impact_height(initial_velocity, duck_velocity, rad_angle, g_constant)
        print(hi)

        if hi <= 0:
            messagebox.showerror(title="DEV ERROR", message="Tu altura es negativa y/o igual a 0 prueba otro valor")

        messagebox.showinfo(title="Altura optima", message=f"La altura a la que debe volar el pato es {hi} mts")
        self.h_pato_value_label.configure(text=str(hi), state="disabled")
        v_ned = c_float(hi)
        # Functions
        mh = maximum_height(v_ned, rad_angle, g_constant)
        ms = maximum_scope(v_ned, rad_angle, g_constant)
        ft = flight_time(v_ned, rad_angle, g_constant)
        hi = impact_height(v_ned, rad_angle, duck_velocity, g_constant)

        y = hi
        # Update the labels with the values
        self.max_h_piedra_value.configure(text=str(mh))
        self.max_alcance_piedra_value.configure(text=str(ms))
        self.tiempo_vuelo_piedra_value.configure(text=str(ft))
        self.pos_impacto_value.configure(text="IMPACTO INMINENTE")

        # Graph status
        i = 0
        while i < ft:
            # pos inicial pato
            x_o = (y / math.tan(angle))
            x_0 = (velocidad_proy * math.cos(angle) - velocidad_pato) * i

            y_piedra = velocidad_proy * math.sin(angle) * i - (1 / 2 * 9.81 * i ** 2)
            x_piedra = (velocidad_proy * math.cos(angle)) * i
            x_pos_pato_1 = x_0 + (velocidad_pato * i)

            # Add positions to array
            x_pos_piedra.append(x_piedra)
            y_pos_piedra.append(y_piedra)
            x_time_piedra.append(i)

            x_time_pato.append(i)
            x_pos_pato.append(x_pos_pato_1)
            y_pos_pato.append(y)

            i = i + 0.01

        x_pato.append(y / math.tan(angle))
        y_pato.append(y)

    def clean_cache(self):
        x_time_piedra.clear()
        y_pos_piedra.clear()
        x_pos_piedra.clear()

        x_time_pato.clear()
        y_pos_pato.clear()
        x_pos_pato.clear()

    def graph_case_1(self):

        plt.plot(x_time_piedra, y_pos_piedra, label='Piedra')
        plt.xlabel('Tiempo de vuelo (seg)')
        plt.ylabel('y(t) -> Altura del proyectil')
        plt.title('Altura del proyectil en función del tiempo')
        plt.legend()
        plt.plot()
        plt.show()

    def graph_case_2(self):
        plt.plot(x_pos_piedra, y_pos_piedra, label='Piedra')
        plt.plot(x_pos_pato, y_pos_pato, label='Pato', color="red")
        plt.xlabel('Posición en x ')
        plt.ylabel('y(x) -> Altura del objeto')
        plt.title('Altura del proyectil en función su posición en x')
        plt.legend()
        plt.plot()
        plt.show()

    def graph_case_3(self):
        plt.plot(x_pos_piedra, y_pos_piedra, label='Piedra')
        plt.plot(x_pos_pato, y_pos_pato, label='Pato', color="red")
        plt.plot(x_pato, y_pato, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
        plt.xlabel('Posición en x ')
        plt.ylabel('y(x) -> Altura del proyectil')
        plt.title('Grafica de la posición de los 2 objetos')
        plt.legend()
        plt.plot()
        plt.show()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def config_menu_event(self, user_option: str):
        print(user_option)


if __name__ == '__main__':
    app = App()
    app.mainloop()
