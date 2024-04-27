def layout():

	# Simulation Properties
	open_space = 0
	wall = 1
	exit = 2
	grid_size = 100

	# Grid setup

	# Set the outside wall
	grid = [[wall if i == 0 or i == grid_size - 1 or j == 0 or j == grid_size - 1 else open_space for j in range(grid_size)] for i in range(grid_size)]

	# Create the 4 office walls
	for i in range(0, 46):
		for j in [45, 55]:
			grid[i][j] = wall
			grid[i][j] = wall
			grid[j][i] = wall
			grid[j][i] = wall

	for i in range(55, 100):
		for j in [45, 55]:
			grid[i][j] = wall
			grid[i][j] = wall
			grid[j][i] = wall
			grid[j][i] = wall

	# Create the internal doors
	for i in range(23, 27):
		grid[45][i] = open_space
		grid[55][i] = open_space
		grid[i][45] = open_space
		grid[i][55] = open_space

	for i in range(75, 79):
		grid[45][i] = open_space
		grid[55][i] = open_space
		grid[i][45] = open_space
		grid[i][55] = open_space

	# Create the desks
	for i in range(10, 35):
		for j in range(7, 38, 10):
			grid[i][j] = wall
			grid[i][j] = wall
		
		for j in range(63, 99, 10):
			grid[i][j] = wall
			grid[i][j] = wall

	for i in range(65, 90):
		for j in range(7, 38, 10):
			grid[i][j] = wall
			grid[i][j] = wall
			
		for j in range(63, 99, 10):
			grid[i][j] = wall
			grid[i][j] = wall

	# Set the exits
	for i in range(49, 52):
		grid[0][i] = exit  # Top
		grid[99][i] = exit # Bottom
		grid[i][0] = exit  # Left
		grid[i][99] = exit  # Right

	return grid