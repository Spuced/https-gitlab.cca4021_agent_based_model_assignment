import tkinter as tk
import random

# Default Properties
open_space, wall, exit, fire = 0, 1, 2, 3
grid_size = 100

parameters = {}

class SimulationParameters:
    def __init__(self, root):
        self.cell_size_var = tk.IntVar(value=8)
        self.desks_var = tk.BooleanVar(value=True)
        self.door_width_var = tk.IntVar(value=4)
        self.exit_locations_var = tk.StringVar(value="top, bottom, left, right")
        self.panic_percent_var = tk.DoubleVar(value=0.3)
        self.steps_to_check_var = tk.IntVar(value=15)
        self.patience_var = tk.IntVar(value=10)
        self.num_workers_var = tk.IntVar(value=1000)
        self.num_fires_var = tk.IntVar(value=1)
        self.fire_x_var = tk.IntVar(value=random.randint(1, 98))
        self.fire_y_var = tk.IntVar(value=random.randint(1, 98))
        self.fire_spread_var = tk.DoubleVar(value=0.5)

        self.setup_gui(root)

    def setup_gui(self, root):

        # GUI Layout for entering parameters
        tk.Label(app, text="Cell Size").grid(row=0, column=0)
        tk.Entry(app, textvariable=self.cell_size_var).grid(row=0, column=1)

        tk.Label(app, text="Desks (True/False)").grid(row=1, column=0)
        tk.Entry(app, textvariable=self.desks_var).grid(row=1, column=1)

        tk.Label(app, text="Door Width").grid(row=2, column=0)
        tk.Entry(app, textvariable=self.door_width_var).grid(row=2, column=1)

        tk.Label(app, text="Exit Locations (comma separated)").grid(row=3, column=0)
        tk.Entry(app, textvariable=self.exit_locations_var).grid(row=3, column=1)

        tk.Label(app, text="Panic Percent").grid(row=4, column=0)
        tk.Entry(app, textvariable=self.panic_percent_var).grid(row=4, column=1)

        tk.Label(app, text="Steps to Check").grid(row=5, column=0)
        tk.Entry(app, textvariable=self.steps_to_check_var).grid(row=5, column=1)

        tk.Label(app, text="Patience").grid(row=6, column=0)
        tk.Entry(app, textvariable=self.patience_var).grid(row=6, column=1)

        tk.Label(app, text="Number of Workers").grid(row=7, column=0)
        tk.Entry(app, textvariable=self.num_workers_var).grid(row=7, column=1)

        tk.Label(app, text="Number of Fires").grid(row=8, column=0)
        tk.Entry(app, textvariable=num_fires_var).grid(row=8, column=1)

        tk.Label(app, text="Fire X Coordinate").grid(row=9, column=0)
        tk.Entry(app, textvariable=fire_x_var).grid(row=9, column=1)

        tk.Label(app, text="Fire Y Coordinate").grid(row=10, column=0)
        tk.Entry(app, textvariable=fire_y_var).grid(row=10, column=1)

        tk.Label(app, text="Fire Spread").grid(row=11, column=0)
        tk.Entry(app, textvariable=fire_spread_var).grid(row=11, column=1)

        tk.Button(app, text="Submit", command=submit).grid(row=12, columnspan=2)

        app.mainloop()

    def submit(self):
        global parameters
        parameters = {
            "cell_size": self.cell_size_var.get(),
            "desks": self.desks_var.get(),
            # Include other parameters similarly...
            "fire_spread": self.fire_spread_var.get(),
        }
        app.quit()  # Close the GUI window

def run():
    global app
    app = tk.Tk()
    app.title("Simulation Parameters (Close After Submitting)")
    SimulationParameters(app)
    app.mainloop()