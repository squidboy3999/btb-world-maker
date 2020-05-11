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
        civ_map=make_cities(0,0,civ_map,quad_split)
        civ_map=make_cities(0,self.map_size/2,civ_map,quad_split)
        civ_map=make_cities(self.map_size/2,0,civ_map,quad_split)
        civ_map=make_cities(self.map_size/2,self.map_size/2,civ_map,quad_split)
        return civ_map

    def make_cities(self,start_row,start_col,civ_map,quad_split):
        civ_map=cities_help(start_row,start_col,civ_map,quad_split)
        if (quad_split):
            civ_map=cities_help(start_row,start_col,civ_map,quad_split)
        return civ_map
        
    def cities_help(self,start_row,start_col,civ_map,quad_split):
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
                if verify_city(row_spot,col_spot,civ_map,2):
                    civ_map=place_city(size,row_spot,col_spot,civ_map)
                    tiles_remaining-=size
            elif size >1:
                if verify_city(row_spot,col_spot,civ_map,1):
                    civ_map=place_city(size,row_spot,col_spot,civ_map)
                    tiles_remaining-=size
            else:
                if verify_spot(row_spot,col_spot,civ_map):
                    civ_map=place_spot(row_spot,col_spot,civ_map)
                    tiles_remaining-=1
            if cnt <1:
                break
        return civ_map

    def verify_city(self,row_spot,col_spot,civ_map,end):
        is_safe=True
        if (((row_spot-1)>=0)and((col_spot-1)>=0)and((col_spot+end)<(map_size-1))and((row_spot+end)<(map_size-1))):
            for i in range(row_spot-1,row_spot+end):
                for j in range(col_spot-1,col_spot+end):
                    if not verify_spot(i,j,civ_map):
                        return False
        else:
            is_safe=False
        return is_safe

    def verify_spot(self,row_spot,col_spot,civ_map):
        if civ_map[row_spot][col_spot].terrain in self.inhabitable:
            if not civ_map[row_spot][col_spot].developed:
                return True
        return False
    
    def place_city(self,size,row_spot,col_spot,civ_map):
        if size==2:
            civ_map=rand_two_spot(row_spot,col_spot,civ_map)
        elif size==3:
            civ_map=rand_three_spot(row_spot,col_spot,civ_map)
        elif size==4:
            civ_map=rand_four_spot(row_spot,col_spot,civ_map)
        elif size==5:
            civ_map=five_spot(row_spot,col_spot,civ_map)
        elif size==6:
            civ_map=rand_six_spot(row_spot,col_spot,civ_map)
        elif size==7:
            civ_map=rand_seven_spot(row_spot,col_spot,civ_map)
        elif size==8:
            civ_map=rand_eight_spot(row_spot,col_spot,civ_map)
        elif size==9:
            civ_map=nine_spot(row_spot,col_spot,civ_map)
        elif size==10:
            civ_map=ten_spot(row_spot,col_spot,civ_map)
        elif size==11:
            civ_map=eleven_spot(row_spot,col_spot,civ_map)
        elif size==12:
            civ_map=twelve_spot(row_spot,col_spot,civ_map)
        elif size==13:
            civ_map=thirteen_spot(row_spot,col_spot,civ_map)
        elif size==14:
            civ_map=fourteen_spot(row_spot,col_spot,civ_map)
        elif size==15:
            civ_map=fifteen_spot(row_spot,col_spot,civ_map)
        else:
            civ_map=sixteen_spot(row_spot,col_spot,civ_map)
        return civ_map

    def rand_two_spot(self,row_spot,col_spot,civ_map):
        """
           .x.   ...   ...   ...
           .x.   .xx   .x.   xx.
           ...   ...   .x.   ...
        """
        template=randint(0,3)
        if template==0:
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
        elif template==1:
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
        elif template==2:
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
        else:
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
        civ_map=place_spot(row_spot,col_spot,civ_map)
        return civ_map

    def rand_three_spot(self,row_spot,col_spot,civ_map):
        """
           .x.   .x.   .x.   ...   ...   ...
           .xx   .x.   xx.   .xx   xxx   xx.
           ...   .x.   ...   .x.   ...   .x.
        """
        template=randint(0,5)
        if template==0:
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
        elif template==1:
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
        elif template==2:
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
        elif template==3:
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
        elif template==4:
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
        else:
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
        civ_map=place_spot(row_spot,col_spot,civ_map)
        return civ_map

    def rand_four_spot(self,row_spot,col_spot,civ_map):
        """
           .x.   .x.   ...   .x.
           .xx   xxx   xxx   xx.
           .x.   ...   .x.   .x.
        """
        template=randint(0,3)
        if template==0:
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
        elif template==1:
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
        elif template==2:
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
        else:
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
        civ_map=place_spot(row_spot,col_spot,civ_map)
        return civ_map

    def five_spot(self,row_spot,col_spot,civ_map):
        """
           .x.   
           xxx   
           .x.   
        """
        civ_map=place_spot(row_spot-1,col_spot,civ_map)
        civ_map=place_spot(row_spot+1,col_spot,civ_map)
        civ_map=place_spot(row_spot,col_spot-1,civ_map)
        civ_map=place_spot(row_spot,col_spot+1,civ_map)
        civ_map=place_spot(row_spot,col_spot,civ_map)
        return civ_map

    def rand_six_spot(self,row_spot,col_spot,civ_map):
        """
           xx.   .xx   .x.   .x.
           xxx   xxx   xxx   xxx
           .x.   .x.   .xx   xx.
        """ 
        template=randint(0,3)
        if template==0:
            civ_map=place_spot(row_spot-1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
        elif template==1:
            civ_map=place_spot(row_spot-1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
        elif template==2:
            civ_map=place_spot(row_spot+1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
        else:
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
        civ_map=place_spot(row_spot,col_spot,civ_map)
        return civ_map

    def rand_seven_spot(self,row_spot,col_spot,civ_map):
        """
           xx.   .xx   xxx   .x.   .xx   xx.
           xxx   xxx   xxx   xxx   xxx   xxx
           .xx   xx.   .x.   xxx   .xx   xx.
        """ 
        template=randint(0,5)
        if template==0:
            civ_map=place_spot(row_spot-1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot+1,col_spot+1,civ_map)
        elif template==1:
            civ_map=place_spot(row_spot-1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
        elif template==2:
            civ_map=place_spot(row_spot-1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
        elif template==3:
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
        elif template==4:
            civ_map=place_spot(row_spot-1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot+1,col_spot+1,civ_map)
        else:
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
        civ_map=place_spot(row_spot,col_spot,civ_map)
        return civ_map

    def rand_eight_spot(self,row_spot,col_spot,civ_map):
        """
           .xx   xx.   xxx   xxx
           xxx   xxx   xxx   xxx
           xxx   xxx   xx.   .xx
        """ 
        template=randint(0,3)
        if template==0:
            civ_map=place_spot(row_spot-1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot+1,col_spot+1,civ_map)
        elif template==1:
            civ_map=place_spot(row_spot-1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot+1,col_spot+1,civ_map)
        elif template==2:
            civ_map=place_spot(row_spot+1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
        else:
            civ_map=place_spot(row_spot+1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot+1,col_spot+1,civ_map)
        civ_map=place_spot(row_spot,col_spot,civ_map)
        return civ_map

    def nine_spot(self,row_spot,col_spot,civ_map):
        """
           .x.   
           xxx   
           .x.   
        """
        civ_map=place_spot(row_spot-1,col_spot-1,civ_map)
        civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
        civ_map=place_spot(row_spot-1,col_spot,civ_map)
        civ_map=place_spot(row_spot+1,col_spot,civ_map)
        civ_map=place_spot(row_spot-1,col_spot+1,civ_map)
        civ_map=place_spot(row_spot+1,col_spot+1,civ_map)
        civ_map=place_spot(row_spot,col_spot-1,civ_map)
        civ_map=place_spot(row_spot,col_spot+1,civ_map)
        civ_map=place_spot(row_spot,col_spot,civ_map)
        return civ_map

    def ten_spot(self,row_spot,col_spot,civ_map):
        """
           x.  .x  ..  ..
           ..  ..  x.  .x
        """
        template=rantint(0,3)
        if template==0:
            civ_map=nine_spot(row_spot,col_spot,civ_map)
            civ_map=place_spot(row_spot+2,col_spot,civ_map)
        elif template==1:
            civ_map=nine_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+2,col_spot+1,civ_map)
        elif template==2:
            civ_map=nine_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
        else:
            civ_map=nine_spot(row_spot+1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot+1,civ_map)
        return civ_map

    def eleven_spot(self,row_spot,col_spot,civ_map):
        """
           x.  .x  ..  ..
           ..  ..  x.  .x
        """
        template=rantint(0,3)
        if template==0:
            civ_map=nine_spot(row_spot,col_spot,civ_map)
            civ_map=place_spot(row_spot+2,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot+2,civ_map)
        elif template==1:
            civ_map=nine_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+2,col_spot+1,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
        elif template==2:
            civ_map=nine_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot+1,col_spot+2,civ_map)
        else:
            civ_map=nine_spot(row_spot+1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
        return civ_map

    def twelve_spot(self,row_spot,col_spot,civ_map):
        """
           xx  x.  ..  .x
           ..  x.  xx  .x
        """
        template=rantint(0,3)
        if template==0:
            civ_map=nine_spot(row_spot,col_spot,civ_map)
            civ_map=place_spot(row_spot-1,col_spot+2,civ_map)
            civ_map=place_spot(row_spot,col_spot+2,civ_map)
            civ_map=place_spot(row_spot+1,col_spot+2,civ_map)
        elif template==1:
            civ_map=nine_spot(row_spot,col_spot,civ_map)
            civ_map=place_spot(row_spot+2,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+2,col_spot,civ_map)
            civ_map=place_spot(row_spot+2,col_spot-1,civ_map)
        elif template==2:
            civ_map=nine_spot(row_spot+1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot+2,col_spot-1,civ_map)
        else:
            civ_map=nine_spot(row_spot+1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot+2,civ_map)
            civ_map=place_spot(row_spot-1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
        return civ_map

    def thirteen_spot(self,row_spot,col_spot,civ_map):
        """
           xxx.   .xxx   .xx.  .xx.
           xxxx   xxxx   xxxx  xxxx
           xxxx   xxxx   xxxx  xxxx
           .xx.   .xx.   .xxx  xxx.
        """
        template=rantint(0,3)
        if template==0:
            civ_map=nine_spot(row_spot,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot+2,civ_map)
            civ_map=place_spot(row_spot+1,col_spot+2,civ_map)
            civ_map=place_spot(row_spot+2,col_spot,civ_map)
            civ_map=place_spot(row_spot+2,col_spot+1,civ_map)
        elif template==1:
            civ_map=nine_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot+2,col_spot,civ_map)
            civ_map=place_spot(row_spot+2,col_spot+1,civ_map)
        elif template==2:
            civ_map=nine_spot(row_spot+1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot-1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
        else:
            civ_map=nine_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot-1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot,col_spot+2,civ_map)
            civ_map=place_spot(row_spot+1,col_spot+2,civ_map)

        return civ_map

    def fourteen_spot(self,row_spot,col_spot,civ_map):
        """
           xxx.   .xxx  
           xxxx   xxxx 
           xxxx   xxxx
           .xxx   xxx.
        """
        template=rantint(0,1)
        if template==0:
            civ_map=nine_spot(row_spot,col_spot,civ_map)
            civ_map=place_spot(row_spot+2,col_spot+2,civ_map)
            civ_map=place_spot(row_spot+2,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+2,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot+2,civ_map)
            civ_map=place_spot(row_spot+1,col_spot+2,civ_map)
        else:
            civ_map=nine_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot-1,col_spot+2,civ_map)
            civ_map=place_spot(row_spot-1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot,col_spot+2,civ_map)
            civ_map=place_spot(row_spot+1,col_spot+2,civ_map)

        return civ_map

    def fifteen_spot(self,row_spot,col_spot,civ_map):
        """
           xxxx   xxxx   .xxx  xxx.
           xxxx   xxxx   xxxx  xxxx
           xxxx   xxxx   xxxx  xxxx
           xxx.   .xxx   xxxx  xxxx
        """
        template=rantint(0,3)
        if template==0:
            civ_map=nine_spot(row_spot,col_spot,civ_map)
            civ_map=place_spot(row_spot-1,col_spot+2,civ_map)
            civ_map=place_spot(row_spot,col_spot+2,civ_map)
            civ_map=place_spot(row_spot+1,col_spot+2,civ_map)
            civ_map=place_spot(row_spot+2,col_spot-1,civ_map)
            civ_map=place_spot(row_spot+2,col_spot,civ_map)
            civ_map=place_spot(row_spot+2,col_spot+1,civ_map)
        elif template==1:
            civ_map=nine_spot(row_spot,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot+2,col_spot,civ_map)
            civ_map=place_spot(row_spot+2,col_spot+1,civ_map)
            civ_map=place_spot(row_spot+2,col_spot+2,civ_map)
        elif template==2:
            civ_map=nine_spot(row_spot+1,col_spot,civ_map)
            civ_map=place_spot(row_spot-1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot,col_spot-1,civ_map)
            civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot-1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot+2,civ_map)
        else:
            civ_map=nine_spot(row_spot+1,col_spot+1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot+2,civ_map)
            civ_map=place_spot(row_spot,col_spot+2,civ_map)
            civ_map=place_spot(row_spot+1,col_spot+2,civ_map)
            civ_map=place_spot(row_spot-1,col_spot-1,civ_map)
            civ_map=place_spot(row_spot-1,col_spot,civ_map)
            civ_map=place_spot(row_spot-1,col_spot+1,civ_map)

        return civ_map

    def sixteen_spot(self,row_spot,col_spot,civ_map):
        """
           xxx   
           xxx   
           xxx   
        """
        civ_map=place_spot(row_spot-1,col_spot-1,civ_map)
        civ_map=place_spot(row_spot+1,col_spot-1,civ_map)
        civ_map=place_spot(row_spot-1,col_spot,civ_map)
        civ_map=place_spot(row_spot+1,col_spot,civ_map)
        civ_map=place_spot(row_spot-1,col_spot+1,civ_map)
        civ_map=place_spot(row_spot+1,col_spot+1,civ_map)
        civ_map=place_spot(row_spot,col_spot-1,civ_map)
        civ_map=place_spot(row_spot,col_spot+1,civ_map)
        civ_map=place_spot(row_spot,col_spot,civ_map)
        civ_map=place_spot(row_spot+2,col_spot-1,civ_map)
        civ_map=place_spot(row_spot+2,col_spot,civ_map)
        civ_map=place_spot(row_spot+2,col_spot+1,civ_map)
        civ_map=place_spot(row_spot+2,col_spot+2,civ_map)
        civ_map=place_spot(row_spot+1,col_spot+2,civ_map)
        civ_map=place_spot(row_spot,col_spot+2,civ_map)
        civ_map=place_spot(row_spot-1,col_spot+2,civ_map)
        return civ_map

    def place_spot(self,row_spot,col_spot,civ_map):
        civ_map[row_spot][col_spot].developed=True
        return civ_map

    def define_nations(self,civ_map):
        return civ_map