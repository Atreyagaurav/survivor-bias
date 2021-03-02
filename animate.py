import argparse
import gc

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation, PillowWriter

import persons

arg_parser = argparse.ArgumentParser(
    description="Simulation of importance of Luck in Success.")
arg_parser.add_argument('--frames', dest='frames', type=int, default=5,
                        help="frames rate for animation. (5)")
arg_parser.add_argument('--epoch', dest='epoch', type=int, default=10,
                        help="how many epoch of simulation to run. (10)")
arg_parser.add_argument('--batch', dest='batch', type=int, default=10,
                        help="how many batch of simulation to run. (10)")
arg_parser.add_argument('--size', dest='size', type=int, default=100,
                        help="how many persons to put in each batch. (100)")
arg_parser.add_argument('--choose', dest='choose', type=int, default=10,
                        help="how many people to choose at the top. (10)")
arg_parser.add_argument('--luck_factor', dest='lf', type=float, default=0.1,
                        help="how important is the luck. (0.1)")
arg_parser.add_argument('--seed', dest='seed', default=None,
                        help="seed value for random.")
arg_parser.add_argument('--outfile', dest='outfile', default='animation.gif',
                        help="Location to the animation output file. (animation.gif)")
args = arg_parser.parse_args()

persons.Person.LUCK_FACTOR = args.lf
total_loop = args.batch * args.epoch

whole_data = [0 for i in range(args.choose+1)]
freq_table = [0 for i in range(args.choose+1)]
pers = [0 for i in range(args.size)]
with plt.style.context(("ggplot", "seaborn")):
    fig = plt.figure(constrained_layout=True, figsize=(16, 9))
    specs = gridspec.GridSpec(ncols=2, nrows=2, figure=fig)

    top = fig.add_subplot(specs[0, :])
    bleft = fig.add_subplot(specs[1, 0])
    bright = fig.add_subplot(specs[1, 1])

    success_plt = top.plot(range(len(pers)), pers,
                           color="tab:blue")[0]
    talent_plt = top.plot(range(len(pers)), pers, color="tab:red",
                          linewidth=0.1)[0]
    luck_plt = top.plot(range(len(pers)), pers, color="tab:green",
                        linewidth=0.1)[0]
    top.set_title("Distribution Success (blue), Talent (red) and " +
                  f"Luck (green) of {args.size} people")
    # top.legend((success_plt, talent_plt, luck_plt),
    #            ("Success", "Talent", "Luck"))

    bleft_bar = bleft.bar(range(args.choose+1), freq_table, color="tab:blue")
    bleft.set_ylabel('Frequency of Occurance')
    bleft.set_xlabel("How many of them would be on top without luck")
    bleft.set_title('This Batch')

    bright_bar = bright.bar(range(args.choose+1), whole_data, color="tab:blue")
    bright.set_ylabel('Frequency of Occurance')
    bright.set_xlabel("How many of them would be on top without luck")
    bright.set_title('Total')


def init():
    top.set_ylim(0, 1)
    top.tick_params(bottom=False, labelbottom=False)
    bright.set_xticks(range(11))
    bleft.set_xticks(range(11))


def update(i):
    global freq_table, whole_data
    print(f'{i*100/total_loop:.2f}%', end='\r')
    if (i % args.batch) == 0:
        freq_table = [0 for i in range(args.choose+1)]
        gc.collect()
    ps = sorted([persons.Person() for i in range(args.size)],
                key=lambda x: x.success_index, reverse=True)
    talented = sorted(ps, key=lambda x: x.talent, reverse=True)
    both = len(set(ps[:args.choose]).intersection(set(talented[:args.choose])))
    freq_table[both] += 1
    whole_data[both] += 1
    success_plt.set_data(range(len(ps)), [p.success_index for p in ps])
    talent_plt.set_data(range(len(ps)), [p.talent for p in ps])
    luck_plt.set_data(range(len(ps)), [p.luck for p in ps])
    bleft.set_ylim(0, max(freq_table))
    bright.set_ylim(0, max(whole_data))
    
    bleft.set_title(f'This Batch ({sum(freq_table)} people)')
    for i, b in enumerate(bleft_bar):
        b.set_height(freq_table[i])
    bright.set_title(f'Total ({sum(whole_data)} people)')
    for i, b in enumerate(bright_bar):
        b.set_height(whole_data[i])


anim = FuncAnimation(fig, update,
                     repeat=False,
                     blit=False,
                     frames=total_loop,
                     cache_frame_data=False,
                     save_count=4,
                     init_func=init)
writer = PillowWriter(fps=args.frames)
anim.save(args.outfile, writer=writer)
plt.show()
