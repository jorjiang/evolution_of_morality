from scipy.special import expit
import numpy as np
import random

class SimpleMoralityGene:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class Monkey:
    max_exchange = 1
    def __init__(self, morality_gene: SimpleMoralityGene,
                 productivity = 1.0,
                 luck = 1.0,
                 resource: float = 1.0,
                 well_being: float = 1.0):
        self.morality_gene = morality_gene
        self.resource = resource
        self.well_being = np.sqrt(self.resource)
        self.productivity = productivity,
        self.luck = luck

    def produce(self, ):
        pass

    def interact(self, other):
        resource_difference = self.resource - other.resource
        exchanged_resource = self.morality_gene.a * resource_difference + \
                             self.morality_gene.b

        if exchanged_resource > other.resource:
            exchanged_resource = other.resource
        if exchanged_resource < -self.resource:
            exchanged_resource = self.resource

        self.resource += np.max(exchanged_resource)
        self.well_being = np.sqrt(self.resource)

        other.resource += exchanged_resource
        other.well_being = np.sqrt(other.resource)

class MonkeySpecies:
    def __init__(self, morality_gene: SimpleMoralityGene,
                 size: int,
                 id: int = -1,
                 interaction_rate = 0.1):
        self.monkeys = [Monkey(morality_gene=morality_gene)] * size
        self.id = id
        self.interaction_rate = interaction_rate
        self.n_interactions = np.round(self.interaction_rate * size)

    def interact(self):
        for monkey in random.shuffle(self.monkeys):
            other_monkeys = random.choices(monkey, k=self.n_interactions)
            for other_monkey in other_monkeys:
                monkey.interact(other_monkey)

        self.monkeys = [monkey for monkey in self.monkeys if monkey.well_being > 0]

    def get_species_well_being(self):
        return np.sum([monkey.well_being for monkey in self.monkeys])

    def get_species_well_being_per_capital(self):
        return np.mean([monkey.well_being for monkey in self.monkeys])


