import tkinter as tk
from tkinter import filedialog


class PixelArtPaint:  # la clase para la ventana principal (Y unica ventana)
    def __init__(self, root, pixel_size=15, grid_size=30):
        self.root = root
        self.pixel_size = pixel_size  # Pixel_size es la que define el tamaño de cada celda en la que se pinta
        self.grid_size = grid_size  # Grid_size es la cantidad de celdas a lo largo de cada eje, permite definir cuantas celdas seran
        self.original_pixel_size = pixel_size
        # Lista donde se tiene definido el color segun el numero
        self.colors = {
            0: "white",
            1: "yellow",
            2: "cyan",
            3: "red",
            4: "#FF8C00",
            5: "green",
            6: "blue",
            7: "purple",
            8: "gray",
            9: "black"
        }
        # Color seleccionado
        self.selected_color_index = 0

        # Matriz de la cuadrícula
        self.grid_matrix = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        ancho_ventana = 850  # Ancho de la ventana principal
        alto_ventana = 700  # Alto de la ventana principal
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}")  # Da el tamaño de la ventana
        self.root.resizable(False, False)  # Impide al usuario modificar las dimensiones de la ventana

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack()

        self.canvas = tk.Canvas(self.canvas_frame, width=455, height=455, scrollregion=(0, 0, self.pixel_size * self.grid_size, self.pixel_size * self.grid_size))
        self.canvas.pack()

        self.h_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        #self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        #self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.config(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)

        self.canvas.bind("<Button-1>",
                         self.paint)  # Esta y la siguiente son la configuracion de cuando se da clic con el mouse o si se mantiene presionado
        self.canvas.bind("<B1-Motion>", self.paint)

        self.create_grid()
        self.create_color_buttons()
        self.create_print_button()
        self.create_save_button()
        self.create_load_button()
        self.create_zoom_buttons()

    def create_grid(self):  # Encargada de generar la cuadricula o lienzo para dibujar
        self.canvas.delete("grid")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0 = i * self.pixel_size
                y0 = j * self.pixel_size
                x1 = x0 + self.pixel_size
                y1 = y0 + self.pixel_size
                color = self.colors[self.grid_matrix[j][i]]
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="gray",fill=color, tags="grid")

    def create_color_buttons(self):  # crea primero un frame(un tipo de espacio) para los botones
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        # Esta creara un boton con cada color de la lista con los colores de arriba llamando al metodo seleccion_color
        for color_index, color in self.colors.items():
            button = tk.Button(button_frame, bg=color, width=4, height=2,
                               command=lambda index=color_index: self.seleccion_color(index))
            button.grid(row=0, column=color_index)

    def create_print_button(self):
        print_button = tk.Button(self.root, text="Print Matrix", command=self.print_matrix)
        print_button.pack(pady=10)

    def create_save_button(self):
        save_button = tk.Button(self.root, text="Save Matrix", command=self.save_matrix)
        save_button.pack(pady=10)

    def create_load_button(self):
        load_button = tk.Button(self.root, text="Load Matrix", command=self.load_matrix)
        load_button.place(x=50,y=100)

    def create_zoom_buttons(self):
        zoom_frame = tk.Frame(self.root)
        zoom_frame.pack(pady=10)

        zoom_in_button = tk.Button(zoom_frame, text="Zoom In", command=self.zoom_in)
        zoom_in_button.grid(row=0, column=0)

        zoom_out_button = tk.Button(zoom_frame, text="Zoom Out", command=self.zoom_out)
        zoom_out_button.grid(row=0, column=1)

    def seleccion_color(self, color_index):  # actualiza la variable que guarda el color
        self.selected_color_index = color_index
        print(self.selected_color_index)

    # La siguiente es la funcion para la accion de pintar los cuadros cuando se da clic
    def paint(self, event):
        x = event.x // self.pixel_size
        y = event.y // self.pixel_size

        if x < self.grid_size and y < self.grid_size:
            self.grid_matrix[y][x] = self.selected_color_index
            color = self.colors[self.selected_color_index]
            x0 = x * self.pixel_size
            y0 = y * self.pixel_size
            x1 = x0 + self.pixel_size
            y1 = y0 + self.pixel_size
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="gray", fill=color)

    def print_matrix(self):
        for row in self.grid_matrix:
            print(row)

    def save_matrix(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                for row in self.grid_matrix:
                    file.write(' '.join(map(str, row)) + '\n')
            print(f"Matrix saved to {file_path}")

    def load_matrix(self):
        # Abre un cuadro de diálogo para seleccionar un archivo .txt
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        # Si se selecciona un archivo (file_path no es una cadena vacía)
        if file_path:
            # Abre el archivo en modo lectura
            with open(file_path, 'r') as file:
                # Inicializa el contador de filas
                y = 0
                for line in file:
                    # Convierte la línea en una lista de enteros, dividiendo la línea en sus componentes y mapeando cada uno a un entero
                    row = list(map(int, line.strip().split()))
                    # Inicializa el contador de columnas
                    x = 0
                    for color_index in row:
                        # Actualiza la matriz grid_matrix con el índice del color
                        self.grid_matrix[y][x] = color_index
                        # Obtiene el color correspondiente al índice del diccionario de colores
                        color = self.colors[color_index]
                        # Calcula las coordenadas del rectángulo en el lienzo
                        x0 = x * self.pixel_size
                        y0 = y * self.pixel_size
                        x1 = x0 + self.pixel_size
                        y1 = y0 + self.pixel_size
                        # Dibuja el rectángulo en el lienzo con el color correspondiente
                        self.canvas.create_rectangle(x0, y0, x1, y1, outline="gray", fill=color)
                        # Incrementa el contador de columnas
                        x += 1
                    # Incrementa el contador de filas
                    y += 1
            # Imprime un mensaje en la consola indicando que la matriz se ha cargado desde el archivo
            print(f"Matrix loaded from {file_path}")

    def zoom_in(self):
        self.pixel_size *= 2  # Duplica el tamaño de los píxeles
        self.canvas.config(scrollregion=(0, 0, self.pixel_size * self.grid_size, self.pixel_size * self.grid_size))
        self.create_grid()
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        print(self.pixel_size)

    def zoom_out(self):
        self.pixel_size = self.original_pixel_size  # Restaura el tamaño original de los píxeles
        self.canvas.config(scrollregion=(0, 0, self.pixel_size * self.grid_size, self.pixel_size * self.grid_size))
        self.create_grid()
        self.h_scrollbar.pack_forget()
        self.v_scrollbar.pack_forget()


if __name__ == "__main__":  # Aqui es donde genera la ventana y mantiene el ciclo de la ventana principal
    VentanaPrin = tk.Tk()
    VentanaPrin.title("Pixel Art")
    app = PixelArtPaint(VentanaPrin)
    VentanaPrin.mainloop()