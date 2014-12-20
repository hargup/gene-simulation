"""
Monte Carlo Simulations to study the genetic drift

Model
-----
* Non overlaping generations
* asexual reproduction
* constant population size
"""

import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


class WorldModel():
    survival_rates = {
        'X': 1.0,
        'Y': 1.0,
    }

    initial_gene_ratio = {
        'X': 1.0,
        'Y': 1.0,
    }


class DefaultArgs:
    pop_size = 1000
    no_gens = 400


def gen_population(pop_size):
    """ generate population of pop_size according to the world model"""
    pop = np.zeros(pop_size, dtype=object)

    i = 0
    for gene in WorldModel.initial_gene_ratio.keys():
        j = i + int(WorldModel.initial_gene_ratio[gene] * pop_size
                    / sum(WorldModel.initial_gene_ratio.values()))
        pop[i: j] = gene
        i = j

    assert j == pop_size  # TODO: there shouldn't be a need to do this
    np.random.shuffle(pop)
    return pop


def next_gen(pop):
    n = len(pop)

    children = np.zeros(2*n, dtype=object)
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


def average_results(pop_size=DefaultArgs.pop_size,
                    no_gens=DefaultArgs.no_gens, no_times=10):
    """
    Caculates the variation of ratio of the population from the highest to
    the lowest percentage with the number of generations
    """
    avg = np.array(play_for_gens(pop_size, no_gens).values())
    avg.sort(axis=0)
    for i in range(1, no_times):
        result = np.array(play_for_gens(pop_size, no_gens).values())
        result.sort(axis=0)
        avg += result

    avg = avg/no_times

    return avg


def plot_ranks(avg):
    no_ranks, no_gens = avg.shape
    for i in range(no_ranks):
        plt.plot(avg[i])

    sns.set_style('darkgrid')
    plt.axis([0, no_gens, 0, 1.0])


def plot_populations(results):
    # use %matplotlib inline in IPython
    no_gens = len(results['X'])
    plt.plot(results['Y'], 'r')
    plt.plot(results['X'], 'b')
    plt.axis([0, no_gens, 0, 1.0])

# plt.plot(avg[0], 'r')
# plt.plot(avg[1], 'b')
