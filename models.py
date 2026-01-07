#-------------------------------------------------------------------------------------------
# models.py -> contains database models and relevants (pickle for now, TODO: use a database)
#-------------------------------------------------------------------------------------------

###########################################################
import pickle
from dataclasses import dataclass
from datetime import datetime
#########################################################


######### CONSTANTS ################################
DATA_FILE = "data.pkl"
################################################

@dataclass
class Booking:
    '''
        Stores bookings info
    '''
    user_email:str
    booked_time:datetime
    holding_state:bool = True


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

    hold_time:int = 3 # max amount of days before your hold freezes and someone else can register
    occupy_time:int = 15 # max amount of days before you HAVE to return it


    booking_ref: Booking | None = None # maybe have a history

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
               

