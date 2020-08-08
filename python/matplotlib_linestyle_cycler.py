from cycler import cycler

default_cycler = (
    (cycler(color=list('rgbkmc')) * cycler(linestyle=['solid', 'dotted', 'dashed']))
)

plt.rc('lines', linewidth=2)
plt.rc('axes', prop_cycle=default_cycler)