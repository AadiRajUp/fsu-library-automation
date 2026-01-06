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
    count:int

def load_data_base() -> list[Item]:
    ''' 
        Loads the data (currently through a pickle file) and returns
        some reference to it. (currently all the values in a list)
    '''
    try:
        with open(DATA_FILE, 'rb') as file:
            return  pickle.load(file)
    except FileNotFoundError:
            return []


