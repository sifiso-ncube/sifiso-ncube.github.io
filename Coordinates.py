
import linecache
for num in range(7670, 7839):
    result = linecache.getline("swmm.inp", num)
    list= result.split(" ")
    filteredList = []
    for element in list:
        if len(element)>0:
            filteredList.append(element)  #append every string with greater than 0 characters this eliminates the empty spaces
    #print(filteredList)

    node= filteredList[0]
    x_coord = filteredList[1]
    y_coord = filteredList[2]
    #print(node)
    #print(x_coord)
    #print(y_coord)
    #print(node, x_coord, y_coord)
