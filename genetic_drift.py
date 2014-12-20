"""
Monte Carlo Simulations to study the genetic drift

Model
-----

There are two species of asexual organisms who produce the indentical copies
of themselves after each generation. Because of enviornmental factors the total
number of organisms remain conserved.
"""

import numpy as np
import itertools
from matplotlib import pyplot as plt
from functools import reduce


class WorldModel():
    survival_rates = {
        'X': 1.0,
        'Y': 1.0
    }

    initial_gene_ratio = {
        'X': 1.0,
        'Y': 1.0
    }


class DefaultArgs:
    pop_size = 1000
    no_gens = 400


def gen_population(pop_size):
    """ generate population of pop_size according to the world model"""
    pop = np.zeros(pop_size, dtype=tuple)

    i = 0
    for gene in WorldModel.initial_gene_ratio.keys():
        j = i + int(WorldModel.initial_gene_ratio[gene]*pop_size
                    /sum(WorldModel.initial_gene_ratio.values()))
        pop[i:j] = gene
        i = j
    assert j == pop_size
    np.random.shuffle(pop)
    return pop


def next_gen(pop):
    n = len(pop)

    children = np.zeros(2*n, dtype=tuple)
    children[:n] = pop
    children[n:] = pop

    rand_arr = np.random.rand(2*n)
    s_rate = children.copy()
    for gene in WorldModel.initial_gene_ratio.keys():
        s_rate[s_rate == gene] = WorldModel.survival_rates[gene]

    surviving_children = children[rand_arr < s_rate]
    np.random.shuffle(surviving_children)

    return surviving_children[:n]


def gene_percentage(pop, gene):
    return np.sum(pop == gene)/(1.0*len(pop))


def play_for_gens(pop_size=DefaultArgs.pop_size, no_gens=DefaultArgs.no_gens):
    """
    Returns
    =======
    Dict:
        The percentage of organism of a particular gene
    """
    pop_ratios = {}
    for gene in WorldModel.initial_gene_ratio.keys():
        pop_ratios[gene] = np.zeros(no_gens)

    pop = gen_population(pop_size)

    for i in range(no_gens):
        for gene in WorldModel.initial_gene_ratio.keys():
            pop_ratios[gene][i] = gene_percentage(pop, gene)
        pop = next_gen(pop)

    return pop_ratios


def average_results(pop_size=DefaultArgs.pop_size, no_gens=DefaultArgs.no_gens, no_times=10):
    """
    Caculates the variation of ratio of the population from the highest to
    the lowest percentage with the number of generations
    """
    no_genes = WorldModel.initial_gene_ratio.keys())

    pop_ratios = np.zeros(no_genes, dtype=np.object)
    for i, gene in enumerate(WorldModel.initial_gene_ratio.keys()):
        pop_ratios.append(np.zeros(no_gens, dtype=np.float16))

    for i in range(no_times):
        result = play_for_gens(pop_size, no_gens)
        ratios = np.array(sorted(result.values()))
        pop_ratios
        for gene in WorldModel.initial_gene_ratio.keys():
            pop_ratios[gene] += result[gene]

    for gene in WorldModel.initial_gene_ratio.keys():
        pop_ratios[gene] = pop_ratios[gene]/no_times

    return pop_ratios


def plot_populations(results):
    # use %matplotlib inline in IPython
    no_gens = len(results['X'])
    plt.plot(results['Y'], 'r')
    plt.plot(results['X'], 'b')
    plt.axis([0, no_gens, 0, 1.0])
