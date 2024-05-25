import tkinter as tk


class PixelArtPaint:
    def __init__(self, root, pixel_size=15, grid_size=30):
        self.root = root
        self.pixel_size = pixel_size
        self.grid_size = grid_size
        self.color = "black"

        self.canvas = tk.Canvas(root, width=self.pixel_size * self.grid_size, height=self.pixel_size * self.grid_size)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.paint)
        self.canvas.bind("<B1-Motion>", self.paint)

        self.create_grid()

    def create_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0 = i * self.pixel_size
                y0 = j * self.pixel_size
                x1 = x0 + self.pixel_size
                y1 = y0 + self.pixel_size
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="gray", fill="white")

    def paint(self, event):
        x = event.x // self.pixel_size * self.pixel_size
        y = event.y // self.pixel_size * self.pixel_size
        self.canvas.create_rectangle(x, y, x + self.pixel_size, y + self.pixel_size, outline="gray", fill=self.color)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pixel Art")
    app = PixelArtPaint(root)
    root.mainloop()
