from random import randint
import collections
import logging


class City_Maker:
	"""
	  cities cannot be built on oceans, coast or mountains
	  verify with natural map and against civilized map that city size is placeable
	  small is 1, medium is 2-9 and large is 10-16 tiles in size
	  - For two nations each has 32 tiles in 2 quadrants (64 per nation)
	  - For four nations each has 32 tiles in 1 quadrant (32 per nation)
	  - For eight nations each has 16 tiles in 1 quadrant (16 per nation) 
	"""
    coast_arr=["di","nb","sb","eb","wb","swc","sec","nwc","nec","nc","sc","ec","wc","ns","ew"]
    uninhabitable=["t","o","d"]
    inhabitable=["f","g","r"]
    map_size=50


    def __init__(self,cm_map,nation_cnt):
    	self.cm_map=cm_map
    	self.nation_cnt=nation_cnt

    def get_civilized_map(self,nation_cnt):
    	"""
    	   returns a civilized map
    	"""
    	civ_map=populate_civmap()
    	civ_map=create_cities(civ_map)
    	civ_map=define_nations(civ_map)
    	return civ_map

    def populate_civmap(self):
    	civ_map=[]
    	for i in range(map_size):
            row=[]
            for j in range(map_size):
                row.append({
                	'terrain':self.cm_map[i][j],
                	'poplation':get_basic_pop(self.cm_map[i][j]),
                	'developed':False,
                	'move_cost':1,
                	'nation':'none'
                	})
                civ_map.append(row)
        return civ_map

    def get_basic_pop(terrain):
    	poplation=0
    	if (terrain!="o"):
            if (terrain in self.inhabitable):
            	poplation=50
            else:
            	poplation=25
        return poplation

    def create_cities(civ_map):
    	quad_split=False
    	if (self.nation_cnt == 8):
    		quad_split=True
    	civ_map=make_cities(0,0,civ_map,quad_split)
        civ_map=make_cities(0,map_size/2,civ_map,quad_split)
        civ_map=make_cities(map_size/2,0,civ_map,quad_split)
        civ_map=make_cities(map_size/2,map_size/2,civ_map,quad_split)
        return civ_map

    def make_cities(start_row,start_col,civ_map,quad_split):
    	civ_map=cities_help(start_row,start_col,civ_map,quad_split)
    	if (quad_split):
            civ_map=cities_help(start_row,start_col,civ_map,quad_split)
    	return civ_map
        
    def cities_help(start_row,start_col,civ_map,quad_split):
    	"""
    	   - small city is 1 tile
    	   - medium city is 2-9 tiles
    	   - large city is 10-16 tiles
    	"""
    	tiles_remaining=32
    	if (quad_split):
    		tiles_remaining=16
    	cnt=100
    	while tiles_remaining>1:
    		size=1
    		if (tiles_remaining>15):
    			# is rand in inclusive
                size= randint(0,16)
            elif (tiles_remaining>8):
            	size= randint(0,9)
    		row_spot=randint(0,(map_size/2)-1)+start_row
    		col_spot=randint(0,(map_size/2)-1)+start_col
    	return civ_map

    def define_nations(civ_map):
    	return civ_map