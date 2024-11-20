import numpy as np

from filterpy.discrete_bayes import update
def lh_hallway(hall, z, z_prob):
    """ compute likelihood that a measurement matches
    positions in the hallway."""
    try:
        scale = z_prob / (1. - z_prob)
    except ZeroDivisionError:
        scale = 1e8
    likelihood = np.ones(len(hall))
    likelihood[hall==z] *= scale
    return likelihood

hallway = np.array([1., 1., 0., 0., 0., 0., 0., 0., 1., 0.]) 

belief = np.array([0.1] * 10)
likelihood = lh_hallway(hallway, z=1, z_prob=.75)
update(likelihood, belief)

print(.75 / (1. - .75))
print (belief)
print (likelihood)

norm_likelihood =  likelihood / sum(likelihood) 
print(norm_likelihood)