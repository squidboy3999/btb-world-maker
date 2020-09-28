from random import randint
import collections
import logging
import resolve_cm_tile
from make_continent_image import build_map_image
from make_civilized_layer import City_Maker
from nation_creation import Nation_Maker

Map_info=collections.namedtuple('Map_info',['cm_map','used_templates'])
Quad_info=collections.namedtuple('Quad_info',['quad_template','used_templates'])

size =50
template_cnt=8

def get_new_cm_map():
    cm_map=init_cm_map()
    # templates should only be used once per continent
    used_templates=[]
    map_info=get_rand_nw_cm_map(cm_map,used_templates)
    map_info=get_rand_ne_cm_map(map_info.cm_map,map_info.used_templates)
    map_info=get_rand_sw_cm_map(map_info.cm_map,map_info.used_templates)
    map_info=get_rand_se_cm_map(map_info.cm_map,map_info.used_templates)
    print_map(map_info.cm_map)
    cm_map=resolve_cm_tile.set_cm_map_values(map_info.cm_map)
    print_natural_map(cm_map)
    build_map_image(cm_map)
    civ_m_inst=City_Maker(cm_map,8)
    civ_m=civ_m_inst.get_civilized_map()
    print_cities(civ_m)
    nation_map_inst=Nation_Maker(civ_m,civ_m_inst.unclaimed_land,civ_m_inst.cities)
    nation_map=nation_map_inst.assign_territory()
    nation_map_inst.print_cm_map()
    nation_map_inst.map_to_file()

def print_cities(cm_map):
    cnt=0
    for i in range(50):
        row=""
        for j in range(50):
            sym = "."
            if (cm_map[i][j]['developed']):
                sym = "E"
                cnt+=1
            row=row+" "+sym
        print(row)
    print(cnt)

def print_map(cm_map):
    for i in range(50):
        row=""
        for j in range(50):
            sym = " "
            if (cm_map[i][j]!="o"):
                sym = "X"
            row=row+" "+sym
        print(row)

def print_natural_map(cm_map):
    map_key={"f":"#",
             "g":"\"",
             "d":"*",
             "t":"M",
             "r":"~"}
    coast_arr=["di","nb","sb","eb","wb","swc","sec","nwc","nec","nc","sc","ec","wc","ns","ew"]
    for i in range(50):
        row=""
        for j in range(50):
            sym = " "
            if (cm_map[i][j]!="o"):
                if cm_map[i][j] in coast_arr:
                    sym="."
                else:
                    sym=map_key[cm_map[i][j]]
            row=row+" "+sym
        print(row)

def init_cm_map():
    cm_map=[]
    for i in range(50):
        row=[]
        for j in range(50):
            row.append("o")
        cm_map.append(row)
    return cm_map

def get_rand_cm_map_quad(used_templates):
    """ Selects a random northwest oriented continent map template

        Return Array of rows, which are arrays of values per column 
        [row[column]], these are alphanumeric values representing ocean, coastline 
        and undefined land.
    """

    #randint is inclusive range a <= N <= b
    template_num=randint(0,template_cnt-1)
    cnt=0
    while template_num in used_templates:
        template_num=randint(0,template_cnt-1)
        cnt += 1
        if cnt ==100:
            break
    print("Template Number: {}".format(template_num))
    used_templates.append(template_num)
    # no switches in python :( 
    if template_num == 0:
        return Quad_info(get_template0(),used_templates)
    elif template_num == 1:
        return Quad_info(get_template1(),used_templates)
    elif template_num == 2:
        return Quad_info(get_template2(),used_templates)
    elif template_num == 3:
        return Quad_info(get_template3(),used_templates)
    elif template_num == 4:
        return Quad_info(get_template4(),used_templates)
    elif template_num == 5:
        return Quad_info(get_template5(),used_templates)
    elif template_num == 6:
        return Quad_info(get_template6(),used_templates)
    else:
        return Quad_info(get_template7(),used_templates)


def get_rand_nw_cm_map(cm_map,used_templates):
    """ Selects a random northwest oriented continent map template using the
        get_rand_cm_map as a helper method

        Return Array of rows, which are arrays of values per column 
        [row[column]], these are alphanumeric values representing ocean, coastline 
        and undefined land.
    """
    quad_info=get_rand_cm_map_quad(used_templates)
    template=quad_info.quad_template
    for i in range(25):
        for j in range(25):
            cm_map[i][j]=template[i][j]
    return Map_info(cm_map,quad_info.used_templates)

def get_rand_ne_cm_map(cm_map,used_templates):
    """ Selects a random northeast oriented continent map template using the
        get_rand_cm_map as a helper method 

        Return Array of rows, which are arrays of values per column 
        [row[column]], these are alphanumeric values representing ocean, coastline 
        and undefined land.
    """
    quad_info=get_rand_cm_map_quad(used_templates)
    template=quad_info.quad_template
    for i in range(25):
        for j in range(25):
            new_j=49-j
            cm_map[i][new_j]=template[i][j]
    return Map_info(cm_map,quad_info.used_templates)

def get_rand_sw_cm_map(cm_map,used_templates):
    """ Selects a random southwest oriented continent map template using the
        get_rand_cm_map as a helper method 

        Return Array of rows, which are arrays of values per column 
        [row[column]], these are alphanumeric values representing ocean, coastline 
        and undefined land.
    """
    quad_info=get_rand_cm_map_quad(used_templates)
    template=quad_info.quad_template
    for i in range(25):
        for j in range(25):
            new_i=49-i
            cm_map[new_i][j]=template[i][j]
    return Map_info(cm_map,quad_info.used_templates)

def get_rand_se_cm_map(cm_map,used_templates):
    """ Selects a random southwest oriented continent map template using the
        get_rand_cm_map as a helper method 

        Return Array of rows, which are arrays of values per column 
        [row[column]], these are alphanumeric values representing ocean, coastline 
        and undefined land.
    """
    quad_info=get_rand_cm_map_quad(used_templates)
    template=quad_info.quad_template
    for i in range(25):
        for j in range(25):
            new_i=49-i
            new_j=49-j
            cm_map[new_i][new_j]=template[i][j]
    return Map_info(cm_map,quad_info.used_templates)

def get_template0():
    """ o is ocean, c is coast, u is undefined land - This is used to describe 
        each row
    
        Return Array of rows, which are arrays of values per column 
        [row[column]], these are alphanumeric values representing ocean, coastline 
        and undefined land.
    """
    o="o"
    c="c"
    u="u"
    map=[]
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,c,c,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,c,c,c,c,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,c,u,c,c,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,c,u,u,u,c,o,o,o,o,o,o,o,o,o,c])
    map.append([o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,c,c,o,o,o,o,o,o,c,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,c,c,c,c,o,c,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,c,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,c,c,c,o,o,o,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,c,c,o,o,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,c,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])

    return map

def get_template1():
    """ o is ocean, c is coast, u is undefined land - This is used to describe 
        each row

        Return Array of rows, which are arrays of values per column 
        [row[column]], these are alphanumeric values representing ocean, coastline 
        and undefined land.
    """
    o="o"
    c="c"
    u="u"
    map=[]
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,c,c,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,c,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,c,c,u,u,c,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,c,o,o,c])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,c,o,c])
    map.append([o,o,o,o,o,o,o,o,o,o,c,c,c,c,c,c,u,u,u,u,u,u,c,o,c])
    map.append([o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,c,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,c,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,c,c,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])

    return map

def get_template2():
    """ o is ocean, c is coast, u is undefined land - This is used to describe 
        each row

        Return Array of rows, which are arrays of values per column 
        [row[column]], these are alphanumeric values representing ocean, coastline 
        and undefined land.
    """
    o="o"
    c="c"
    u="u"
    map=[]
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u])
    map.append([o,o,o,o,o,o,o,c,c,c,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u])
    map.append([o,o,o,o,o,o,c,u,u,u,c,o,o,o,c,c,c,o,o,o,c,u,u,u,u])
    map.append([o,o,o,o,o,c,u,u,u,u,u,c,c,c,u,u,u,c,c,c,u,u,u,u,u])
    map.append([o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,u,u,u,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,c,c,c,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])

    return map

def get_template3():
    """ o is ocean, c is coast, u is undefined land - This is used to describe 
        each row

        Return Array of rows, which are arrays of values per column 
        [row[column]], these are alphanumeric values representing ocean, coastline 
        and undefined land.
    """
    o="o"
    c="c"
    u="u"
    map=[]
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,c,o,o,c])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,c,u,u,c,c,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,c,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,c,c,o,o,c,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,c,u,c,c,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,c,c,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,c,u,u,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])

    return map

def get_template4():
    """ o is ocean, c is coast, u is undefined land - This is used to describe 
        each row

        Return Array of rows, which are arrays of values per column 
        [row[column]], these are alphanumeric values representing ocean, coastline 
        and undefined land.
    """
    o="o"
    c="c"
    u="u"
    map=[]
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,c,c,c,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,c,c,o,o,c,c,u,u,u,c,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,c,u,u,c,c,u,u,u,u,u,u,c,c,c,c,o,o,c,c,c,o,o,o])
    map.append([o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,c,c,u,u,u,c,c,c])
    map.append([o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,c,u,u,u,u,u,u,u,c,c,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,c,u,u,c,u,u,u,c,o,o,c,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,c,c,o,c,u,c,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,c,c,o,o,c,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,c,o,o,o,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])

    return map

def get_template5():
    """ o is ocean, c is coast, u is undefined land - This is used to describe 
        each row

        Return Array of rows, which are arrays of values per column 
        [row[column]], these are alphanumeric values representing ocean, coastline 
        and undefined land.
    """
    o="o"
    c="c"
    u="u"
    map=[]
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,c,c,c])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,o,o,c,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,c,c,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,c,c,c,c,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])

    return map

def get_template6():
    """ o is ocean, c is coast, u is undefined land - This is used to describe 
        each row

        Return Array of rows, which are arrays of values per column 
        [row[column]], these are alphanumeric values representing ocean, coastline 
        and undefined land.
    """
    o="o"
    c="c"
    u="u"
    map=[]
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,c,c,c,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,c,u,u,c,c,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,c,u,u,u,c,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,c,u,u,c,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,c,o,o,o,o,o,c,u,u,c,o,o,o,o,o,c,o,o,o,o,o,c])
    map.append([o,o,c,u,c,c,o,o,o,o,c,u,c,o,o,o,o,c,u,c,c,o,o,c,u])
    map.append([o,c,u,u,u,u,c,o,o,o,o,c,u,c,o,o,c,u,u,c,o,o,c,u,u])
    map.append([o,o,c,u,u,u,u,c,c,o,o,c,u,c,o,c,u,u,c,o,o,o,c,u,u])
    map.append([o,o,o,c,u,u,u,u,u,c,c,u,u,c,c,u,u,u,c,o,o,c,u,u,u])
    map.append([o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,c,o,c,u,u,u])
    map.append([o,o,o,o,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,c,u,u,u,u])
    map.append([o,o,o,o,o,o,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])

    return map


def get_template7():
    """ o is ocean, c is coast, u is undefined land - This is used to describe 
        each row

        Return Array of rows, which are arrays of values per column 
        [row[column]], these are alphanumeric values representing ocean, coastline 
        and undefined land.
    """
    o="o"
    c="c"
    u="u"
    map=[]
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,o,o,o,o,o,o,o,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,c,o,o,o,c,c,c,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,c,o,o,c,u,u,c,o,o])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,u,c,c,u,u,u,u,c,c])
    map.append([o,o,o,o,o,o,o,o,o,o,o,o,o,o,c,c,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,o,c,c,c,c,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,o,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,c,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])
    map.append([o,o,o,o,o,c,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u,u])

    return map
