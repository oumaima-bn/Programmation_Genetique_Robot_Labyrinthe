from random import randint, random, choice
from pyamaze import maze, agent, COLOR

# -----------------------------
# PARAMÈTRES
# -----------------------------
r, c = 7, 7
POP_SIZE = 100
GENERATIONS = 100
MAX_STEPS = 50

ACTIONS = [0, 1, 2]  
# 0 = avancer, 1 = gauche, 2 = droite

# -----------------------------
# LABYRINTHE
# -----------------------------
m = maze(r, c)
m.CreateMaze(loopPercent=30)
Map = m.maze_map

a = agent(m, footprints=True, filled=True)

# -----------------------------
# DONNÉES
# -----------------------------
Population = []
Fitness = []
Paths = []

# -----------------------------
# POPULATION
# -----------------------------
def init_population():
    Population.clear()
    for _ in range(POP_SIZE):
        # 12 règles pour plus de puissance (IMPORTANT)
        ind = [randint(0,2) for _ in range(12)]
        Population.append(ind)

# -----------------------------
# CAPTEURS SIMPLIFIÉS
# -----------------------------
def sensors(pos):
    x, y = pos
    front = 1 if Map[(x,y)]['E'] == 0 else 0
    left  = 1 if Map[(x,y)]['N'] == 0 else 0
    right = 1 if Map[(x,y)]['S'] == 0 else 0
    return (front, left, right)

# -----------------------------
# SIMULATION + FITNESS
# -----------------------------
def evaluate():
    Fitness.clear()
    Paths.clear()

    for ind in Population:
        pos = (1,1)
        path = [pos]
        visited = set()
        steps = 0

        for _ in range(MAX_STEPS):

            s = sensors(pos)
            idx = s[0]*4 + s[1]*2 + s[2]
            action = ind[idx % len(ind)]

            x, y = pos

            if action == 0:  # avancer
                if Map[(x,y)]['E'] == 1:
                    pos = (x, y+1)

            elif action == 1:  # gauche
                if Map[(x,y)]['N'] == 1:
                    pos = (x-1, y)

            elif action == 2:  # droite
                if Map[(x,y)]['S'] == 1:
                    pos = (x+1, y)

            if pos in visited:
                break

            visited.add(pos)
            path.append(pos)
            steps += 1

            if pos == (r,c):
                break

        Paths.append(path)

        # distance Manhattan
        dist = abs(pos[0]-r) + abs(pos[1]-c)

        # FITNESS AMÉLIORÉE ⭐
        score = 300 - dist*30 - steps*2

        if pos == (r,c):
            score += 1500

        Fitness.append(score)

# -----------------------------
# SÉLECTION (TOP 20%)
# -----------------------------
def selection():
    combined = list(zip(Fitness, Population))
    combined.sort(reverse=True, key=lambda x: x[0])
    return [ind for _, ind in combined[:POP_SIZE//5]]

# -----------------------------
# CROSSOVER
# -----------------------------
def crossover(parents):
    new_pop = []

    while len(new_pop) < POP_SIZE:
        p1 = choice(parents)
        p2 = choice(parents)

        cut = randint(1,len(p1)-1)
        child = p1[:cut] + p2[cut:]

        new_pop.append(child)

    return new_pop

# -----------------------------
# MUTATION (IMPORTANTE)
# -----------------------------
def mutation(pop):
    for ind in pop:
        if random() < 0.4:
            i = randint(0,len(ind)-1)
            ind[i] = randint(0,2)

# -----------------------------
# MEILLEURE SOLUTION
# -----------------------------
def best_solution():
    best = max(Fitness)
    idx = Fitness.index(best)
    return best, Population[idx], Paths[idx]

# -----------------------------
# MAIN LOOP
# -----------------------------
init_population()

solution = False

for gen in range(GENERATIONS):

    evaluate()

    best_score, best_ind, best_path = best_solution()

    print(f"Generation {gen} | Best score = {best_score}")

    if best_score > 1400:
        print("✅ Solution trouvée !")
        solution = True
        break

    parents = selection()
    Population[:] = crossover(parents)
    mutation(Population)

# -----------------------------
# AFFICHAGE FINAL
# -----------------------------
if solution and (r,c) in best_path:

    Final_Path = {}

    for i in range(1, len(best_path)):
        Final_Path[best_path[i]] = best_path[i-1]

    m.tracePath({a: Final_Path})
    m.run()

else:
    print(" Aucune solution complète trouvée")