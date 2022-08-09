import math
import random
import requests
#from time import time

population_size = 50
chromosome_size = 384
percentage_tournament = 0.5  # 50% tournament size
max_cycles = 10000
debug_level = 0


def random_initalization():
    # ------------------------------------------------------
    # This method initializes a population randomly (binary)
    # ------------------------------------------------------
    population = []
    for x in range(population_size):
        population.append([])
        chromosome_partial = ''
        for y in range(chromosome_size):
            randInt = random.randint(0, 1)
            chromosome_partial = chromosome_partial + str(randInt)
        population[x].append(chromosome_partial)
    return list(population)


def get_individual_fitness(individual):
    # ---------------------------------------------
    # This method gets the fitness of an individual
    # ---------------------------------------------
    url = "http://163.117.164.219/age/alfa?c="
    url = url + str(individual[0])
    r = 0
    if debug_level >= 3:
        print("calling url..." + url)
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
    for x in range(population_size):
        population_fitness.append(get_individual_fitness(population[x]))

    if debug_level >= 2:
        print("Fitness for first individual: " + str(population_fitness[0]))
    return list(population_fitness)


def tournament_selection(population_fitness):
    # ----------------------------------------------------------
    # This method selects the best individuals using tournaments
    # ----------------------------------------------------------
    t_size = int(math.floor(percentage_tournament * population_size))
    # print(t_size)
    intermediate_population = []
    for x in range(population_size):
        # select t random individuals
        selected = random.sample(range(population_size), t_size)
        # Promote the best one of the selected ones
        min_fitness = float('inf')
        best_individual = 0
        for y in selected:
            if debug_level >= 1:
                print("Potential individual: " + str(y) + " " + str(population_fitness[y]))
            if population_fitness[y] < min_fitness:
                min_fitness = population_fitness[y]
                best_individual = y
        intermediate_population.append(population[best_individual])
        if debug_level >= 1:
            print(best_individual)
            print(intermediate_population[x])
    return list(intermediate_population)


def generate_new_population(parents):
    # -------------------------------------------------------------------
    # This method generates a new population making crosses and mutations
    # -------------------------------------------------------------------

    # Crosses
    new_population = []
    cont = 0
    for x in range(population_size / 2):
        child_1 = ''
        child_2 = ''
        for y in range(chromosome_size):
            # child 1
            rand = random.randint(0, 1)
            if rand == 0:
                child_1 = child_1 + parents[cont][0][y]
            else:
                child_1 = child_1 + parents[cont + 1][0][y]
            # child 2
            rand = random.randint(0, 1)
            if rand == 0:
                child_2 = child_2 + parents[cont][0][y]
            else:
                child_2 = child_2 + parents[cont + 1][0][y]
        new_population.append([])
        new_population[cont].append(child_1)
        new_population.append([])
        new_population[cont + 1].append(child_2)
        cont = cont + 2
        if debug_level >= 1:
            print(child_1)
            print(child_2)
    # print(new_population)

    # Mutations
    mutations = []
    for x in range(population_size):
        mutation = ''
        for y in range(chromosome_size):
            rand = random.random()
            if rand < 0.02:
                if debug_level >= 1:
                    print(rand)
                    print(new_population[x])
                    print(mutation)
                if new_population[x][0][y] == '0':
                    mutation = mutation + '1'
                else:
                    mutation = mutation + '0'
            else:
                if new_population[x][0][y] == '0':
                    mutation = mutation + '0'
                else:
                    mutation = mutation + '1'
        mutations.append([])
        mutations[x].append(mutation)
    new_population = mutations
    # print(new_population)

    return list(new_population)

def obtain_replacement(population_fitness, new_population_fitness):
    # ------------------------------------------------------------------------------------------------------------
    # This method obtains the replacement (the new generation) by mixing the "best individuals" of two populations
    # ------------------------------------------------------------------------------------------------------------

    #print(population)
    #print(population_fitness)
    #print(new_population)
    #print(new_population_fitness)

    replacement = []
    for x in range(population_size):
        if new_population_fitness[x] < population_fitness[x]:
            replacement.append(new_population[x])
        else:
            replacement.append(population[x])

    return list(replacement)


min_fitness = float('inf')
better_individual = ''
population = random_initalization()  # The population is randomly initialized
population_fitness = evaluate_population(population)  # The fitness of the individuals in the population is evaluated

for i in range(population_size):
    if population_fitness[i] < min_fitness:
        min_fitness = population_fitness[i]
        better_individual = population[i]
print("El mejor fitness al principio es: " + str(
    min_fitness) + ", y se consigue con: " + str(better_individual))  # Print of the best individual and his fitness

#sum_execution_time_cycle = 0  # To calculate execution time of each cicle
for cycle in range(max_cycles):

    #start = time()

    min_fitness = float('inf')  # Minimum fitness of each cycle
    parents = tournament_selection(population_fitness)  # The individuals who are going to have offspring are obtained
    new_population = generate_new_population(parents)  # A new population is obtained by making crosses and mutations
    new_population_fitness = evaluate_population(new_population) # The fitness of the individuals in the new population is evaluated
    replacement = obtain_replacement(population_fitness, new_population_fitness)  # The new generation of individuals is obtained by comparing the fitness of the two populations
    population = replacement  # The original population is replaced by the new generation
    population_fitness = evaluate_population(population)  # The fitness of the individuals in the population is evaluated
    for j in range(population_size):
        if population_fitness[j] < min_fitness:
            min_fitness = population_fitness[j]
            better_individual = population[j]
    print("El mejor fitness al final del ciclo " + str(cycle + 1) + " es: " + str(
        min_fitness) + ", y se consigue con: " + str(better_individual))  # Print of the best individual and his fitness

    #end = time()

    #execution_time_cycle = end - start
    #sum_execution_time_cycle = sum_execution_time_cycle + execution_time_cycle

#mean_execution_time_cycle = sum_execution_time_cycle/max_cycles
#print("La media de tiempo de ejecucion de cada ciclo es " + str(mean_execution_time_cycle))


