import pygame
import random

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class Agent:
    def __init__(self, team, x, y, weapon="sword", health=100, attack=10, defense=5, armor=False):
        self.team = team
        self.x = x
        self.y = y
        self.weapon = weapon
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
            damage = max(0, self.attack - enemy.defense)
            enemy.health -= damage
        elif self.weapon == "spear":
            if abs(self.x - enemy.x) <= 2 and abs(self.y - enemy.y) <= 2 and random.random() < 0.5:
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
        self.spear_blue = 5
        self.spear_red = 5
        self.agents = []
        self.running = False

    def initialize_agents(self):
        for team, num_agents, num_armor, num_spear in [(0, self.agents_blue, self.armor_blue, self.spear_blue),
                                                       (1, self.agents_red, self.armor_red, self.spear_red)]:
            for _ in range(num_agents):
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                armor = _ < num_armor
                weapon = "sword"
                if _ < num_spear:
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

    def remove_dead_agents(self):
        self.agents = [agent for agent in self.agents if agent.health > 0]

    def run_simulation(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width * 20, self.height * 20))
        pygame.display.set_caption("Medieval Battle Simulation")
        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            screen.fill(WHITE)

            self.move_agents()
            self.combat()
            self.remove_dead_agents()

            for agent in self.agents:
                color = BLUE if agent.team == 0 else RED
                size = 10  # Decrease the size of agents
                pygame.draw.rect(screen, color, (agent.x * 20, agent.y * 20, size, size))

            pygame.display.flip()
            clock.tick(30)  # Adjust the frame rate

        pygame.quit()

# Example usage
simulation = BattleSimulation(30, 30)  # 30x30 battlefield
simulation.initialize_agents()
simulation.run_simulation()
