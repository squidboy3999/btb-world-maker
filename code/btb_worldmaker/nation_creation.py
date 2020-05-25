import collections
import logging
import queue


class Nation_Maker:
    """
      cities cannot be built on oceans, coast or mountains
      verify with natural map and against civilized map that city size is placeable
      small is 1, medium is 2-9 and large is 10-16 tiles in size
      - For two nations each has 32 tiles in 2 quadrants (64 per nation)
      - For four nations each has 32 tiles in 1 quadrant (32 per nation)
      - For eight nations each has 16 tiles in 1 quadrant (16 per nation) 
    """

    def __init__(self,cm_map,land_cnt,cities):
        self.cm_map=cm_map
        self.land_cnt=land_cnt
        self.cities_a=cities
        self.cities_b=queue.Queue()
        self.map_size=50

    def assign_territory(self):
        cur_q="a"
        cnt=0
        while self.land_cnt >0:
            cnt+=1
            if cur_q=="a":
                while not self.cities_a.empty():
                    cur_city_spot=self.cities_a.get()
                    self.cities_b.put(cur_city_spot)
                    self.claim_territory(cur_city_spot)
                    if self.land_cnt >0:
                        return self.cm_map
                cur_q="b"
            else:
                while not self.cities_b.empty():
                    cur_city_spot=self.cities_b.get()
                    self.cities_a.put(cur_city_spot)
                    self.claim_territory(cur_city_spot)
                    if self.land_cnt >0:
                        return self.cm_map
                cur_q="a"
            if cnt > 2500:
                print('Land Claim Defect')
                return self.cm_map
        print('Appears to be no unclaimed land')
        return self.cm_map

    def print_cm_map(self):
        for i in range(self.map_size):
            line =""
            for j in range(self.map_size):
                line=line+str(self.cm_map[i][j]["nation"])+" "
            print(line)

    def claim_territory(self,cur_city_spot):
        for i in range(self.map_size):
            if self.place_in_radius(i,cur_city_spot):
                return
        print ("Land count doesn't seem to match reality!")

    def place_in_radius(self,radius,city_spot):
        if len(city_spot)==2:
            row=city_spot[0]
            col=city_spot[1]
            nation=self.cm_map[row][col]["nation"]
            if self.try_corners(city_spot,radius,nation):
                return True
            elif self.try_nw_se_vector(city_spot,[-radius,0],radius,nation):
                return True
            elif self.try_nw_se_vector(city_spot,[0,-radius],radius,nation):
                return True
            elif self.try_sw_ne_vector(city_spot,[0,-radius],radius,nation):
                return True
            elif self.try_sw_ne_vector(city_spot,[radius,0],radius,nation):
                return True
            return False
        else:
            print("City spot does not contain 2 item list: {}".format(city_spot)) 

    def try_corners(self,city_spot,radius,nation):
        if self.try_spot([radius,0],city_spot,nation):
            return True
        elif self.try_spot([-radius,0],city_spot,nation):
            return True
        elif self.try_spot([0,radius],city_spot,nation):
            return True
        elif self.try_spot([0,-radius],city_spot,nation):
            return True
        else:
            return False

    def try_nw_se_vector(self,city_spot,modifier,radius,nation):
        if radius==2:
            if self.try_spot([modifier[0]-1,modifier[1]+1],city_spot,nation):
                return True
            else:
                return False
        else:
            for i in range(1,radius-1):
                if self.try_spot([modifier[0]-i,modifier[1]+i],city_spot,nation):
                    return True
            return False

    def try_sw_ne_vector(self,city_spot,modifier,radius,nation):
        if radius==2:
            if self.try_spot([modifier[0]+1,modifier[1]+1],city_spot,nation):
                return True
            else:
                return False
        else:
            for i in range(1,radius-1):
                if self.try_spot([modifier[0]+i,modifier[1]+i],city_spot,nation):
                    return True
            return False

    def try_spot(self,modifier,city_spot,nation):
        row=city_spot[0]+modifier[0]
        col=city_spot[1]+modifier[1]
        if self.cm_map[row][col]["terrain"] != "o" and self.cm_map[row][col]["nation"] == 0:
            self.cm_map[row][col]["nation"]=nation
            self.land_cnt-=1
            return True
        else:
            print("location row - {} col - {} -not set".format(row,col))
            return False