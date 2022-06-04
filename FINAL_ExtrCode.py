
import linecache            # a module that allows us to read any line.
from pyswmm import  Output, Simulation, Subcatchments, Links, Nodes, RainGages
from swmm.toolkit.shared_enum import LinkAttribute, SubcatchAttribute, NodeAttribute
from datetime import datetime, timedelta, date



#flooding refers to all water that overflows a node whether it ponds or not.
'''
This Code Extracts Flood-related parameters from the SWMM Model. The following functions are developed:

1. Run the model
2. Ponded Volume for all Nodes at a given time - gives the flooded nodes/locations
3. Time series ponded volume for a given node
4. Node IDs
5. Hours Flooded
6. Time of max flood
7. Max flooding rate
8. Node flooding rate
9. Ts Rainfall over a given subcatchment

'''

#setting the total precipitation
# with Simulation('DoLo.inp') as sim:
#     rg1 = RainGages(sim)["YN1"]
#     print(rg1.total_precip)
#     rg1.total_precip = 0.2
#     print(rg1.total_precip)

# ########################################################################################

#
# ##Running the model
# # after running the model it generates a report (.rpt)
#
#
def simulate():
    sim = Simulation("DoLo.inp")
    simul= sim.execute()
    return simul


# sim2 = Simulation ('DoLo.inp')
# def Simulate_userinput(node_name,user_rain):
#     sim2 = Simulation('DoLo.inp')
#     rg1 = RainGages(sim2)["YN1"]
#     #print(rg1.total_precip)
#     rg1.total_precip = user_rain # change the valu of the total rainfall the user inputs.the value of the total rainfall the user inputs
#     j1 = Nodes(sim2)[node_name]
#     fl_j1 = []
#     sim2.step_advance(60*60*72)
#     for step in sim2:
#         fl_j1.append((sim2.current_time, j1.flooding))
#     return fl_j1
#
# print(Simulate_userinput("N33-1",100))

##########################################################################################

# #%%
#LOCATION NAMES
# # Nodes IDs
# # returns a dictionary of model node names with their indices as values
# def Ex_node_ids():
#   with Output('DoLo.out') as out:
#     ids = out.nodes
#     return ids
# #########################################################################################
# #%%
# #Node Attributes -For all nodes at given time, get a particular attribute. -returns a dictionary of attribute values for all nodes at given timestep
#
# #Node Flooding Rate
# def Ex_nodeFlood_rate(node_name):
#     sim = Simulation(r"DoLo.inp")
#     nodeflood = Nodes(sim)[node_name]
#     nodfloodlst= []
#     time = []
#     sim.step_advance(60*15)       #every 15 mins
#     for step in sim:
#         nodfloodlst.append(nodeflood.flooding)
#         time.append(sim.current_time)
#     return nodfloodlst, time
#
# ####################################################################################
# #%%
# # Ponded Volume- for all nodes at a given time
#
# # For all nodes at given time, get the ponded volume.
# # returns a dictionary of attribute values for all nodes at given timestep
# def Ex_ponded_volume():
#     with Output('DoLo.out') as out:
#         data = out.node_attribute(NodeAttribute.PONDED_VOLUME, datetime(2020, 10, 15, 21))
#         node_pondvol = []
#         index_list = []
#         non_ponded = []
#         for object in data:
#             if data[object] > 0:  # only those nodes which are flooded/ponded
#                 node_pondvol.append(data[object])  # data[object] gives the ponded volume
#                 index_list.append(object)  # the object is the node name
#             else:
#                 non_ponded.append(object)
#                 # print(object, data[object])
#         return node_pondvol, index_list, non_ponded
#
# #########################################################################################
#
# #Node Time series for ponded volume. you specify the start and end time
# # Returns a dictionary of attribute values with between start_index and end_index with reporting timesteps as keys
# def Ex_node_pondedvol(node_name):
#   with Output('DoLo.out') as out:
#       ts = out.node_series(node_name, NodeAttribute.PONDED_VOLUME, datetime(2020, 10, 15, 12), datetime(2020, 10, 16, 12))
#       ts_node_pondedvol = []
#       index_list= []
#
#       for index in ts:
#         ts_node_pondedvol.append(ts[index])     #ts[index] gives the time series value of the ponded volume at node N33-1
#         index_list.append(index)                #the index is the node name
#       return ts_node_pondedvol,index_list
#
# ################################################################################
#
# # Node Attributes
# #Gets all the attributes for a node at given time.
# #returns a dictionary of attributes for a node at given timestep
#
# def Ex_node_attributes(node_name):
#   with Output('DoLo.out') as out:
#       data = out.node_result(node_name, datetime(2020, 10, 15, 21))
#       index_list= []
#       node_attr = []
#       for object in data:
#          node_attr.append(data[object])       #data[object] gives the value
#          index_list.append(object)                #the object is the node attribute
#       return node_attr, index_list
#####################################################################################################
#####################################################################################################
#HOURS THAT THE LOCATION IS FLOODED
def Ex_floodHrs():        #fn extracts number of hours a node is flooded.
    nodes= []
    flooded_hrs = []
    for num in range(758, 869):
        filteredList = []
        result = linecache.getline("swmm.rpt", num)
        list = result.split(" ")
        for element in list:
            if len(element) > 0:
                filteredList.append(element)  # append every string with greater than 0 characters (# this eliminates the empty spaces)
        nodes.append(filteredList[0])
        flooded_hrs.append(float(filteredList[1]))
    return(nodes, flooded_hrs)

#10 yr return
def Ex_floodHrs10():        #fn extracts number of hours a node is flooded.
    nodes= []
    flooded_hrs = []
    for num in range(786, 924):
        filteredList = []
        result = linecache.getline("swmm10.rpt", num)
        list = result.split(" ")
        for element in list:
            if len(element) > 0:
                filteredList.append(element)  # append every string with greater than 0 characters (# this eliminates the empty spaces)
        nodes.append(filteredList[0])
        flooded_hrs.append(float(filteredList[1]))
    return(nodes, flooded_hrs)

def Ex_NodeFloodHrs(node_name, file_name, startline,endline):        #fn extracts number of hours a node is flooded.
    nodes = []
    flooded_hrs = []
    for num in range(startline, endline):
        filteredList = []
        result = linecache.getline(file_name, num)
        list = result.split(" ")
        for element in list:
            if len(element) > 0:
                filteredList.append(element)  # append every string with greater than 0 characters (this eliminates the empty spaces)
        nodes.append(filteredList[0])
        flooded_hrs.append(float(filteredList[1]))
    index = nodes.index(node_name)              #the location of the node_name
    return flooded_hrs[index]

#10 yr return
def Ex_NodeFloodHrs10(node_name):        #fn extracts number of hours a node is flooded.
    nodes = []
    flooded_hrs = []
    for num in range(786, 924):
        filteredList = []
        result = linecache.getline("swmm10.rpt", num)
        list = result.split(" ")
        for element in list:
            if len(element) > 0:
                filteredList.append(element)  # append every string with greater than 0 characters (this eliminates the empty spaces)
        nodes.append(filteredList[0])
        flooded_hrs.append(float(filteredList[1]))
    index = nodes.index(node_name)              #the location of the node_name
    return flooded_hrs[index]

##################################################################################################
#FLOOD LEVEL/DEPTH
def Ex_Ponded_depth():
    nodes= []
    max_ponded_depth = []
    for num in range(758, 869):
        filteredList = []
        result = linecache.getline("swmm.rpt", num)
        list = result.split(" ")
        for element in list:
            if len(element) > 0:
                filteredList.append(element)  # append every string with greater than 0 characters this eliminates the empty spaces
        nodes.append(filteredList[0])
        max_ponded_depth.append(float(filteredList[6]))
    return (nodes, max_ponded_depth)

def Ex_NodePonded_depth(node_name):
    nodes= []
    max_ponded_depth = []
    for num in range(758, 869):
        filteredList = []
        result = linecache.getline("swmm.rpt", num)
        list = result.split(" ")
        for element in list:
            if len(element) > 0:
                filteredList.append(element)  # append every string with greater than 0 characters this eliminates the empty spaces
        nodes.append(filteredList[0])
        max_ponded_depth.append(float(filteredList[6]))
    index = nodes.index(node_name)                  #location of node_name
    return max_ponded_depth[index]

#10 yr return
def Ex_NodePonded_depth10(node_name):
    nodes= []
    max_ponded_depth = []
    for num in range(786, 924):
        filteredList = []
        result = linecache.getline("swmm10.rpt", num)
        list = result.split(" ")
        for element in list:
            if len(element) > 0:
                filteredList.append(element)  # append every string with greater than 0 characters this eliminates the empty spaces
        nodes.append(filteredList[0])
        max_ponded_depth.append(float(filteredList[6]))
    index = nodes.index(node_name)                  #location of node_name
    return max_ponded_depth[index]

#######################################################################################################
### TIME MAX FLOODING OCCURS
def Ex_Time_maxflood():
    nodes= []
    T_maxflood = []
    for num in range(758, 869):
        filteredList = []
        result = linecache.getline("swmm.rpt", num)
        list = result.split(" ")
        for element in list:
            if len(element) > 0:
                filteredList.append(element)  # append every string with greater than 0 characters this eliminates the empty spaces
        nodes.append(filteredList[0])
        T_maxflood.append([filteredList[3],filteredList[4]])

    return(nodes, T_maxflood)

startingDate = date(2020, 10, 14)
def Ex_Node_Time_maxflood(node_name):
    nodes= []
    T_maxflood = []
    for num in range(758, 869):
        filteredList = []
        result = linecache.getline("swmm.rpt", num)
        list = result.split(" ")
        for element in list:
            if len(element) > 0:
                filteredList.append(element)  # append every string with greater than 0 characters this eliminates the empty spaces
        nodes.append(filteredList[0])
        T_maxflood.append([str(startingDate + (timedelta(days = int(filteredList[3])))), filteredList[4]])
    index = nodes.index(node_name)  # location of node_name
    return T_maxflood[index]
#print(Ex_Node_Time_maxflood('N10-1'))
#############################################################
#### MAX FLOOD RATE
def Ex_max_floodrate():
    nodes= []
    max_floodrate = []
    for num in range(758, 868):
        filteredList = []
        result = linecache.getline("swmm.rpt", num)
        list = result.split(" ")
        for element in list:
            if len(element) > 0:
                filteredList.append(element)  # append every string with greater than 0 characters this eliminates the empty spaces
        nodes.append(filteredList[0])
        max_floodrate.append(float(filteredList[2]))
    return(nodes, max_floodrate)

def Ex_Nodemax_floodrate(node_name):
    nodes= []
    max_floodrate = []
    for num in range(758, 868):
        filteredList = []
        result = linecache.getline("swmm.rpt", num)
        list = result.split(" ")
        for element in list:
            if len(element) > 0:
                filteredList.append(element)  # append every string with greater than 0 characters this eliminates the empty spaces
        nodes.append(filteredList[0])
        max_floodrate.append(float(filteredList[2]))
    index = nodes.index(node_name)                      # location of node_name
    return max_floodrate[index]
################################################################
