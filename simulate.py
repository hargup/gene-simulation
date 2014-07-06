""" A simulation to check the effect of interbreeding on the percentage of
ressesive carrier """

import numpy as np
import itertools
from matplotlib import pyplot as plt

class person():
    def __init__(self, gender, gene):
        self.gender = gender
        self.gene = gene

    def __str__(self):
        return str((self.gender, self.gene))

    def __repr__(self):
        return self.__str__()


survival_rates = {
    'XX': 1.0,
    'XY': 1.0,
    'YX': 1.0,
    'YY': 0.5
}

initial_gene_ratio = {
    'XX': 1.0,
    'XY': 1.0,
    'YX': 1.0,
    'YY': 1.0
}

def create_children(parent1, parent2):
    """
    create the children out of parents
    """
    #XXX: this is independent of the gender of the parent
    gene = [reduce(lambda x, y: x + y, g)
            for g in itertools.product(parent1.gene, parent2.gene)]
    # the output produced by product is of type ('X', 'X')
    children = []
    for g in gene:
        if np.random.randint(2) == 1:
            children.append(person('M', g))
        else:
            children.append(person('F', g))
    return children


def gen_population(pop_size):
    # XXX: generating only female population
    # TODO: it can be an interesting experiment to play with
    # the number of genders and their mode of reproduction
    # Currently the reproduction is sexual but all the individuals can be thought to be
    # hermaphodite, who can possibly have sex with themselves
    pop = []

    for gene in initial_gene_ratio.keys():
        pop = pop + [person('F', gene) for i in
                     xrange(int(initial_gene_ratio[gene]*pop_size/sum(initial_gene_ratio.values())))]
    np.random.shuffle(pop)
    return pop


def next_gen(pop):
    n = len(pop)

    children = []
    for i in xrange(n):
        j, k = np.random.randint(n), np.random.randint(n)
        children = children + create_children(pop[j], pop[k])

    children = [child for child in children
                if np.random.rand() < survival_rates[child.gene]][:n]

    np.random.shuffle(children)
    return children


def gene_percentage(pop, gene):
    return sum(1 for p in pop if p.gene == gene)/(1.0*len(pop))


def play_for_gens(pop_size=500, no_gens=100):
    pop = gen_population(pop_size)

    print("Running the simulations with populuation"
          "size %s for %s generations " %(pop_size, no_gens))
    pop_ratios = {
        'XX': [gene_percentage(pop, 'XX')],
        'XY': [gene_percentage(pop, 'XY')],
        'YX': [gene_percentage(pop, 'YX')],
        'YY': [gene_percentage(pop, 'YY')]
    }
    # Though XY is not YX is not different but ignored it for simplicity
    for i in xrange(no_gens):
        pop = next_gen(pop)
        pop_ratios['XX'].append(gene_percentage(pop, 'XX'))
        pop_ratios['XY'].append(gene_percentage(pop, 'XY'))
        pop_ratios['YX'].append(gene_percentage(pop, 'YX'))
        pop_ratios['YY'].append(gene_percentage(pop, 'YY'))

    return pop_ratios

results = [play_for_gens(pop_size=500), play_for_gens(pop_size=1000), play_for_gens(pop_size=2000)]
plt.plot(results[0]['YY'], 'r')
plt.plot(results[1]['YY'], 'g')
plt.plot(results[2]['YY'], 'b')

# plt.plot(result1['XY'], 'r')
# plt.plot(result1['YX'], 'g')
# plt.plot(result1['YY'], 'y')

# How will it play out when

# Simulate the process of Exomarriage and gotra and inbreeding
# and exobreeding, marriage with cousins. Maintaining pedigree, etc

# Here the population size has been kept fixed try increasing it with
# numbers of generations.

# What about favourable recessive traits? It can be modeled by having a XX
# have a higher survival percentage than the XY and YY where both have same survial
# percentage

# Can have a lot of gene sets


# Don't lead to conclusions. Give warning about your limited knowledge of
# genetics
