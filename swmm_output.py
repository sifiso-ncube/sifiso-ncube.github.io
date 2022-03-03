
#%%
from pyswmm import Output, Simulation, Subcatchments, Links, Nodes, RainGages
from swmm.toolkit.shared_enum import LinkAttribute, SubcatchAttribute, NodeAttribute
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


#%%
# Number of subcatchments
def Ex_nmbr_subcatchments():
  with Output('15.10.1realday.out') as out:
    number_of_subcmts = len(out.subcatchments)
    return number_of_subcmts

print("The number of subcatchments is: ", Ex_nmbr_subcatchments())

#%%

from pyswmm import Output, Simulation, Subcatchments, Links, Nodes, RainGages

out=Output('15.10.1realday.out')
# %%
print(len(out.subcatchments))
print(len(out.nodes))
print(len(out.links))
print(out.version)

# %%
