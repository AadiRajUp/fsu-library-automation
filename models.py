#############################################################################################
# models.py -> contains database models and relevants (pickle for now, TODO: use a database)
#############################################################################################

###########################################################
import pickle
from dataclasses import dataclass
#########################################################


######### CONSTANTS ################################
DATA_FILE = "data.pkl"
################################################

@dataclass
class Item:
    '''
        Item : holds information about a registered item
    '''
    id:int
    name:str
    description:str
    image_path:str|None 
    count:int # TODO: redundant???
    available: int = 0

    info: str = "" # for tracking, maybe make a seperate table for the whole histroy? TODO

    def __post_init__(self):
        self.available = self.count

def load_data_base() -> list[Item]:
    ''' 
        Loads the data (currently through a pickle file) and returns
        some reference to it. (currently all the values in a list)
    '''
    try:
        with open(DATA_FILE, 'rb') as file:
            return  pickle.load(file)
    except FileNotFoundError:
            print("[STORED DATA NOT FOUND, RETURNING EMPTY]")
            return []

def fill_test_data() -> None:
    '''
        Fills random data for testing purposes
    '''
    _test_data = [
          Item(1,"Football","Some ball", "stuff/stuff", 2),
          Item(2,"Frankenstien","Crazy book", "stuff/stuff", 1),
          Item(3,"Cricket Bat","For cricket", "stuff/stuff", 1),
          Item(4,"Mouse","Not a computer one, a  real one", "stuff/stuff", 3),
          Item(5,"Helicopter","Useful for flying", "stuff/stuff", 1),
     ]

    try:
        with open(DATA_FILE ,'wb') as file:
            pickle.dump(_test_data, file)
        print("Test data wrote succesfully ")
    except FileNotFoundError:
      print("Couldn't write data into file ")
               

