import random
import math
import colorama

class Person:
    COUNT=0

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
        return self.talent * 0.9 + self.luck * 0.1

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
        persons = sorted((Person(parents=(
            random.choice(parents), random.choice(parents)
        ), key=lambda x: x.success_index, reverse=True)))
    else:
        persons = sorted((Person() for i in range(1000)), key=lambda x: x.success_index, reverse=True)
    talented = sorted(persons, key=lambda x: x.talent, reverse=True)
    lucky = sorted(persons, key=lambda x: x.luck, reverse=True)
    for i, p in enumerate(zip(talented, lucky), start=1):
        p[0].talent_rank = i
        p[1].luck_rank = i
    return persons

def show_top(persons, number):
    count = 0
    for person in persons[:number]:
        if person.talent_rank < number:
            count += 1
            print(colorama.Fore.GREEN, end='')
        elif person.talent_rank < number*2:
            print(colorama.Fore.YELLOW, end='')
        print(person, end='')
        print(colorama.Fore.RESET)
    return count


data = []
batch = 10
size = 1000
top = 10
verbose = False
for i in range(batch):
    ps = get_persons(size)
    if verbose:
        print(f'Experiment: {i+1}')
        both = show_top(ps, top)
        color = colorama.Fore.BLACK
        if both>4:
            color += colorama.Back.GREEN
        elif both>2:
            color += colorama.Back.YELLOW
        else:
            color += colorama.Back.RED
        print('Would have Accepted Anyway: ', end='')
        print(color+f'{both}'+colorama.Back.RESET+colorama.Fore.RESET)
    else:
        both = sum(map(lambda p: p.luck_rank < top, ps[:top]))
    data.append(both)

freq_table = [0 for i in range(top)]
for d in data:
    freq_table[d] += 1

most_freq = max(freq_table)
for i, entry in enumerate(freq_table):
    print(f'{i+1:2d}: {entry:3d}', end='')
    print('█'*(entry*100//most_freq))
