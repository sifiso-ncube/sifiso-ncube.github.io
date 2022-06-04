
import linecache            # a module that allows us to read any line.
#import matplotlib.pyplot as plt
# flooding refers to all water that overflows a node whether it ponds or not.
def Ex_floodHrs():        #number of hours a node is flooded.
    nodes= []
    flooded_hrs = []

    for num in range(758, 869):
        filteredList = []
        result = linecache.getline("swmm.rpt", num)
        list = result.split(" ")
        for element in list:
            if len(element) > 0:
                filteredList.append(element)  # append every string with greater than 0 characters this eliminates the empty spaces
        nodes.append(filteredList[0])
        flooded_hrs.append(float(filteredList[1]))
    return(nodes, flooded_hrs)

nodes, flooded_hrs = Ex_floodHrs()
print(nodes, flooded_hrs)

############################################################
# def Ex_flooding():
#     nodes= []
#     flooded_hrs = []
#     max_floodrate = []
#     T_maxflood = []
#     max_ponded_depth = []
#     for num in range(758, 869):
#         filteredList = []
#         result = linecache.getline("swmm.rpt", num)
#         list = result.split(" ")
#         for element in list:
#             if len(element) > 0:
#                 filteredList.append(element)  # append every string with greater than 0 characters this eliminates the empty spaces
#         nodes.append(filteredList[0])
#         flooded_hrs.append(float(filteredList[1]))
#         max_floodrate.append(float(filteredList[2]))
#         T_maxflood.append([float(filteredList[3]),float(filteredList[4])])
#         max_ponded_depth.append(float(filteredList[6]))
#     return(nodes, flooded_hrs) #max_floodrate,T_maxflood,max_ponded_depth)
#
#
#         #node = filteredList[0]
#         #hours_flooded = filteredList[1]
# nodes, flooded_hrs = Ex_flooding()
# print(nodes, flooded_hrs)
# font = {'family': 'serif',
#         'color': 'darkred',
#         'weight': 'normal',
#         'size': 16,
#         }
# plt.figure(figsize=[20, 6])
# plt.bar(nodes, flooded_hrs, label='$ Hours Flooded $')
# plt.xlabel("\n Nodes ", fontdict=font)
# plt.ylabel("\n Hours Flooded", fontdict=font)
# plt.title("Hours of Flooding \n", fontdict=font)
# plt.xticks(rotation='vertical')
# plt.legend()
# plt.show()