import math
import random
import numpy as np
import requests
import sys

population_size = 70  # number of individuals
chromosome_size = 4  # number of rotors
percentage_tournament = 0.03  # 3% tournament size
max_cycles = 10000
evaluations = 0
parents_fitness = []
T = 1/(math.sqrt(2*math.sqrt(chromosome_size)))
T0 = 1/(math.sqrt(2*chromosome_size))

def random_initalization():
    # -----------------------------------------------------------------------------
    # This method initializes a population randomly (functional part and variances)
    # -----------------------------------------------------------------------------
    population_x = np.empty(shape=(population_size, chromosome_size))
    population_v = np.empty(shape=(population_size, chromosome_size))
    codification = np.array((1, 1))
    variances = np.array((1, 1))
    for x in range(population_size):
        funtional = []
        sigma = []
        for y in range(chromosome_size):
            randFloat_x = random.uniform(-180, 180)
            randFloat_v = random.uniform(-180, 180)
            funtional.append(randFloat_x)
            sigma.append(randFloat_v)
            codification = np.array(funtional)
            variances = np.array(sigma)
        population_x[x] = codification
        population_v[x] = variances
    return population_x, population_v

def get_individual_fitness(individual):
    # ---------------------------------------------
    # This method gets the fitness of an individual
    # ---------------------------------------------
    global evaluations

    if chromosome_size == 4:
        url = "http://163.117.164.219/age/robot4?c1=" + str(individual[0]) + "&c2=" + str(individual[1]) \
              + "&c3=" + str(individual[2]) + "&c4=" + str(individual[3])

    if chromosome_size == 10:
        url = "http://163.117.164.219/age/robot10?c1=" + str(individual[0]) + "&c2=" + str(individual[1]) \
              + "&c3=" + str(individual[2]) + "&c4=" + str(individual[3]) + "&c5=" + str(individual[4]) \
              + "&c6=" + str(individual[5]) + "&c7=" + str(individual[6]) + "&c8=" + str(individual[7]) \
              + "&c9=" + str(individual[8]) + "&c10=" + str(individual[9])

    evaluations += 1
    r = 0
    try:
        r = requests.get(url).content
        r = r.decode("utf-8")
    except:
        print("error with the web call")
    result = float(r)
    return result


def evaluate_population(population):
    # --------------------------------------------------------------------
    # This method saves all individual fitness of the population in a list
    # --------------------------------------------------------------------
    population_fitness = []
    actual_population_size = population[0].shape[0]
    for x in range(actual_population_size):
        population_fitness.append(get_individual_fitness(population[0][x]))

    return list(population_fitness)


def tournament_selection(population_fitness):
    # ----------------------------------------------------------
    # This method selects the best individuals using tournaments
    # ----------------------------------------------------------
    t_size = int(math.floor(percentage_tournament * population_size))
    global parents_fitness
    intermediate_population_x = np.empty(shape=(population_size, chromosome_size))
    intermediate_population_v = np.empty(shape=(population_size, chromosome_size))
    for x in range(population_size):

        # select t random individuals
        selected = random.sample(range(population_size), t_size)

        # Promote the best one of the selected ones
        min_fitness = float('inf')
        best_individual = 0
        for y in selected:
            if population_fitness[y] < min_fitness:
                min_fitness = population_fitness[y]
                best_individual = y
        intermediate_population_x[x] = population[0][best_individual]
        parents_fitness.append(min_fitness)
        intermediate_population_v[x] = population[1][best_individual]

    return intermediate_population_x, intermediate_population_v


def generate_new_population(parents):
    # ------------------------------------------------------------------------------------------------------------
    # This method generates a new population by making the crosses and mutations corresponding to (mu + lambda)-EE
    # ------------------------------------------------------------------------------------------------------------

    # Crosses
    new_population_x = np.empty(shape=(population_size/2, chromosome_size))
    new_population_v = np.empty(shape=(population_size/2, chromosome_size))
    cont = 0
    for x in range(population_size / 2):
        for y in range(chromosome_size):
            # x_crosses
            new_population_x[x, y] = (parents[0][cont, y] + parents[0][cont + 1, y])*0.5
            # variance_crosses
            rand = random.randint(0, 1)
            if rand == 0:
                new_population_v[x, y] = parents[1][cont, y]
            else:
                new_population_v[x, y] = parents[1][cont + 1, y]
        cont = cont + 2

    # Mutations
    mutations_x = np.empty(shape=(population_size/2, chromosome_size))
    mutations_v = np.empty(shape=(population_size/2, chromosome_size))
    for x in range(population_size/2):
        for y in range(chromosome_size):

            # x_mutations
            mutations_x[x, y] = new_population_x[x, y] + np.random.normal(loc=0.0, scale=abs(new_population_v[x, y]), size=None)
            if mutations_x[x, y] > 180.0:
                mutations_x[x, y] = 180.0
            if mutations_x[x, y] < -180.0:
                mutations_x[x, y] = -180.0

            # variance_mutations
            mutations_v[x, y] = math.exp(np.random.normal(loc=0.0, scale=T0, size=None))\
                                * new_population_v[x, y] * math.exp(np.random.normal(loc=0.0, scale=T, size=None))
            if mutations_v[x, y] > 180.0:
                mutations_v[x, y] = 180.0
            if mutations_v[x, y] < -180.0:
                mutations_v[x, y] = -180.0

    return mutations_x, mutations_v


def obtain_replacement():
    # ---------------------------------------------------------------------------
    # This method obtains the replacement of the original population by inclusion
    # ---------------------------------------------------------------------------

    replacement_x = np.empty(shape=(population_size * 3 / 2, chromosome_size))
    replacement_v = np.empty(shape=(population_size * 3 / 2, chromosome_size))
    fitness_union = []
    for x in range(population_size):
        replacement_x[x] = population[0][x]
        replacement_v[x] = population[1][x]
        fitness_union.append(population_fitness[x])
    for x in range(population_size/2):
        replacement_x[x + population_size] = new_population[0][x]
        replacement_v[x + population_size] = new_population[1][x]
        fitness_union.append(new_population_fitness[x])
    for x in range(population_size/2):
        worst_fitness = fitness_union.index(max(fitness_union))
        replacement_x = np.delete(replacement_x, worst_fitness, axis=0)
        replacement_v = np.delete(replacement_v, worst_fitness, axis=0)
        del fitness_union[worst_fitness]
    return replacement_x, replacement_v


min_fitness = float('inf')

if chromosome_size == 4:
    better_c1 = 0
    better_c2 = 0
    better_c3 = 0
    better_c4 = 0
    population = random_initalization()  # The population is randomly initialized
    population_fitness = evaluate_population(population)  # The fitness of the individuals in the population is evaluated

    for i in range(population_size):
        if population_fitness[i] < min_fitness:
            min_fitness = population_fitness[i]
            better_c1 = population[0][i, 0]
            better_c2 = population[0][i, 1]
            better_c3 = population[0][i, 2]
            better_c4 = population[0][i, 3]
    print("El mejor fitness al principio es: " + str(min_fitness) + ", y se consigue con: c1=" + str(better_c1)
          + ", c2=" + str(better_c2) + ", c3=" + str(better_c3) + ", c4=" + str(better_c4) + ", y con "
          + str(evaluations) + " evaluaciones")  # Print of the best individual and his fitness and evaluations

    for cycle in range(max_cycles):

        min_fitness = float('inf')  # Minimum fitness of each cycle
        parents = tournament_selection(population_fitness)  # The individuals who are going to have descendents are obtained
        new_population = generate_new_population(parents)  # A new population is obtained by making crosses and mutations
        new_population_fitness = evaluate_population(new_population) # The fitness of the individuals in the new population is evaluated
        replacement = obtain_replacement()  # The new generation of individuals is obtained by inclusion
        population = replacement  # The original population is replaced by the new generation
        population_fitness = evaluate_population(population)  # The fitness of the individuals in the population is evaluated
        for j in range(population_size):
            if population_fitness[j] < min_fitness:
                min_fitness = population_fitness[j]
                better_c1 = population[0][j, 0]
                better_c2 = population[0][j, 1]
                better_c3 = population[0][j, 2]
                better_c4 = population[0][j, 3]
        print("El mejor fitness al final del ciclo " + str(cycle + 1) + " es: " + str(min_fitness)
              + ", y se consigue con: c1=" + str(better_c1) + ", c2=" + str(better_c2)
              + ", c3=" + str(better_c3) + ", c4=" + str(better_c4) + ", y con "
              + str(evaluations) + " evaluaciones")  # Print of the best individual and his fitness and evaluations

elif chromosome_size == 10:
    better_c1 = 0
    better_c2 = 0
    better_c3 = 0
    better_c4 = 0
    better_c5 = 0
    better_c6 = 0
    better_c7 = 0
    better_c8 = 0
    better_c9 = 0
    population = random_initalization()  # The population is randomly initialized
    population_fitness = evaluate_population(
        population)  # The fitness of the individuals in the population is evaluated

    for i in range(population_size):
        if population_fitness[i] < min_fitness:
            min_fitness = population_fitness[i]
            better_c1 = population[0][i, 0]
            better_c2 = population[0][i, 1]
            better_c3 = population[0][i, 2]
            better_c4 = population[0][i, 3]
            better_c5 = population[0][i, 4]
            better_c6 = population[0][i, 5]
            better_c7 = population[0][i, 6]
            better_c8 = population[0][i, 7]
            better_c9 = population[0][i, 8]
            better_c10 = population[0][i, 9]
    print("El mejor fitness al principio es: " + str(min_fitness) + ", y se consigue con: c1="
          + str(better_c1) + ", c2=" + str(better_c2) + ", c3=" + str(better_c3) + ", c4=" + str(better_c4)
          + ", c5=" + str(better_c5) + ", c6=" + str(better_c6) + ", c7=" + str(better_c7) + ", c8=" + str(better_c8)
          + ", c9=" + str(better_c9) + ", c10=" + str(better_c10) + ", y con " + str(evaluations)
          + " evaluaciones")  # Print of the best individual and his fitness and evaluations

    for cycle in range(max_cycles):

        min_fitness = float('inf')  # Minimum fitness of each cycle
        parents = tournament_selection(population_fitness)  # The individuals who are going to have descendents are obtained
        new_population = generate_new_population(parents)  # A new population is obtained by making crosses and mutations
        new_population_fitness = evaluate_population(new_population)  # The fitness of the individuals in the new population is evaluated
        replacement = obtain_replacement()  # The new generation of individuals is obtained by inclusion
        population = replacement  # The original population is replaced by the new generation
        population_fitness = evaluate_population(
            population)  # The fitness of the individuals in the population is evaluated
        for j in range(population_size):
            if population_fitness[j] < min_fitness:
                min_fitness = population_fitness[j]
                better_c1 = population[0][j, 0]
                better_c2 = population[0][j, 1]
                better_c3 = population[0][j, 2]
                better_c4 = population[0][j, 3]
                better_c5 = population[0][j, 4]
                better_c6 = population[0][j, 5]
                better_c7 = population[0][j, 6]
                better_c8 = population[0][j, 7]
                better_c9 = population[0][j, 8]
                better_c10 = population[0][j, 9]
        print("El mejor fitness al final del ciclo " + str(cycle + 1) + " es: " + str(min_fitness)
              + ", y se consigue con: c1=" + str(better_c1) + ", c2=" + str(better_c2) + ", c3="
              + str(better_c3) + ", c4=" + str(better_c4) + ", c5=" + str(better_c5) + ", c6=" + str(better_c6)
              + ", c7=" + str(better_c7) + ", c8=" + str(better_c8) + ", c9=" + str(better_c9) + ", c10=" + str(
                    better_c10)
              + ", y con " + str(
                    evaluations) + " evaluaciones")  # Print of the best individual and his fitness and evaluations
else:
    print("Error: chromosome size should be 4 or 10")
    sys.exit(1)
