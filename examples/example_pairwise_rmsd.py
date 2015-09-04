import pytraj as pt

traj = pt.iterload('../tests/data/md1_prod.Tc5b.x', '../tests/data/Tc5b.top')

mat = pt.pairwise_rmsd(traj, '@CA')
print(mat)
