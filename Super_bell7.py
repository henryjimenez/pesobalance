import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as mpimg
import numpy as np

class WeightBalanceCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Peso y Balance - Bell B212")
        self.root.configure(bg='#2e3f4f')
        
        # Crear y ubicar los widgets
        labels = ["Asiento 1 (lbs):", "Asiento 2 (lbs):", "Asiento 3 (lbs):", "Asiento 4 (lbs):",
                  "Asiento 5 (lbs):", "Equipaje Trasero (lbs):", "Carga Externa (lbs):",
                  "Piloto (lbs):", "Carga (lbs):", "Personalizado 1 (lbs):", "Personalizado 2 (lbs):"]
        
        self.entries = []
        for i, label in enumerate(labels):
            lbl = tk.Label(root, text=label, bg='#2e3f4f', fg='#ffffff', font=('Helvetica', 10, 'bold'))
            lbl.grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            entry = tk.Entry(root, bg='#ffffff', fg='#000000', font=('Helvetica', 10))
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries.append(entry)

        calc_button = tk.Button(root, text="Calcular", command=self.calculate, bg='#4CAF50', fg='#ffffff', font=('Helvetica', 12, 'bold'))
        calc_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(root, text="", bg='#2e3f4f', fg='#ffffff', font=('Helvetica', 12, 'bold'))
        self.result_label.grid(row=len(labels)+1, column=0, columnspan=2)

        # Configurar la figura para el gráfico
        self.figure = Figure(figsize=(10, 6), dpi=100, facecolor='#2e3f4f')
        self.ax = self.figure.add_subplot(121, facecolor='#2e3f4f')
        self.ax2 = self.figure.add_subplot(122, facecolor='#2e3f4f')
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=len(labels)+2, padx=10, pady=10)

        # Crear widget de texto para la gráfica ASCII
        self.ascii_text = tk.Text(root, height=10, width=50, bg='#2e3f4f', fg='#ffffff', font=('Courier', 10))
        self.ascii_text.grid(row=len(labels)+2, column=0, columnspan=2, pady=10, padx=10)
        self.ascii_text.insert(tk.END, self.get_ascii_representation([0]*11))  # Inicializar con la estructura vacía

        # Cargar la imagen del helicóptero
 #       self.helicopter_img = mpimg.imread("helicopter.png")
 #       self.helicopter_ax = self.figure.add_axes([0.65, 0.1, 0.3, 0.3], anchor='NE')
 #       self.helicopter_ax.imshow(self.helicopter_img)
 #       self.helicopter_ax.axis('off')

    def calculate(self):
        try:
            # Leer datos de entrada
            weights = [float(entry.get()) if entry.get() else 0 for entry in self.entries]

            # Datos de prueba para los brazos (momentos) de cada entrada
            arms = [150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]

            # Calcular peso total y momento total
            total_weight = sum(weights)
            total_moment = sum(w * a for w, a in zip(weights, arms))

            # Calcular centro de gravedad (CG)
            cg = total_moment / total_weight if total_weight != 0 else 0

            # Mostrar resultados
            result_text = (
                f"Peso total: {total_weight} lbs\n"
                f"Momento total: {total_moment} lbs-in\n"
                f"Centro de gravedad (CG): {cg} in\n"
            )

            # Verificar límites de CG del Bell B212 (ejemplo)
            cg_min = 200.0  # Límite mínimo del CG
            cg_max = 220.0  # Límite máximo del CG
            if cg_min <= cg <= cg_max:
                result_text += "El centro de gravedad está dentro de los límites permitidos."
            else:
                result_text += "El centro de gravedad está fuera de los límites permitidos."

            self.result_label.config(text=result_text)

            # Actualizar el gráfico
            self.update_graph(cg, cg_min, cg_max, total_weight, weights)

            # Actualizar gráfica ASCII
            self.ascii_text.delete(1.0, tk.END)
            self.ascii_text.insert(tk.END, self.get_ascii_representation(weights))

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

    def update_graph(self, cg, cg_min, cg_max, total_weight, weights):
        self.ax.clear()
        self.ax.axvline(cg_min, color='r', linestyle='--', label='CG Min')
        self.ax.axvline(cg_max, color='r', linestyle='--', label='CG Max')
        self.ax.axvline(cg, color='b', linestyle='-', label='CG Actual')
        self.ax.set_xlim(cg_min - 20, cg_max + 20)
        self.ax.set_ylim(0, 1)
        self.ax.set_xlabel('Centro de Gravedad (in)', color='#ffffff')
        self.ax.set_yticks([])
        self.ax.legend(facecolor='#2e3f4f', edgecolor='#ffffff')

        # Mostrar imagen del helicóptero en la segunda gráfica
        self.ax2.clear()
        y_pos = np.arange(len(weights))
        self.ax2.barh(y_pos, weights, align='center', color='#4CAF50')
        self.ax2.set_yticks(y_pos)
        self.ax2.set_yticklabels(['Asiento 1', 'Asiento 2', 'Asiento 3', 'Asiento 4', 'Asiento 5', 'Equipaje Trasero',
                                  'Carga Externa', 'Piloto', 'Carga', 'Personalizado 1', 'Personalizado 2'])
        self.ax2.invert_yaxis()  # Invertir el eje y para tener la primera barra en la parte superior
        self.ax2.set_xlabel('Peso (lbs)', color='#ffffff')
        self.ax2.set_facecolor('#2e3f4f')
        self.ax2.tick_params(axis='x', colors='#ffffff')
        self.ax2.tick_params(axis='y', colors='#ffffff')

        self.canvas.draw()

    def get_ascii_representation(self, weights):
        ascii_representation = (
            "-------------------------------\n"
            "|     |           |           |\n"
            f"|  P  |  A1: {weights[0]:>3}   |  A2: {weights[1]:>3}   |\n"
            "|     |           |           |\n"
            "|-----|-----------|-----------|\n"
            "|     |           |           |\n"
            f"|  C  |  A3: {weights[2]:>3}   |  A4: {weights[3]:>3}   |\n"
            "|     |           |           |\n"
            "|-----|-----------|-----------|\n"
            "|     |           |           |\n"
            f"|  C  |  A5: {weights[4]:>3}   |  E:  {weights[5]:>3}   |\n"
            "|     |           |           |\n"
            "|-----------------------------|\n"
            f"|  Piloto: {weights[7]:>3}     Carga: {weights[8]:>3}   |\n"
            "|-----------------------------|\n"
            f"| Pers 1: {weights[9]:>3}     Pers 2: {weights[10]:>3}  |\n"
            "-------------------------------\n"
        )
        return ascii_representation

if __name__ == "__main__":
    root = tk.Tk()
    app = WeightBalanceCalculator(root)
    root.mainloop()
