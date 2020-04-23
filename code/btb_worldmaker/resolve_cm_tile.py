from random import randint

u="u"
o="o"
c="c"
g="g"
f="f"
# marsh
r="r"
# mountain
t="t"
d="d"
coast_neighbors=[g,g,g,g,g,g,f,f,r,t]
grass_neighbors=[g,g,g,g,g,g,g,g,g,g,g,g,f,f,f,f,d,d,r,t]
marsh_neighbors=[r,r,r,r,r,r,r,r,r,r,r,r,f,f,f,g,g,g,t,d]
mountain_neighbors=[t,t,t,t,t,t,t,t,t,t,t,t,f,f,f,d,d,d,r,g]
forest_neighbors=[f,f,f,f,f,f,f,f,f,f,f,f,f,g,g,g,t,t,r,r,d]
desert_neighbors=[d,d,d,d,d,d,d,d,d,d,d,d,g,g,g,t,t,t,r,f]

def set_cm_map_values(cm_map):
    for i in range(50):
        for j in range(50):
            if(cm_map[i][j]==c or cm_map[i][j]==u):
                cm_map[i][j]=resolve_cm_space(cm_map,i,j)
    return cm_map

def resolve_cm_space(cm_map,i,j):
    north=u
    south=u
    east=u
    west=u
    if(i-1>=0):
        north=cm_map[i-1][j]
    if(i+1<=49):
        south=cm_map[i+1][j]
    if(j-1>=0):
        west=cm_map[i][j-1]
    if(j+1<=49):
        east=cm_map[i][j+1]
    if(north==o or south==o or east==o or west==o):
        return resolve_beach(north,south,east,west)
    elif is_near_beach(north,south,east,west):
        return coast_neighbors[randint(0,len(coast_neighbors)-1)]
    else:
        options=[]
        options=add_option(options,north)
        options=add_option(options,south)
        options=add_option(options,east)
        options=add_option(options,west)
        if(len(options)==0):
            print("No Options from neighbors, this should never happen!")
            return 'g'
        else:
            return options[randint(0,len(options)-1)]

def resolve_beach(n,s,e,w):
    ocean_loc=""
    if n==o:
        ocean_loc = ocean_loc+o
    else:
        ocean_loc = ocean_loc+u
    if s==o:
        ocean_loc = ocean_loc+o
    else:
        ocean_loc = ocean_loc+u
    if e==o:
        ocean_loc = ocean_loc+o
    else:
        ocean_loc = ocean_loc+u
    if w==o:
        ocean_loc = ocean_loc+o
    else:
        ocean_loc = ocean_loc+u
    # does not include uuoo and oouu, these should never happen
    coast_dict={"oooo": "di",
          "uooo":"nb",
          "ouoo":"sb",
          "oouo":"eb",
          "ooou":"wb",
          "uouo":"swc",
          "uoou":"sec",
          "ouuo":"nwc",
          "ouou":"nec",
          "ouuu":"nc",
          "uouu":"sc",
          "uuou":"ec",
          "uuuo":"wc",
          "uuoo":"ns",
          "oouu":"ew"}
    return coast_dict[ocean_loc]

def is_near_beach(n,s,e,w):
    cases=["c","di","nb","sb","eb","wb","swc","sec","nwc","nec","nc","sc","ec","wc","ns","ew"]
    if(n in cases or s in cases or e in cases or w in cases):
        return True
    else:
        return False

def add_option(options,neighbor):
    if neighbor==u:
        return options
    elif neighbor==g:
        return grass_neighbors[randint(0,len(grass_neighbors)-1)]
    elif neighbor==f:
        return forest_neighbors[randint(0,len(forest_neighbors)-1)]
    elif neighbor==d:
        return desert_neighbors[randint(0,len(desert_neighbors)-1)]
    elif neighbor==r:
        return marsh_neighbors[randint(0,len(marsh_neighbors)-1)]
    elif neighbor==t:
        return mountain_neighbors[randint(0,len(mountain_neighbors)-1)]
    else:
        print("Invalid neighbor - {} - used in add_option function".format(neighbor))
        return grass_neighbors[randint(0,len(grass_neighbors)-1)]
