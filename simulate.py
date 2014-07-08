""" A simulation to check the effect of interbreeding on the percentage of
ressesive carrier """

# The prime motive for this simulation was to test if interbreeding will
# eleminate the ressesive but unfavourable gene from the population faster than
# the exogamy would do. I'm little confused about simulating exogamy and interbreeding
# and the current program simulates only exogamy. It appears that interbreeding
# can eliminate unfourable traits pretty fast even if they appear as only ressesive triats
# so what is left are the traits which are favourable, exogamy appears to have its own
# advantages by as it can have best of both world mixing the goods two or more not very
# closely related gene pools. Or maybe a something like a restricted exogamy is
# favorable which is followed in northern India, where people aren't allowed to marry very
# closely related people (people of same gotra), but they don't marry outside the caste.
# Or maybe something like branch out -> grow in isolation -> merge. BTW we(humans) did
# branched out of early apes and mating with gorrilas (our cousins) doesn't seems to be
# very good idea.
#
# Outbreeding appears to have a better chance at producing good, whereas inbreeding seems to
# be better at eliminating the bad. I guess there will be a lot of factors at play for example
# the inbreeding specie will have a lot more unsuccessful kids which may lead to negative population
# growth and the ultimate extinction of the specie. We have a lot less risk of such cases in
# outbreeding because there are less chances of producing something too bad but what are the rates
# of progation of some good trait emerging out of the system? These are some pretty
# interesting questions.

# XXX: the simulation might not even a good candidate for inbreeding

import numpy as np
import itertools
from matplotlib import pyplot as plt
from numba import jit

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
    'YY': 1.0
}

initial_gene_ratio = {
    'XX': 1.0,
    'XY': 1.0,
    'YX': 1.0,
    'YY': 1.0
}


children_dict = {}
for g1 in initial_gene_ratio.keys():
    for g2 in initial_gene_ratio.keys():
        # the output produced by product is of type ('X', 'X')
        children_dict[(g1, g2)] = [reduce(lambda x, y: x + y, g)
                                   for g in itertools.product(g1, g2)]

def create_children(parent1, parent2):
    """
    create the children out of parents
    """
    #XXX: this is independent of the gender of the parent
    gene = children_dict[(parent1.gene, parent2.gene)]
    return tuple([person('F', g) for g in gene])


def gen_population(pop_size):
    # XXX: generating only female population
    # TODO: it can be an interesting experiment to play with
    # the number of genders and their mode of reproduction
    # Currently the reproduction is sexual but all the individuals can be thought to be
    # hermaphodite, who can possibly have sex with themselves
    pop = np.zeros(pop_size, dtype=tuple)

    i = 0
    for gene in initial_gene_ratio.keys():
        j = i + int(initial_gene_ratio[gene]*pop_size/sum(initial_gene_ratio.values()))
        pop[i:j] = person('F', gene)
        i = j
    assert j == pop_size
    np.random.shuffle(pop)
    return pop


def next_gen(pop):
    n = len(pop)

    children = []
    for i in xrange(n):
        j, k = np.random.randint(n), np.random.randint(n)
        for child in create_children(pop[j], pop[k]):
            children.append(child)

    np.random.shuffle(children)
    children = [child for child in children
                if np.random.rand() < survival_rates[child.gene]][:n]

    return np.array(children)


def gene_percentage(pop, gene):
    return sum(1 for p in pop if p.gene == gene)/(1.0*len(pop))


def play_for_gens(pop_size=100, no_gens=100, times_of_run=4):
    print("Running the simulations with populuation"
          "size %s for %s generations for %s times " %(pop_size, no_gens, times_of_run))
    pop_ratios = {
        'XX': [np.zeros(no_gens) for i in xrange(times_of_run)],
        'XY': [np.zeros(no_gens) for i in xrange(times_of_run)],
        'YX': [np.zeros(no_gens) for i in xrange(times_of_run)],
        'YY': [np.zeros(no_gens) for i in xrange(times_of_run)]
    }
    for i in xrange(times_of_run):
        pop = gen_population(pop_size)

        # Though XY is not YX is not different but ignored it for simplicity
        for j in xrange(no_gens):
            for gene in initial_gene_ratio.keys():
                pop_ratios[gene][i][j] = gene_percentage(pop, gene)
            pop = next_gen(pop)

    for gene in initial_gene_ratio.keys():
        pop_ratios[gene] = sum(pop_ratios[gene])/times_of_run

    return pop_ratios

results = [None, None, None]

results[2] = play_for_gens()

plt.plot(results[2]['XY'], 'r')
plt.plot(results[2]['YX'], 'g')
plt.plot(results[2]['YY'], 'b')
plt.plot(results[2]['XX'], 'y')
