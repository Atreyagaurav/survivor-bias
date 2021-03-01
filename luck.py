import random
import colorama
import persons
import argparse


def show_top(persons, number):
    count = 0
    for person in persons[:number]:
        if person.talent_rank < number:
            count += 1
            print(colorama.Fore.GREEN, end='')
        elif person.talent_rank < number * 2:
            print(colorama.Fore.YELLOW, end='')
        print(person, end='')
        print(colorama.Fore.RESET)
    return count


arg_parser = argparse.ArgumentParser(
    description="Simulation of importance of Luck in Success.")
arg_parser.add_argument('--batch', dest='batch', type=int, default=10,
                        help="how many batch of simulation to run. (10)")
arg_parser.add_argument('--size', dest='size', type=int, default=1000,
                        help="how many persons to put in each batch. (1000)")
arg_parser.add_argument('--choose', dest='choose', type=int, default=10,
                        help="how many people to choose at the top. (10)")
arg_parser.add_argument('--luck_factor', dest='lf', type=float, default=0.1,
                        help="how important is the luck. (0.1)")
arg_parser.add_argument('--seed', dest='seed', default=None,
                        help="seed value for random.")
arg_parser.add_argument('--verbose', dest='verbose', action='store_true',
                        help="verbose output.")
args = arg_parser.parse_args()

if args.seed:
    random.seed(args.seed)
persons.Person.LUCK_FACTOR = args.lf

data = []
for i in range(args.batch):
    ps = persons.get_persons(args.size)
    if args.verbose:
        print(f'Experiment: {i+1}')
        both = show_top(ps, args.choose)
        color = colorama.Fore.BLACK
        if both > 4:
            color += colorama.Back.GREEN
        elif both > 2:
            color += colorama.Back.YELLOW
        else:
            color += colorama.Back.RED
        print('Would have Accepted Anyway: ', end='')
        print(color + f'{both}' + colorama.Back.RESET + colorama.Fore.RESET)
    else:
        both = sum(map(lambda p: p.luck_rank < args.choose, ps[:args.choose]))
    data.append(both)

freq_table = [0 for i in range(args.choose+1)]
for d in data:
    freq_table[d] += 1

most_freq = max(freq_table)
for i, entry in enumerate(freq_table):
    print(f'{i:2d} ', end='')
    print('█' * (entry * 50 // most_freq) + f' {entry}')
