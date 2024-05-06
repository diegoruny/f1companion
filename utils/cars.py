from tkinter import Canvas, PhotoImage, Tk

class Car:
    def __init__(self, canvas, x, y, team, driver_code, image_paths):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.team = team
        self.driver_code = driver_code
        self.image = PhotoImage(file=image_paths[team])
        self.id = canvas.create_image(x, y, image=self.image, anchor='nw')
        image_width = self.image.width()
        image_height = self.image.height()
        # Create text label for driver code
        self.label_id = canvas.create_text(x + image_width / 2, y - 10, text=f'[{driver_code}]', font=('Arial', 12, 'bold'))

    def move_to_starting_line(self, starting_line_x):
        current_x = self.canvas.coords(self.id)[0]
        if current_x < starting_line_x:
            self.canvas.move(self.id, 5, 0)  # Move car right
            # Move the label with the car
            self.canvas.move(self.label_id, 5, 0)

    def move(self, dx, dy):
        # Move the car by dx, dy
        self.x += dx
        self.y += dy
        self.canvas.move(self.id, dx, dy)
        self._check_bounds()

    def _check_bounds(self):
        # Check and adjust car's position if it moves out of canvas bounds
        if self.x < 0:
            self.canvas.delete(self.id)  # Remove car from canvas if it moves past the left edge

