import tkinter as tk
import random

class Agent:
    def __init__(self, team, x, y, health=100, attack=10, defense=5, armor=False):
        self.team = team
        self.x = x
        self.y = y
        self.health = health
        self.attack = attack
        self.defense = defense
        self.armor = armor
        if self.armor:
            self.health = 150

    def move(self, dx, dy, width, height):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < width:
            self.x = new_x
        if 0 <= new_y < height:
            self.y = new_y

    def attack_enemy(self, enemy):
        damage = max(0, self.attack - enemy.defense)
        enemy.health -= damage

class BattleSimulation:
    def __init__(self, width, height, agents_per_team, armor_per_team):
        self.width = width
        self.height = height
        self.agents_per_team = agents_per_team
        self.armor_per_team = armor_per_team
        self.agents = []
        self.canvas = None
        self.root = None

    def initialize_agents(self, agents_blue, agents_red, armor_blue, armor_red):
        for team in range(2):
            num_agents = agents_blue if team == 0 else agents_red
            num_armor = armor_blue if team == 0 else armor_red
            for _ in range(num_agents):
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                armor = _ < num_armor  # Assign armor to first num_armor agents
                agent = Agent(team, x, y, armor=armor)
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
        for agent in self.agents:
            if agent.health > 0:
                color = "blue" if agent.team == 0 else "red"
                x0 = agent.x * 20
                y0 = agent.y * 20
                x1 = (agent.x + 1) * 20
                y1 = (agent.y + 1) * 20
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def remove_dead_agents(self):
        self.agents = [agent for agent in self.agents if agent.health > 0]

    def step_simulation(self):
        self.move_agents()
        self.combat()
        self.remove_dead_agents()
        self.update_canvas()

    def run_simulation(self, agents_blue, agents_red, armor_blue, armor_red):
        self.root = tk.Tk()
        self.root.title("Medieval Battle Simulation")
        self.canvas = tk.Canvas(self.root, width=self.width * 20, height=self.height * 20, bg="white")
        self.canvas.pack()

        self.initialize_agents(agents_blue, agents_red, armor_blue, armor_red)
        self.update_canvas()

        step_button = tk.Button(self.root, text="Step", command=self.step_simulation)
        step_button.pack()

        self.root.mainloop()

# Example usage
simulation = BattleSimulation(25, 25, 20, 5)  # 40x40 battlefield, 20 agents per team, 5 agents with armor per team
simulation.run_simulation(20, 30, 20, 0)  # 15 agents and 3 armor for team blue, 15 agents and 2 armor for team red
