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

class defaut_args():
    pop_size = 1000
    no_gens = 400


children_dict = {}
for g1 in initial_gene_ratio.keys():
    for g2 in initial_gene_ratio.keys():
        # the output produced by product is of type ('X', 'X')
        children_dict[(g1, g2)] = [reduce(lambda x, y: x + y, g)
                                   for g in itertools.product(g1, g2)]


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
        pop[i:j] = gene
        i = j
    assert j == pop_size
    np.random.shuffle(pop)
    return pop


def next_gen(pop):
    n = len(pop)

    children = []
    for i in xrange(n):
        j, k = np.random.randint(n), np.random.randint(n)
        for child in children_dict[(pop[j], pop[k])]:
            children.append(child)

    np.random.shuffle(children)
    children = [child for child in children
                if np.random.rand() < survival_rates[child]][:n]

    return np.array(children)


def gene_percentage(pop, gene):
    return sum(1 for p in pop if p == gene)/(1.0*len(pop))


def play_for_gens(pop_size=defaut_args.pop_size, no_gens=defaut_args.no_gens):
    pop_ratios = {}
    for gene in initial_gene_ratio.keys():
        pop_ratios[gene] = np.zeros(no_gens)

    pop = gen_population(pop_size)

    for i in xrange(no_gens):
        for gene in initial_gene_ratio.keys():
            pop_ratios[gene][i] = gene_percentage(pop, gene)
        pop = next_gen(pop)

    return pop_ratios


def average_results(pop_size=defaut_args.pop_size, no_gens=defaut_args.no_gens, no_times=10):
    pop_ratios = {}
    for gene in initial_gene_ratio.keys():
        pop_ratios[gene] = np.zeros(no_gens, dtype=np.float16)

    for i in xrange(no_times):
        result = play_for_gens(pop_size, no_gens)
        for gene in initial_gene_ratio.keys():
            pop_ratios[gene] += result[gene]

    for gene in initial_gene_ratio.keys():
        pop_ratios[gene] = pop_ratios[gene]/no_times

    return pop_ratios


def plot_populations(results):
    # use %matplotlib inline in IPython
    no_gens = len(results['XY'])
    plt.plot(results['XY'], 'r')
    plt.plot(results['YX'], 'g')
    plt.plot(results['YY'], 'b')
    plt.plot(results['XX'], 'y')
    plt.axis([0, no_gens, 0, 1.0])
