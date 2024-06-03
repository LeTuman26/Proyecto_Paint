import tkinter as tk
from tkinter import filedialog

class PixelArtPaint:
    def __init__(self, root, pixel_size=15, grid_size=30):
        self.root = root
        self.pixel_size = pixel_size  # Dimensiones de cada celda
        self.original_pixel_size = pixel_size  # Guardar el tamaño original de pixel
        self.grid_size = grid_size  # Número de celdas en la cuadrícula
        self.colors = {
            0: "white", 1: "yellow", 2: "cyan", 3: "red",
            4: "#FF8C00", 5: "green", 6: "blue", 7: "purple",
            8: "gray", 9: "black"
        }
        self.selected_color_index = 0
        self.grid_matrix = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Configuración de la ventana
        ancho_ventana = 850
        alto_ventana = 700
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}")
        self.root.resizable(False, False)

        # Configuración del canvas y las barras de desplazamiento
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack()
        self.canvas = tk.Canvas(self.canvas_frame, width=455, height=455, scrollregion=(0, 0, self.pixel_size * self.grid_size, self.pixel_size * self.grid_size))
        self.canvas.pack()
        self.h_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)

        self.canvas.bind("<Button-1>", self.paint)
        self.canvas.bind("<B1-Motion>", self.paint)

        # Creación de las funcionalidades de la interfaz
        # Mostrar los botones en la pantalla
        self.create_grid()
        self.create_color_buttons()
        self.create_print_button()
        self.create_save_button()
        self.create_load_button()
        self.create_zoom_buttons()
        self.create_clear_button()
        self.create_mirror_button()
        self.create_mirror_vertical_button()
        self.alto_contraste_button()
        self.negativo_button()

    def create_grid(self):
        self.canvas.delete("grid")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0 = i * self.pixel_size
                y0 = j * self.pixel_size
                x1 = x0 + self.pixel_size
                y1 = y0 + self.pixel_size
                color = self.colors[self.grid_matrix[j][i]]
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="gray", fill=color, tags="grid")

    def create_color_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        for color_index, color in self.colors.items():
            button = tk.Button(button_frame, bg=color, width=4, height=2, command=lambda index=color_index: self.seleccion_color(index))
            button.grid(row=0, column=color_index)

    def create_print_button(self):
        print_button = tk.Button(self.root, text="Print Matrix", command=self.print_matrix)
        print_button.pack(pady=10)

    def create_save_button(self):
        save_button = tk.Button(self.root, text="Save Matrix", command=self.save_matrix)
        save_button.pack(pady=10)

    def create_load_button(self):
        load_button = tk.Button(self.root, text="Load Matrix", command=self.load_matrix)
        load_button.place(x=50, y=100)

    def create_zoom_buttons(self):
        zoom_frame = tk.Frame(self.root)
        zoom_frame.pack(pady=10)
        zoom_in_button = tk.Button(zoom_frame, text="Zoom In", command=self.zoom_in)
        zoom_in_button.grid(row=0, column=0)
        zoom_out_button = tk.Button(zoom_frame, text="Zoom Out", command=self.zoom_out)
        zoom_out_button.grid(row=0, column=1)

    def create_clear_button(self):
        clear_button = tk.Button(self.root, text="Clear", command=self.clear_canvas)
        clear_button.place(x=50, y=50)  # Asegúrate de que 'pady' no está interfiriendo.

    def create_mirror_button(self):
        mirror_button = tk.Button(self.root, text="Mirror Horizontal", command=self.mirror_colors)
        mirror_button.place(x= 50, y=150)
        
    def create_mirror_vertical_button(self):
        mirror_vertical_button = tk.Button(self.root, text="Mirror Vertical", command=self.mirror_vertical)
        mirror_vertical_button.place(x=50, y=200)

    def alto_contraste_button(self):
        alto_contraste_button = tk.Button(self.root, text="Alto Contraste", command=self.transform_colors)
        alto_contraste_button.place(x=50, y=250)

    def negativo_button(self):
        negativo_button = tk.Button(self.root, text="Negativo", command=self.negativo)
        negativo_button.place(x=50, y=300)

    def seleccion_color(self, color_index):
        self.selected_color_index = color_index
        print(color_index)

    def paint(self, event):
        x = event.x // self.pixel_size
        y = event.y // self.pixel_size
        if x < self.grid_size and y < self.grid_size:
            self.grid_matrix[y][x] = self.selected_color_index
            self.update_color_in_grid(x, y)

    def update_color_in_grid(self, x, y):
        color = self.colors[self.grid_matrix[y][x]]
        x0 = x * self.pixel_size
        y0 = y * self.pixel_size
        x1 = x0 + self.pixel_size
        y1 = y0 + self.pixel_size
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="gray", fill=color)
# Esta función modifica los valores dados en la matriz de forma horizontal para dar un efecto espejo
    def mirror_colors(self):
        new_matrix = [list(reversed(row)) for row in self.grid_matrix]
        self.grid_matrix = new_matrix
        self.create_grid()
        
# Esta función modifica los valores dados en la matriz de forma vertical para dar un efecto espejo
    def mirror_vertical(self):
        new_matrix = list(reversed(self.grid_matrix))
        self.grid_matrix = new_matrix
        self.create_grid()
# Esta función retorna en la terminal la matriz dibujada en la interfaz
    def print_matrix(self):
        for row in self.grid_matrix:
            print(row)
# Esta función trasnforma los colores del 0 al 4 como "0" y del 5 al 9 como "9"
    def transform_colors(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid_matrix[y][x] <= 4:
                    self.grid_matrix[y][x] = 0
                else:
                    self.grid_matrix[y][x] = 9
        self.create_grid()

    def negativo(self):
        color_mapping = {0: 9, 1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1, 9: 0}
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.grid_matrix[y][x] = color_mapping[self.grid_matrix[y][x]]
        self.create_grid()

    def save_matrix(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                for row in self.grid_matrix:
                    file.write(' '.join(map(str, row)) + '\n')
            print(f"Matrix saved to {file_path}")

    def load_matrix(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                y = 0
                for line in file:
                    row = list(map(int, line.strip().split()))
                    x = 0
                    for color_index in row:
                        self.grid_matrix[y][x] = color_index
                        self.update_color_in_grid(x, y)
                        x += 1
                    y += 1
            print(f"Matrix loaded from {file_path}")

    def clear_canvas(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.grid_matrix[y][x] = 0
        self.create_grid()

    def zoom_in(self):
        self.pixel_size *= 2
        self.canvas.config(scrollregion=(0, 0, self.pixel_size * self.grid_size, self.pixel_size * self.grid_size))
        self.create_grid()

    def zoom_out(self):
        self.pixel_size = self.original_pixel_size
        self.canvas.config(scrollregion=(0, 0, self.pixel_size * self.grid_size, self.pixel_size * self.grid_size))
        self.create_grid()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pixel Art")
    app = PixelArtPaint(root)
    root.mainloop()
