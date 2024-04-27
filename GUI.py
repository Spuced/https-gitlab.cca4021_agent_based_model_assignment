import tkinter as tk
import random

# Function to create and run the GUI
def run_gui():
    # Create the main application window
    app = tk.Tk()
    app.title("Simulation Parameters (Close After Submitting)")

    # Variables initialisation with Tkinter
    vars = {
        'cell_size_var': tk.IntVar(value=8),
        'desks_var': tk.BooleanVar(value=True),
        'door_width_var': tk.IntVar(value=4),
        'exit_locations_var': tk.StringVar(value="top, bottom, left, right"),
        'panic_percent_var': tk.DoubleVar(value=0.3),
        'steps_to_check_var': tk.IntVar(value=15),
        'patience_var': tk.IntVar(value=10),
        'num_workers_var': tk.IntVar(value=1000),
        'num_fires_var': tk.IntVar(value=1),
        'fire_x_var': tk.IntVar(value=random.randint(1, 98)),
        'fire_y_var': tk.IntVar(value=random.randint(1, 98)),
        'fire_spread_var': tk.DoubleVar(value=0.5),
        'random_seed_var': tk.IntVar(value=1234)
    }

    # Function to handle the submit button action
    def submit():
        # Retrieve and print values from the GUI (or store them for later use)
        results = {key: var.get() for key, var in vars.items()}
        app.quit()
        return results

    # GUI layout configuration
    for i, (label, var) in enumerate(vars.items()):
        tk.Label(app, text=label.replace("_var", "").capitalize()).grid(row=i, column=0)
        tk.Entry(app, textvariable=var).grid(row=i, column=1)

    # Submit button
    tk.Button(app, text="Submit", command=submit).grid(row=len(vars)+1, columnspan=2)

    # Start the GUI event loop
    app.mainloop()

    # Return the results collected from the GUI
    return {key: var.get() for key, var in vars.items()}