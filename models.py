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
    
    booked_date:datetime  # booked is the first time they hold it 
    occupied_date:datetime | None= None # occupy happens when they physically come and take it 

    on_hold_state:bool = True
    on_occupied_state:bool = False
    is_expired = False # happens when occupied days crosses the max occupy days


@dataclass
class Item:
    '''
        Item : holds information about a registered item
    '''
    id:int
    name:str
    description:str
    image_path:str|None 
    available: bool = True

    hold_time:int = 3 # max amount of days before your hold freezes and someone else can register
    occupy_time:int = 15 # max amount of days before you HAVE to return it

    booking_ref: Booking = None # maybe have a history


def save_data_base(data = list[Item]) -> None:
    '''
        Saves some updated data chunk into the databse (currently through pickle file).
    '''
    try:
        with open(DATA_FILE, 'wb') as file:
            pickle.dump(data, file)
    except Exception as e :
        print(f'[COULDN"T SAVE FILE IN THE DATABASE BECAUSE OF {e}]')

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
          Item(1,"Football","Some ball", "stuff/stuff"),
          Item(2,"Frankenstien","Crazy book", "stuff/stuff"),
          Item(3,"Cricket Bat","For cricket", "stuff/stuff"),
          Item(4,"Mouse","Not a computer one, a  real one", "stuff/stuff"),
          Item(5,"Helicopter","Useful for flying", "stuff/stuff"),
     ]

    
    with open(DATA_FILE ,'wb') as file:
        pickle.dump(_test_data, file)
    print("Test data wrote succesfully ")
               

