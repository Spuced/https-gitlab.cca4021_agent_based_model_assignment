def layout(desks=True, door_width=4, exit_locations=None):
    # Simulation Properties
    open_space = 0
    wall = 1
    exit = 2
    grid_size = 100

    # Grid setup
    grid = [[wall if i == 0 or i == grid_size - 1 or j == 0 or j == grid_size - 1 else open_space for j in range(grid_size)] for i in range(grid_size)]

    # Create the 4 office walls
    for i in range(0, 46):
        for j in [45, 55]:
            grid[i][j] = wall
            grid[j][i] = wall

    for i in range(55, 100):
        for j in [45, 55]:
            grid[i][j] = wall
            grid[j][i] = wall

    # Create the internal doors
    door_positions = [(23, 27), (75, 79)]  # Start and end positions for doors
    for start, end in door_positions:
        for i in range(start, start + door_width):
            for x in [45, 55]:
                grid[x][i] = open_space
                grid[i][x] = open_space

    # Adding desks based on the flag
    if desks:
        for i in range(10, 35):
            for j in range(7, 38, 10):
                grid[i][j] = wall
            for j in range(63, 99, 10):
                grid[i][j] = wall

        for i in range(65, 90):
            for j in range(7, 38, 10):
                grid[i][j] = wall
            for j in range(63, 99, 10):
                grid[i][j] = wall

    # Set the exits based on the exit_locations parameter
    exit_positions = range(49, 52)
    if exit_locations is None:
        exit_locations = ['top', 'bottom', 'left', 'right']

    if 'top' in exit_locations:
        for i in exit_positions:
            grid[0][i] = exit
    if 'bottom' in exit_locations:
        for i in exit_positions:
            grid[99][i] = exit
    if 'left' in exit_locations:
        for i in exit_positions:
            grid[i][0] = exit
    if 'right' in exit_locations:
        for i in exit_positions:
            grid[i][99] = exit

    return grid