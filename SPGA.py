#!/usr/bin/env python
# coding: utf-8

# In[2]:


from collections import OrderedDict
import random
from chromosome import Chromosome
import csv
import pandas as pd
import numpy as np
import math

# In[3]:


class SPGA(object):
    def __init__(self, dimension, weights, len_cromosom, src, dest, flag):
        """
        :param dimension: problem dimension
        :param weights:
        :param len_cromosom: length of chromosome
        :param src: source node
        :param dest: destination node
        :return:
        """
        if src >= dimension or dest >= dimension:
            raise ValueError
        # class parameters
        self.dimension = dimension
        self.weights = weights
        self.src = src
        self.dest = dest
        self.results = []
        self.len_cromosom = len_cromosom
        self.best_chromosome = None
        self.population = []
        self.population_size = 0
        self.population_scores = []
        self.flag = flag

    # get the score of population / all chromosomes in population
    def getPopulationScores(self):
        return self.population_scores
    
    # get the fitness of population 
    def fitnessPopulation(self):
        """
        :return: calculate fitness for this population
        """
        score = 0
        for crom in self.population:
            # get fitness for each chromosome in population
            score = score + self.fitnessChromosome(crom)
        return score
        
    # start Genetic Algorithm
    def runGA(self, max_num_generations, size_population):
        """
        :param max_num_generations: maximum number of generations
        :param size_population: initial population size
        :return: best solution found
        """
        generation = 0  # from first generation
        prev_score = 0
        self.generatePopulation(size_population)  # generate initial population
        self.population_size = size_population
        #if not self.flag:
            #self.doPrint('Начальная популяция:')
            #self.printPopulation(self.population)
        # loop into all generations
        while generation <= max_num_generations:
            generation += 1
            population_counter = 1
            new_population = list()
            # inter population / loop into chromosomes
            while population_counter <= self.population_size:
                population_counter += 1
                parents = random.sample(range(self.population_size), 2)
                # get crossover
                chromosome_crossover = self.crossover(self.population[parents[0]], self.population[parents[1]])
                # get mutate
                chromosome_crossover.mutate()
                #get the fitness of chromosome
                fit = self.fitnessChromosome(chromosome_crossover)
                self.results.append((chromosome_crossover, fit))
                # get new population
                new_population.append(chromosome_crossover)
                # choose the best chromosome
                if self.best_chromosome is None or self.best_chromosome[1] > fit:
                    self.best_chromosome = (chromosome_crossover, fit)
            # get selesction
            self.selection(self.population, new_population)
            # get the fitness of population
            score = self.fitnessPopulation()
            self.population_scores.append(score)
            #print(f"Поколение {generation}:\n\tПригодность популяции: {score}, Лучшая хромосома: {self.best_chromosome}")
        return self.best_chromosome

    def selection(self, previous_generation, current):
        """
        :param previous_generation: previous generation
        :param current: new generation
        :return:
        """
        previous_generation.extend(current)
        previous_generation.sort(key=lambda cr: self.fitnessChromosome(cr))
        self.population = previous_generation[:self.population_size]

    def generatePopulation(self, num):
        """
        :param num: number of chromosomes
        :return: population of chromosomes
        """
        list_population = list()
        for i in range(num):
            list_population.append(self.generateChromosome())
        self.population = list_population

    def generateChromosome(self):
        """
        :return: random path from source to destination
        """
        chromosome = random.sample(list(set(range(self.dimension)) - {self.src, self.dest}),
                                   self.len_cromosom - 2)
        chromosome.insert(0, self.src)
        chromosome.append(self.dest)
        return Chromosome(chromosome)

    def crossover(self, parent1, parent2):
        """
        :param parent1: first parent
        :param parent2: second parent
        :return: crossing over child
        """
        parent1_list = parent1.get()
        parent2_list = parent2.get()
        cut = random.randint(0, self.len_cromosom - 1)
        child = parent1_list[0:cut] + parent2_list[cut:]
        return Chromosome(child)

    def fitnessChromosome(self, chromosome):
        """
        :param chromosome: calculate fitness for this chromosome 
        :return: the score of fitness
        """
        chromosome_list = chromosome.get()
        return sum([self.weights[i][j] for i, j in zip(chromosome_list[:-1], chromosome_list[1:])])

    def printPopulation(self, population):
        """
        :param population: print chromosomes in population
        """
        for i, chromosome in enumerate(population):
            print ("Хромосома "+ str(i) + ": " + str(chromosome) + " | Пригодность: " + str(self.fitnessChromosome(chromosome)))
    
    def doPrint(msg, hint=''):
        print ('')
        print ('==================')
        print (hint + str(msg))
        print ('==================')


# In[ ]:




