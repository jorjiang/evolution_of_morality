import random

import numpy as np

from utils.helper import randomly


class SimpleMoralityGene:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class Monkey:
    max_exchange = 1

    def __init__(self, morality_gene: SimpleMoralityGene,
                 productivity: float = 0.1,
                 luck=1.0,
                 resource: float = None,
                 id=-1):
        if resource is None:
            self.resource = np.random.normal(1, 0.1)
        self.morality_gene = morality_gene
        self.well_being = np.sqrt(self.resource)
        self.productivity = productivity
        self.luck = luck
        self.id = id

    def work(self):
        self.resource *= 1.0 + self.productivity

    def interact(self, other):
        # resource_difference = self.resource - other.resource
        exchanged_resource = self.morality_gene.a * other.well_being + \
                             self.morality_gene.b

        if exchanged_resource > other.resource:
            exchanged_resource = other.resource
        if exchanged_resource < -self.resource:
            exchanged_resource = self.resource

        self.resource += np.max(exchanged_resource)
        self.well_being = np.sqrt(self.resource)

        other.resource -= exchanged_resource
        other.well_being = np.sqrt(other.resource)


class MonkeySpecies:
    def __init__(self, morality_gene: SimpleMoralityGene,
                 size: int,
                 id: int = -1,
                 interaction_rate=0.1):
        self.morality_gene = morality_gene
        self.monkeys = []
        for i in range(size):
            self.monkeys.append(Monkey(morality_gene,
                                       id=i))
        self.interaction_rate = interaction_rate
        self.max_n_interactions = int(np.round(self.interaction_rate * size))
        self.id = id

    def work(self):
        for monkey in self.monkeys:
            monkey.work()

    def interact(self):
        for monkey in randomly(self.monkeys):
            all_other_monkeys = [m for m in self.monkeys if m.id != monkey.id]
            n_interactions = min(self.max_n_interactions, len(all_other_monkeys))
            other_monkeys = random.choices(all_other_monkeys, k=n_interactions)
            for other_monkey in other_monkeys:
                monkey.interact(other_monkey)

        self.monkeys = [monkey for monkey in self.monkeys if monkey.well_being > 0]

    def get_species_well_being(self):
        return np.sum([monkey.well_being for monkey in self.monkeys])

    def get_species_well_being_per_capital(self):
        return np.mean([monkey.well_being for monkey in self.monkeys])

    def get_all_well_being(self):
        return [monkey.well_being for monkey in self.monkeys]
