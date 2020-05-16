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

    def __init__(self,cm_map,nation_cnt):
        self.cm_map=cm_map
        self.nation_cnt=nation_cnt
        self.coast_arr=["di","nb","sb","eb","wb","swc","sec","nwc","nec","nc","sc","ec","wc","ns","ew"]
        self.uninhabitable=["t","o","d"]
        self.inhabitable=["f","g","r"]
        self.map_size=50


    def get_civilized_map(self):
        """
           returns a civilized map
        """
        civ_map=self.populate_civmap()
        civ_map=self.create_cities(civ_map)
        civ_map=self.define_nations(civ_map)
        return civ_map

    def populate_civmap(self):
        civ_map=[]
        for i in range(self.map_size):
            row=[]
            for j in range(self.map_size):
                row.append({
                    'terrain':self.cm_map[i][j],
                    'poplation':self.get_basic_pop(self.cm_map[i][j]),
                    'developed':False,
                    'move_cost':1,
                    'nation':0
                    })
            civ_map.append(row)
        return civ_map

    def get_basic_pop(self,terrain):
        poplation=0
        if (terrain!="o"):
            if (terrain in self.inhabitable):
                poplation=50
            else:
                poplation=25
        return poplation

    def create_cities(self,civ_map):
        quad_split=False
        if (self.nation_cnt == 8):
            quad_split=True
        nation_num=1
        civ_map=self.make_cities(0,0,civ_map,quad_split,nation_num)
        if nation_num>2:
            nation_num+=1
        civ_map=self.make_cities(0,self.map_size/2,civ_map,quad_split,nation_num)
        nation_num+=1
        civ_map=self.make_cities(self.map_size/2,0,civ_map,quad_split,nation_num)
        if nation_num>2:
            nation_num+=1
        civ_map=self.make_cities(self.map_size/2,self.map_size/2,civ_map,quad_split,nation_num)
        return civ_map

    def make_cities(self,start_row,start_col,civ_map,quad_split,nation_num):
        civ_map=self.cities_help(int(start_row),int(start_col),civ_map,quad_split,nation_num)
        if (quad_split):
            nation_num+=4
            civ_map=self.cities_help(int(start_row),int(start_col),civ_map,quad_split,nation_num)
        return civ_map
        
    def cities_help(self,start_row,start_col,civ_map,quad_split,nation_num):
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
            cnt -=1
            size=1
            row_spot=randint(0,(self.map_size/2)-1)+start_row
            col_spot=randint(0,(self.map_size/2)-1)+start_col
            if (tiles_remaining>15):
                # rand is inclusive
                size= randint(0,15)+1
            elif (tiles_remaining>8):
                size= randint(0,8)+1
            if size >9:
                if self.verify_city(row_spot,col_spot,civ_map,2):
                    civ_map=self.place_city(size,row_spot,col_spot,civ_map,nation_num)
                    tiles_remaining-=size
            elif size >1:
                if self.verify_city(row_spot,col_spot,civ_map,1):
                    civ_map=self.place_city(size,row_spot,col_spot,civ_map,nation_num)
                    tiles_remaining-=size
            else:
                if self.verify_spot(row_spot,col_spot,civ_map):
                    civ_map=self.place_spot(row_spot,col_spot,civ_map,nation_num)
                    tiles_remaining-=1
            if cnt <1:
                break
        return civ_map

    def verify_city(self,row_spot,col_spot,civ_map,end):
        is_safe=True
        if (((row_spot-1)>=0)and((col_spot-1)>=0)and((col_spot+end)<(self.map_size-1))and((row_spot+end)<(self.map_size-1))):
            for i in range(row_spot-1,row_spot+end):
                for j in range(col_spot-1,col_spot+end):
                    if not self.verify_spot(i,j,civ_map):
                        return False
        else:
            is_safe=False
        return is_safe

    def verify_spot(self,row_spot,col_spot,civ_map):
        if civ_map[row_spot][col_spot]['terrain'] in self.inhabitable:
            if not civ_map[row_spot][col_spot]['developed']:
                return True
        return False
    
    def place_city(self,size,row_spot,col_spot,civ_map,nation_num):
        if size==2:
            civ_map=self.rand_two_spot(row_spot,col_spot,civ_map,nation_num)
        elif size==3:
            civ_map=self.rand_three_spot(row_spot,col_spot,civ_map,nation_num)
        elif size==4:
            civ_map=self.rand_four_spot(row_spot,col_spot,civ_map,nation_num)
        elif size==5:
            civ_map=self.five_spot(row_spot,col_spot,civ_map,nation_num)
        elif size==6:
            civ_map=self.rand_six_spot(row_spot,col_spot,civ_map,nation_num)
        elif size==7:
            civ_map=self.rand_seven_spot(row_spot,col_spot,civ_map,nation_num)
        elif size==8:
            civ_map=self.rand_eight_spot(row_spot,col_spot,civ_map,nation_num)
        elif size==9:
            civ_map=self.nine_spot(row_spot,col_spot,civ_map,nation_num)
        elif size==10:
            civ_map=self.ten_spot(row_spot,col_spot,civ_map,nation_num)
        elif size==11:
            civ_map=self.eleven_spot(row_spot,col_spot,civ_map,nation_num)
        elif size==12:
            civ_map=self.twelve_spot(row_spot,col_spot,civ_map,nation_num)
        elif size==13:
            civ_map=self.thirteen_spot(row_spot,col_spot,civ_map,nation_num)
        elif size==14:
            civ_map=self.fourteen_spot(row_spot,col_spot,civ_map,nation_num)
        elif size==15:
            civ_map=self.fifteen_spot(row_spot,col_spot,civ_map,nation_num)
        else:
            civ_map=self.sixteen_spot(row_spot,col_spot,civ_map,nation_num)
        return civ_map

    def rand_two_spot(self,row_spot,col_spot,civ_map,nation_num):
        """
           .x.   ...   ...   ...
           .x.   .xx   .x.   xx.
           ...   ...   .x.   ...
        """
        template=randint(0,3)
        if template==0:
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
        elif template==1:
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
        elif template==2:
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
        else:
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot,civ_map,nation_num)
        return civ_map

    def rand_three_spot(self,row_spot,col_spot,civ_map,nation_num):
        """
           .x.   .x.   .x.   ...   ...   ...
           .xx   .x.   xx.   .xx   xxx   xx.
           ...   .x.   ...   .x.   ...   .x.
        """
        template=randint(0,5)
        if template==0:
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
        elif template==1:
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
        elif template==2:
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
        elif template==3:
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
        elif template==4:
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
        else:
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot,civ_map,nation_num)
        return civ_map

    def rand_four_spot(self,row_spot,col_spot,civ_map,nation_num):
        """
           .x.   .x.   ...   .x.
           .xx   xxx   xxx   xx.
           .x.   ...   .x.   .x.
        """
        template=randint(0,3)
        if template==0:
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
        elif template==1:
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
        elif template==2:
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
        else:
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot,civ_map,nation_num)
        return civ_map

    def five_spot(self,row_spot,col_spot,civ_map,nation_num):
        """
           .x.   
           xxx   
           .x.   
        """
        civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
        civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot,civ_map,nation_num)
        return civ_map

    def rand_six_spot(self,row_spot,col_spot,civ_map,nation_num):
        """
           xx.   .xx   .x.   .x.
           xxx   xxx   xxx   xxx
           .x.   .x.   .xx   xx.
        """ 
        template=randint(0,3)
        if template==0:
            civ_map=self.place_spot(row_spot-1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
        elif template==1:
            civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
        elif template==2:
            civ_map=self.place_spot(row_spot+1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
        else:
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot,civ_map,nation_num)
        return civ_map

    def rand_seven_spot(self,row_spot,col_spot,civ_map,nation_num):
        """
           xx.   .xx   xxx   .x.   .xx   xx.
           xxx   xxx   xxx   xxx   xxx   xxx
           .xx   xx.   .x.   xxx   .xx   xx.
        """ 
        template=randint(0,5)
        if template==0:
            civ_map=self.place_spot(row_spot-1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot+1,civ_map,nation_num)
        elif template==1:
            civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
        elif template==2:
            civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
        elif template==3:
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
        elif template==4:
            civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot+1,civ_map,nation_num)
        else:
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot,civ_map,nation_num)
        return civ_map

    def rand_eight_spot(self,row_spot,col_spot,civ_map,nation_num):
        """
           .xx   xx.   xxx   xxx
           xxx   xxx   xxx   xxx
           xxx   xxx   xx.   .xx
        """ 
        template=randint(0,3)
        if template==0:
            civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot+1,civ_map,nation_num)
        elif template==1:
            civ_map=self.place_spot(row_spot-1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot+1,civ_map,nation_num)
        elif template==2:
            civ_map=self.place_spot(row_spot+1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
        else:
            civ_map=self.place_spot(row_spot+1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot+1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot,civ_map,nation_num)
        return civ_map

    def nine_spot(self,row_spot,col_spot,civ_map,nation_num):
        """
           .x.   
           xxx   
           .x.   
        """
        civ_map=self.place_spot(row_spot-1,col_spot-1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
        civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
        civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot+1,col_spot+1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot,civ_map,nation_num)
        return civ_map

    def ten_spot(self,row_spot,col_spot,civ_map,nation_num:
        """
           x.  .x  ..  ..
           ..  ..  x.  .x
        """
        template=randint(0,3)
        if template==0:
            civ_map=self.nine_spot(row_spot,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot,civ_map,nation_num)
        elif template==1:
            civ_map=self.nine_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot+1,civ_map,nation_num)
        elif template==2:
            civ_map=self.nine_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
        else:
            civ_map=self.nine_spot(row_spot+1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)
        return civ_map

    def eleven_spot(self,row_spot,col_spot,civ_map,nation_num):
        """
           x.  .x  ..  ..
           ..  ..  x.  .x
        """
        template=randint(0,3)
        if template==0:
            civ_map=self.nine_spot(row_spot,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+2,civ_map,nation_num)
        elif template==1:
            civ_map=self.nine_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
        elif template==2:
            civ_map=self.nine_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot+2,civ_map,nation_num)
        else:
            civ_map=self.nine_spot(row_spot+1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
        return civ_map

    def twelve_spot(self,row_spot,col_spot,civ_map,nation_num):
        """
           xx  x.  ..  .x
           ..  x.  xx  .x
        """
        template=randint(0,3)
        if template==0:
            civ_map=self.nine_spot(row_spot,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot+2,civ_map,nation_num)
        elif template==1:
            civ_map=self.nine_spot(row_spot,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot-1,civ_map,nation_num)
        elif template==2:
            civ_map=self.nine_spot(row_spot+1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot-1,civ_map,nation_num)
        else:
            civ_map=self.nine_spot(row_spot+1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
        return civ_map

    def thirteen_spot(self,row_spot,col_spot,civ_map,nation_num):
        """
           xxx.   .xxx   .xx.  .xx.
           xxxx   xxxx   xxxx  xxxx
           xxxx   xxxx   xxxx  xxxx
           .xx.   .xx.   .xxx  xxx.
        """
        template=randint(0,3)
        if template==0:
            civ_map=self.nine_spot(row_spot,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot+1,civ_map,nation_num)
        elif template==1:
            civ_map=self.nine_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot+1,civ_map,nation_num)
        elif template==2:
            civ_map=self.nine_spot(row_spot+1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
        else:
            civ_map=self.nine_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot+2,civ_map,nation_num)

        return civ_map

    def fourteen_spot(self,row_spot,col_spot,civ_map,nation_num):
        """
           xxx.   .xxx  
           xxxx   xxxx 
           xxxx   xxxx
           .xxx   xxx.
        """
        template=randint(0,1)
        if template==0:
            civ_map=self.nine_spot(row_spot,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot+2,civ_map,nation_num)
        else:
            civ_map=self.nine_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot+2,civ_map,nation_num)

        return civ_map

    def fifteen_spot(self,row_spot,col_spot,civ_map,nation_num):
        """
           xxxx   xxxx   .xxx  xxx.
           xxxx   xxxx   xxxx  xxxx
           xxxx   xxxx   xxxx  xxxx
           xxx.   .xxx   xxxx  xxxx
        """
        template=randint(0,3)
        if template==0:
            civ_map=self.nine_spot(row_spot,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot+1,civ_map,nation_num)
        elif template==1:
            civ_map=self.nine_spot(row_spot,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+2,col_spot+2,civ_map,nation_num)
        elif template==2:
            civ_map=self.nine_spot(row_spot+1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot+2,civ_map,nation_num)
        else:
            civ_map=self.nine_spot(row_spot+1,col_spot+1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot+1,col_spot+2,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot-1,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
            civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)

        return civ_map

    def sixteen_spot(self,row_spot,col_spot,civ_map,nation_num):
        """
           xxx   
           xxx   
           xxx   
        """
        civ_map=self.place_spot(row_spot-1,col_spot-1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot+1,col_spot-1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot-1,col_spot,civ_map,nation_num)
        civ_map=self.place_spot(row_spot+1,col_spot,civ_map,nation_num)
        civ_map=self.place_spot(row_spot-1,col_spot+1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot+1,col_spot+1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot-1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot+1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot,civ_map,nation_num)
        civ_map=self.place_spot(row_spot+2,col_spot-1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot+2,col_spot,civ_map,nation_num)
        civ_map=self.place_spot(row_spot+2,col_spot+1,civ_map,nation_num)
        civ_map=self.place_spot(row_spot+2,col_spot+2,civ_map,nation_num)
        civ_map=self.place_spot(row_spot+1,col_spot+2,civ_map,nation_num)
        civ_map=self.place_spot(row_spot,col_spot+2,civ_map,nation_num)
        civ_map=self.place_spot(row_spot-1,col_spot+2,civ_map,nation_num)
        return civ_map

    def place_spot(self,row_spot,col_spot,civ_map,nation_num):
        civ_map[row_spot][col_spot]['developed']=True
        iv_map[row_spot][col_spot]['nation']=nation_num
        return civ_map

    def define_nations(self,civ_map):
        return civ_map