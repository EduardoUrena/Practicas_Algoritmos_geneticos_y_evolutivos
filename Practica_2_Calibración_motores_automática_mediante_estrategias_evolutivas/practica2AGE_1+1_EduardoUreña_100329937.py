import math
import random
import numpy as np
import requests
import sys

chromosome_size = 4  # number of rotors
max_cycles = 100000
evaluations = 0
s = 10.0
changes_queue = []  # In this queue a "1" will be saved if there is an individual change and a "0" if there is not
changes_num = 0.0  # number of times the population has changed in the last "s" cycles


def random_initalization():
    # -----------------------------------------------------------------------------
    # This method initializes a population randomly (functional part and variances)
    # -----------------------------------------------------------------------------
    population_x = np.empty(shape=(1, chromosome_size))
    population_v = np.empty(shape=(1, chromosome_size))
    codification = np.array((1, 1))
    variances = np.array((1, 1))
    funtional = []
    sigma = []
    for y in range(chromosome_size):
        randFloat_x = random.uniform(-180, 180)
        randFloat_v = random.uniform(-18, 18)
        funtional.append(randFloat_x)
        sigma.append(randFloat_v)
        codification = np.array(funtional)
        variances = np.array(sigma)
    population_x[0] = codification
    population_v[0] = variances
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
    fitness = float(r)
    return fitness


def generate_new_population():
    # ----------------------------------------------------------
    # This method generates a new population by making mutations
    # ----------------------------------------------------------
    global changes_num

    mutation_x = np.empty(shape=(1, chromosome_size))
    mutation_v = np.empty(shape=(1, chromosome_size))
    for y in range(chromosome_size):
        # x_mutation
        mutation_x[0, y] = population[0][0, y] + np.random.normal(loc=0.0, scale=abs(population[1][0, y]), size=None)
        if mutation_x[0, y] > 180.0:
            mutation_x[0, y] = 180.0
        if mutation_x[0, y] < -180.0:
            mutation_x[0, y] = -180.0

        if cycle >= s:
            changes_num = changes_queue.count('1')
            psi = float(changes_num/s)
            if psi < 0.2:
                mutation_v[0, y] = 0.82 * float(population[1][0, y])
            if psi > 0.2:
                mutation_v[0, y] = float(population[1][0, y])/0.82
            if psi == 0.2:
                mutation_v[0, y] = float(population[1][0, y])
        if mutation_v[0, y] > 180.0:
            mutation_v[0, y] = 180.0
        if mutation_v[0, y] < -180.0:
            mutation_v[0, y] = -180.0

    return mutation_x, mutation_v


def obtain_replacement():
    # -------------------------------------------------------------------------------------------
    # This method obtains the replacement of the original population by comparing the populations
    # -------------------------------------------------------------------------------------------
    global population
    global changes_queue

    if new_population_fitness < population_fitness:
        for x in range(chromosome_size):
            population[0][0, x] = new_population[0][0, x]
            population[1][0, x] = new_population[1][0, x]
        if cycle >= s:
            changes_queue.pop(0)
        changes_queue.append('1')
    else:
        if cycle >= s:
            changes_queue.pop(0)
        changes_queue.append('0')
    return population


if chromosome_size == 4:

    population = random_initalization()  # The population is randomly initialized
    population_fitness = get_individual_fitness(population[0][0])  # The fitness of the individual in the population is evaluated

    c1 = population[0][0, 0]
    c2 = population[0][0, 1]
    c3 = population[0][0, 2]
    c4 = population[0][0, 3]
    print("El mejor fitness al principio es: " + str(population_fitness) + ", y se consigue con: c1=" + str(c1)
          + ", c2=" + str(c2) + ", c3=" + str(c3) + ", c4=" + str(c4) + ", y con "
          + str(evaluations) + " evaluaciones")  # Print of the best individual and his fitness and evaluations

    for cycle in range(max_cycles):

        new_population = generate_new_population()  # A new population is obtained by making mutations
        new_population_fitness = get_individual_fitness(new_population[0][0])  # The fitness of the new individual is evaluated
        population = obtain_replacement()  # A new generation is obtained by comparing the original individual with the new one
        population_fitness = get_individual_fitness(population[0][0])  # The fitness of the individual in the population is evaluated

        c1 = population[0][0, 0]
        c2 = population[0][0, 1]
        c3 = population[0][0, 2]
        c4 = population[0][0, 3]
        print("El mejor fitness al final del ciclo " + str(cycle + 1) + " es: " + str(population_fitness)
              + ", y se consigue con: c1=" + str(c1) + ", c2=" + str(c2)
              + ", c3=" + str(c3) + ", c4=" + str(c4) + ", y con "
              + str(evaluations) + " evaluaciones")  # Print of the best individual and his fitness and evaluations

elif chromosome_size == 10:

    population = random_initalization()  # The population is randomly initialized
    population_fitness = get_individual_fitness(population[0][0])  # The fitness of the individual in the population is evaluated

    c1 = population[0][0, 0]
    c2 = population[0][0, 1]
    c3 = population[0][0, 2]
    c4 = population[0][0, 3]
    c5 = population[0][0, 4]
    c6 = population[0][0, 5]
    c7 = population[0][0, 6]
    c8 = population[0][0, 7]
    c9 = population[0][0, 8]
    c10 = population[0][0, 9]
    print("El mejor fitness al principio es: " + str(population_fitness) + ", y se consigue con: c1="
          + str(c1) + ", c2=" + str(c2) + ", c3=" + str(c3) + ", c4=" + str(c4)
          + ", c5=" + str(c5) + ", c6=" + str(c6) + ", c7=" + str(c7) + ", c8=" + str(c8)
          + ", c9=" + str(c9) + ", c10=" + str(c10) + ", y con " + str(evaluations)
          + " evaluaciones")  # Print of the best individual and his fitness and evaluations

    for cycle in range(max_cycles):
        new_population = generate_new_population()  # A new population is obtained by making mutations
        new_population_fitness = get_individual_fitness(new_population[0][0])  # The fitness of the new individual is evaluated
        population = obtain_replacement()  # A new generation is obtained by comparing the original individual with the new one
        population_fitness = get_individual_fitness(population[0][0])  # The fitness of the individual in the population is evaluated

        c1 = population[0][0, 0]
        c2 = population[0][0, 1]
        c3 = population[0][0, 2]
        c4 = population[0][0, 3]
        c5 = population[0][0, 4]
        c6 = population[0][0, 5]
        c7 = population[0][0, 6]
        c8 = population[0][0, 7]
        c9 = population[0][0, 8]
        c10 = population[0][0, 9]
        print("El mejor fitness al final del ciclo " + str(cycle + 1) + " es: " + str(population_fitness)
              + ", y se consigue con: c1=" + str(c1) + ", c2=" + str(c2) + ", c3=" + str(c3)
              + ", c4=" + str(c4) + ", c5=" + str(c5) + ", c6=" + str(c6) + ", c7=" + str(c7)
              + ", c8=" + str(c8) + ", c9=" + str(c9) + ", c10=" + str(c10)
              + ", y con " + str(evaluations) + " evaluaciones")  # Print of the best individual and his fitness and evaluations
else:
    print("Error: chromosome size should be 4 or 10")
    sys.exit(1)
