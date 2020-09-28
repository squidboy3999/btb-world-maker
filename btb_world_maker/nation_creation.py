import collections
import logging
import queue
import json

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
        self.nm_logger=logging.getLogger('')
        # handlers
        c_handler =logging.StreamHandler()
        f_handler = logging.FileHandler('nation_maker.log')
        self.nm_logger.setLevel(logging.INFO)
        # formatters
        c_format=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(c_format)
        # add handlers
        self.nm_logger.addHandler(c_handler)
        self.nm_logger.addHandler(f_handler)
        self.nm_logger.info('--- Logger Initilialized ---')

    def assign_territory(self):
        cur_q="a"
        cnt=0
        while self.land_cnt >0:
            cnt+=1
            self.nm_logger.info('Remaining land count: {}'.format(self.land_cnt))
            if cur_q=="a":
                while not self.cities_a.empty():
                    cur_city_spot=self.cities_a.get()
                    self.cities_b.put(cur_city_spot)
                    self.claim_territory(cur_city_spot)
                    if self.land_cnt <1:
                        return self.cm_map
                cur_q="b"
            else:
                while not self.cities_b.empty():
                    cur_city_spot=self.cities_b.get()
                    self.cities_a.put(cur_city_spot)
                    self.claim_territory(cur_city_spot)
                    if self.land_cnt <1:
                        return self.cm_map
                cur_q="a"
            if cnt > 2500:
                print('Land Claim Defect')
                return self.cm_map
        print('Appears to be no unclaimed land')
        return self.cm_map
    
    def map_to_file(self):
        with open('cm_map.json','w') as fp:
            json.dump(self.cm_map, fp,indent=4)

    def print_cm_map(self):
        cnt_1=0
        cnt_2=0
        cnt_3=0
        cnt_4=0
        cnt_5=0
        cnt_6=0
        cnt_7=0
        cnt_8=0
        for i in range(self.map_size):
            line =""
            for j in range(self.map_size):
                line=line+str(self.cm_map[i][j]["nation"])+" "
                if self.cm_map[i][j]["nation"]==1:
                    cnt_1+=1
                elif self.cm_map[i][j]["nation"]==2:
                    cnt_2+=1 
                elif self.cm_map[i][j]["nation"]==3:
                    cnt_3+=1
                elif self.cm_map[i][j]["nation"]==4:
                    cnt_4+=1
                elif self.cm_map[i][j]["nation"]==5:
                    cnt_5+=1 
                elif self.cm_map[i][j]["nation"]==6:
                    cnt_6+=1
                elif self.cm_map[i][j]["nation"]==7:
                    cnt_7+=1
                elif self.cm_map[i][j]["nation"]==8:
                    cnt_8+=1
            print(line)
        self.nm_logger.info('Count for nation 1: {}'.format(cnt_1))
        self.nm_logger.info('Count for nation 2: {}'.format(cnt_2))
        self.nm_logger.info('Count for nation 3: {}'.format(cnt_3))
        self.nm_logger.info('Count for nation 4: {}'.format(cnt_4))
        self.nm_logger.info('Count for nation 5: {}'.format(cnt_5))
        self.nm_logger.info('Count for nation 6: {}'.format(cnt_6))
        self.nm_logger.info('Count for nation 7: {}'.format(cnt_7))
        self.nm_logger.info('Count for nation 8: {}'.format(cnt_8))

    def claim_territory(self,cur_city_spot):
        for i in range(self.map_size):
            if self.place_in_radius(i,cur_city_spot):
                return
        print ("Land count doesn't seem to match reality!")

    def place_in_radius(self,radius,city_spot):
        if len(city_spot)==2:

            row=city_spot[0]
            col=city_spot[1]
            self.nm_logger.info('--- Place in radius: {} - row: {} , col: {} ---'.format(radius,row,col))
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
        if row < self.map_size and col < self.map_size and row >=0 and col >=0:
            if self.cm_map[row][col]["terrain"] != "o" and self.cm_map[row][col]["nation"] == 0:
                self.cm_map[row][col]["nation"]=nation
                self.land_cnt-=1
                return True
            else:
                print("location row - {} col - {} -not set".format(row,col))
                return False
        else:
            print("location row - {} col - {} -out of bounds".format(row,col))
            return False
