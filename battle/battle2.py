import tkinter as tk
import random

class Agent:
    def __init__(self, team, x, y, weapon="sword", health=100, attack=10, defense=5, armor=False):
        self.team = team
        self.x = x
        self.y = y
        self.weapon = weapon  # Default weapon is "sword"
        self.health = health
        self.attack = attack
        self.defense = defense
        self.armor = armor
        if self.armor:
            self.health = 200

    def move(self, dx, dy, width, height):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < width:
            self.x = new_x
        if 0 <= new_y < height:
            self.y = new_y

    def attack_enemy(self, enemy):
        if self.weapon == "sword":
            # Sword attack logic remains unchanged
            damage = max(0, self.attack - enemy.defense)
            enemy.health -= damage
        elif self.weapon == "spear":
            # Spear attack logic: 50% chance of attacking enemies 2 cells away
            if abs(self.x - enemy.x) <= 2 and abs(self.y - enemy.y) <= 2 and random.random() < 0.66:
                damage = max(0, self.attack - enemy.defense)
                enemy.health -= damage

class BattleSimulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.agents_blue = 20
        self.agents_red = 20
        self.armor_blue = 5
        self.armor_red = 5
        self.spear_blue = 5  # Add spear count for blue team
        self.spear_red = 5   # Add spear count for red team
        self.blue_agents_entry = None
        self.red_agents_entry = None
        self.blue_armor_entry = None
        self.red_armor_entry = None
        self.canvas = None
        self.blue_bar = None
        self.red_bar = None
        self.root = None
        self.delay = 34  # milliseconds
        self.is_running = False

    def initialize_agents(self):
        self.agents = []
        for team, num_agents, num_armor, num_spear in [(0, self.agents_blue, self.armor_blue, self.spear_blue),
                                                       (1, self.agents_red, self.armor_red, self.spear_red)]:
            for _ in range(num_agents):
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                armor = _ < num_armor  # Assign armor to first num_armor agents
                weapon = "sword"
                if _ < num_spear:  # Assign spear to first num_spear agents
                    weapon = "spear"
                agent = Agent(team, x, y, weapon=weapon, armor=armor)
                self.agents.append(agent)

    def move_agents(self):
        for agent in self.agents:
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            agent.move(dx, dy, self.width, self.height)

    def combat(self):
        for agent in self.agents:
            enemies = [other for other in self.agents if other.team != agent.team and
                       abs(other.x - agent.x) <= 1 and abs(other.y - agent.y) <= 1]
            if enemies:
                enemy = random.choice(enemies)
                agent.attack_enemy(enemy)

    def update_canvas(self):
        self.canvas.delete("all")
        self.blue_bar = self.canvas.create_rectangle(0, 0, 20, (self.agents_blue / (self.agents_blue + self.agents_red)) * self.height * 20, fill="blue")
        self.red_bar = self.canvas.create_rectangle(self.width * 20 - 20, 0, self.width * 20, (self.agents_red / (self.agents_blue + self.agents_red)) * self.height * 20, fill="red")
        for agent in self.agents:
            if agent.health > 0:
                color = "blue" if agent.team == 0 else "red"
                x0 = agent.x * 20
                y0 = agent.y * 20
                x1 = (agent.x + 1) * 20
                y1 = (agent.y + 1) * 20
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def remove_dead_agents(self):
        for agent in self.agents:
            if agent.health <= 0:
                self.agents.remove(agent)
                if agent.team == 0:
                    self.agents_blue -= 1
                else:
                    self.agents_red -= 1

    def step_simulation(self):
        self.move_agents()
        self.combat()
        self.remove_dead_agents()
        self.update_canvas()
        if self.is_running:
            self.root.after(self.delay, self.step_simulation)

    def start_simulation(self):
        self.is_running = True
        self.agents_blue = int(self.blue_agents_entry.get())
        self.agents_red = int(self.red_agents_entry.get())
        self.armor_blue = int(self.blue_armor_entry.get())
        self.armor_red = int(self.red_armor_entry.get())
        self.initialize_agents()
        self.step_simulation()

    def stop_simulation(self):
        self.is_running = False

    def run_simulation(self):
        self.root = tk.Tk()
        self.root.title("Medieval Battle Simulation")

        blue_agents_label = tk.Label(self.root, text="Blue agents:")
        blue_agents_label.grid(row=0, column=0)
        self.blue_agents_entry = tk.Entry(self.root)
        self.blue_agents_entry.insert(tk.END, self.agents_blue)
        self.blue_agents_entry.grid(row=0, column=1)

        red_agents_label = tk.Label(self.root, text="Red agents:")
        red_agents_label.grid(row=1, column=0)
        self.red_agents_entry = tk.Entry(self.root)
        self.red_agents_entry.insert(tk.END, self.agents_red)
        self.red_agents_entry.grid(row=1, column=1)

        blue_armor_label = tk.Label(self.root, text="Blue armor:")
        blue_armor_label.grid(row=2, column=0)
        self.blue_armor_entry = tk.Entry(self.root)
        self.blue_armor_entry.insert(tk.END, self.armor_blue)
        self.blue_armor_entry.grid(row=2, column=1)

        red_armor_label = tk.Label(self.root, text="Red armor:")
        red_armor_label.grid(row=3, column=0)
        self.red_armor_entry = tk.Entry(self.root)
        self.red_armor_entry.insert(tk.END, self.armor_red)
        self.red_armor_entry.grid(row=3, column=1)

        blue_spear_label = tk.Label(self.root, text="Blue spear agents:")
        blue_spear_label.grid(row=4, column=0)
        self.blue_spear_entry = tk.Entry(self.root)
        self.blue_spear_entry.insert(tk.END, self.spear_blue)
        self.blue_spear_entry.grid(row=4, column=1)

        red_spear_label = tk.Label(self.root, text="Red spear agents:")
        red_spear_label.grid(row=5, column=0)
        self.red_spear_entry = tk.Entry(self.root)
        self.red_spear_entry.insert(tk.END, self.spear_red)
        self.red_spear_entry.grid(row=5, column=1)

        start_button = tk.Button(self.root, text="Start", command=self.start_simulation)
        start_button.grid(row=6, column=0, columnspan=2)

        stop_button = tk.Button(self.root, text="Stop", command=self.stop_simulation)
        stop_button.grid(row=7, column=0, columnspan=2)

        # Adjust the canvas size and agent size
        self.canvas = tk.Canvas(self.root, width=self.width * 20, height=self.height * 20, bg="white")
        self.canvas.grid(row=8, column=0, columnspan=2)

        self.root.mainloop()

# Example usage
simulation = BattleSimulation(30, 30)  # 40x40 battlefield
simulation.run_simulation()
