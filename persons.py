import random
import math


class Person:
    COUNT = 0
    LUCK_FACTOR = 0.1

    def __init__(self, parents=None):
        self.id = Person.COUNT
        Person.COUNT += 1
        if parents:
            self.talent = (parents[0].talent + parents[1].talent) / 2 * (
                1 + (random.random() - 0.5) / 10)
        else:
            self.talent = random.random()
        self.luck = random.random()
        self.luck_rank = math.inf
        self.talent_rank = math.inf

    @property
    def success_index(self):
        return self.talent * (
            1 - Person.LUCK_FACTOR) + self.luck * Person.LUCK_FACTOR

    def __repr__(self):
        return f'Person-{self.id}: T={self.talent_rank}({self.talent:.2f})' +\
            f' L={self.luck_rank}({self.luck:.2f})'

    def __eq__(self, other):
        if isinstance(other, Person):
            return self.id == other.id
        return False

    def __hash__(self):
        return self.id


def get_persons(count=100, parents=None):
    if parents:
        persons = sorted(
            (Person(parents=(random.choice(parents), random.choice(parents)),
                    key=lambda x: x.success_index,
                    reverse=True)))
    else:
        persons = sorted((Person() for i in range(1000)),
                         key=lambda x: x.success_index,
                         reverse=True)
    talented = sorted(persons, key=lambda x: x.talent, reverse=True)
    lucky = sorted(persons, key=lambda x: x.luck, reverse=True)
    for i, p in enumerate(zip(talented, lucky)):
        p[0].talent_rank = i
        p[1].luck_rank = i
    return persons
