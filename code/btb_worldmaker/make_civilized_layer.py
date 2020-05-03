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


    def __init__(self,cm_map,nation_cnt):
    	self.cm_map=cm_map
    	self.nation_cnt=nation_cnt

    def get_civilized_map(self,nation_cnt):
    	"""
    	   returns a civilized map
    	"""
    	civ_map=populate_civmap()
    	civ_map=create_cities(civ_map)
    	return civ_map

    def populate_civmap(self):
    	civ_map=[]
    	for i in range(50):
            row=[]
            for j in range(50):
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
        pass