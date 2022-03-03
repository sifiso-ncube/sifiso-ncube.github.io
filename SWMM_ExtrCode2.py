'''
This Code Extracts Flood-related parameters from the SWMM Model. The following functions are developed
1. Run the model
2. Node flooding rate
3. Ponded Volume for all Nodes at a given time
4. Time series ponded volume for s given node
5. Ts Rainfall over a given subcatchment
6.  Runoff rate for all subcatchments at a fixed time
7. Ts runoff rate for a given subcatchment
8. Node attributes- attributes for a node at given timestep
9. Node IDs
'''


#%%
from pyswmm import  Output, Simulation, Subcatchments, Links, Nodes, RainGages
from swmm.toolkit.shared_enum import LinkAttribute, SubcatchAttribute, NodeAttribute
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
#%%
sim = Simulation(r"./DoLo.inp")              #r means treat as raw string

##Running the model
# after running the model it generates a report (.rpt)
def simulate():
    simul= sim.execute()
    return simul
simulate()

#%%
##NODES (tested using node N33-1)
# Number of Nodes
def Ex_nmbr_nodes():
  with Output('DoLo.out') as out:
    number_of_nodes = len(out.nodes)
    return number_of_nodes




#%%
# Nodes IDs
# returns a dictionary of model node names with their indices as values
def Ex_node_ids():
  with Output('DoLo.out') as out:
    ids = out.nodes
    return ids


#var= tb.listvariables('DoLo.out')




#%%
#Node Attributes -For all nodes at given time, get a particular attribute. -returns a dictionary of attribute values for all nodes at given timestep

#Node Flooding Rate
sim = Simulation(r"./DoLo.inp")
def Ex_nodeFlood_rate(node_name):
    nodeflood = Nodes(sim)[node_name]
    nodfloodlst= []
    time = []
    sim.step_advance(60*15)       #every 15 mins
    for step in sim:
        nodfloodlst.append(nodeflood.flooding)
        time.append(sim.current_time)
    return nodfloodlst, time

node_name = "N33-1"


#%%
nodfloodlst, time = Ex_nodeFlood_rate(node_name)
# font = {'family': 'serif',
#         'color':  'darkred',
#         'weight': 'normal',
#         'size': 16,
#         }
# plt.figure(figsize = [20, 6])
# plt.plot(time,nodfloodlst, label = '$Flooding Rate $')
# plt.xlabel("\n Datetime ",fontdict = font)
# plt.ylabel("\n Flooding (CMS)",fontdict = font)
# plt.title("Flooding Rate Time Series at Node: " +str(node_name), fontdict = font)
# #plt.xticks(nodes, rotation ='vertical')
# plt.legend()
# plt.show()

# Ponded Volume- for all nodes at a given time

# For all nodes at given time, get the ponded volume.
# returns a dictionary of attribute values for all nodes at given timestep
def Ex_ponded_volume():
    with Output('./DoLo.out') as out:
        data = out.node_attribute(NodeAttribute.PONDED_VOLUME, datetime(2020, 10, 15, 21))
        node_pondvol = []
        index_list = []
        non_ponded = []
        for object in data:
            if data[object] > 0:  # only those nodes which are flooded/ponded
                node_pondvol.append(data[object])  # data[object] gives the ponded volume
                index_list.append(object)  # the object is the node name
            else:
                non_ponded.append(object)
                # print(object, data[object])
        return node_pondvol, index_list, non_ponded


#node_pondvol, index_list, non_ponded = Ex_ponded_volume()  # assigning the function outputs to the list variables



# font = {'family': 'serif',
#         'color': 'darkred',
#         'weight': 'normal',
#         'size': 16,
#         }
# plt.figure(figsize=[20, 6])
# plt.bar(index_list, node_pondvol, label='$Ponded Volume for the nodes $')
# plt.xlabel("\n Nodes ", fontdict=font)
# plt.ylabel("\n Ponded volume (CM)", fontdict=font)
# plt.title("Ponded Volume on 2020-10-15 at 21:00hrs \n", fontdict=font)
# plt.xticks(rotation='vertical')
# plt.legend()
# plt.show()


#Node Time series for ponded volume. you specify the start and end time
# Returns a dictionary of attribute values with between start_index and end_index with reporting timesteps as keys
def Ex_node_pondedvol(node_name):
  with Output('./DoLo.out') as out:
      ts = out.node_series(node_name, NodeAttribute.PONDED_VOLUME, datetime(2020, 10, 15, 12), datetime(2020, 10, 16, 12))
      ts_node_pondedvol = []
      index_list= []

      for index in ts:
        ts_node_pondedvol.append(ts[index])     #ts[index] gives the time series value of hydraulics head at node N33-1
        index_list.append(index)                #the index is the node name
      return ts_node_pondedvol,index_list


node_name = "N33-1"

ts_node_pondedvol,index_list = Ex_node_pondedvol(node_name)   # assigning the function outputs to the list variables

# font = {'family': 'serif',
#         'color':  'darkred',
#         'weight': 'normal',
#         'size': 16,
#         }
# plt.figure(figsize = [20, 6])
# plt.plot(index_list, ts_node_pondedvol, label = '$ Ponded volume for node $')
# plt.xlabel("\n Nodes ",fontdict = font)
# plt.ylabel("\n Ponded volume (CM)",fontdict = font)
# plt.title("Ponded Volume for Node " + str(node_name), fontdict = font)
# #plt.xticks(nodes, rotation='vertical')
# plt.legend()
# plt.show()

# Node Attributes
#Gets all the attributes for a node at given time.
#returns a dictionary of attributes for a node at given timestep

def Ex_node_attributes(node_name):
  with Output('./DoLo.out') as out:
      data = out.node_result(node_name, datetime(2020, 10, 15, 21))
      index_list= []
      node_attr = []
      for object in data:
         node_attr.append(data[object])       #data[object] gives the value
         index_list.append(object)                #the object is the node attribute
      return node_attr, index_list
         #print(object, data[object])


node_name = "N33-1"

#node_attr, index_list = Ex_node_attributes(node_name)       #assigning the function outputs to the list variables
 ## make a table


##SUBCATCHMENT ATTRIBUTES
#Subcatchment IDs
def Ex_subcatchment_ids():
  with Output('./DoLo.out') as out:
    subctmts = out.subcatchments
    return subctmts

Ex_subcatchment_ids()

#Runoff Rate- Get the runoff rate for all subcatchments at a given time.
def Ex_runoff_rate():
  with Output('DoLo.out') as out:
    runoff_rate = []
    index_list= []
    data = out.subcatch_attribute(SubcatchAttribute.RUNOFF_RATE, datetime(2020, 10, 15, 21))
    for object in data:
      #print(object, data[object])
      runoff_rate.append(data[object])
      index_list.append(object)
    return runoff_rate, index_list

#runoff_rate, index_list = (Ex_runoff_rate())

# font = {'family': 'serif',
#         'color':  'darkred',
#         'weight': 'normal',
#         'size': 16,
#         }
# plt.figure(figsize = [15, 5])
# plt.bar(index_list, runoff_rate, align='edge',width= 0.8, label = '$Runoff-Rate$')
# plt.xlabel("\n Subcatchments ",fontdict = font)
# plt.ylabel("\n Runoff Rate (CMS)",fontdict = font)
# plt.title("Runoff Rate in 2020-10-15\n",fontdict = font)
# plt.xticks(rotation ='vertical')
# plt.legend()
# plt.show()

#SUBCATCHMENT TIME SERIES FOR DIFFERENT ATTRIBUTES, FOR A SPECIFIED TIME FRAME
#%%
# Subcatchment Time Series for Rainfall
#Subcatchment Time series for rainfall. you specify the start and end time
# Returns a dictionary of attribute values with between start_index and end_index with reporting timesteps as keys
def Ex_ts_rainfall(subctmt_name):
  with Output('./DoLo.out') as out:
      ts = out.subcatch_series(subctmt_name, SubcatchAttribute.RAINFALL, datetime(2020, 10, 15, 12), datetime(2020, 10, 16, 12))
      ts_rainfall = []
      index_list= []

      for index in ts:
        ts_rainfall.append(ts[index])     #ts[index] gives the time series value of rainfall over a subcatchment
        index_list.append(index)                #the index is the node name
      return ts_rainfall,index_list


subctmt_name ='SU36-1'
  # input ("Enter the area of interest: ")


#%%
#ts_rainfall,index_list = Ex_ts_rainfall(subctmt_name)   # assigning the function outputs to the list variables

# font = {'family': 'serif',
#         'color':  'darkred',
#         'weight': 'normal',
#         'size': 16,
#         }
# plt.figure(figsize = [20, 6])
# plt.plot(index_list, ts_rainfall, label = '$ Rainfall $')
# plt.xlabel("\n DateTime ",fontdict = font)
# plt.ylabel("\n Rainfall(mm)",fontdict = font)
# plt.title("Time Series for Rainfall over subcatchment: " + str(subctmt_name), fontdict = font)
# #plt.xticks(nodes, rotation='vertical')
# plt.legend()
# plt.show()

#%%
#Get Subcatchment Time Series for Runoff Rate
#Subcatchment Time series for runoff rate. you specify the start and end time
# Returns a dictionary of attribute values with between start_index and end_index with reporting timesteps as keys
def Ex_ts_runoffrate(subctmt_name):
  with Output('./DoLo.out') as out:
      ts = out.subcatch_series(subctmt_name, SubcatchAttribute.RUNOFF_RATE, datetime(2020, 10, 15, 12), datetime(2020, 10, 16, 12))
      ts_runoffrate = []
      index_list= []

      for index in ts:
        ts_runoffrate.append(ts[index])     #ts[index] gives the time series value of subcatchment runoff rate
        index_list.append(index)                #the index is the node name
      return ts_runoffrate,index_list


subctmt_name = "SU36-1"


#%%
#ts_runoffrate,index_list = Ex_ts_runoffrate(subctmt_name)   # assigning the function outputs to the list variables

# font = {'family': 'serif',
#         'color':  'darkred',
#         'weight': 'normal',
#         'size': 16,
#         }
# plt.figure(figsize = [20, 6])
# plt.plot(index_list, ts_runoffrate, label = '$ Rainfall $')
# plt.xlabel("\n DateTime ",fontdict = font)
# plt.ylabel("\n Runoff Rate(CMS)",fontdict = font)
# plt.title("Time Series for Runoff Rate over subcatchment: " + str(subctmt_name), fontdict = font)
# #plt.xticks(nodes, rotation='vertical')
# plt.legend()
# plt.show()

# %%
