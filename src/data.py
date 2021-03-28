from src.other import clear_v1
import pickle

# Iteration 1 test data

#DBInited = False

class ListeningDict(dict):
    # override base class method
    def __init__(self, initialDict):
        # global DBInited
        # if DBInited == False:
        #     f = open('database.p', 'rb')
        #     initialDict = pickle.load(f)
        #     f.close()
        #     DBInited = True

        # recursively replace nested dictionaries with instance of ListeningDict
        for k,v in initialDict.items():
          if isinstance(v,dict):
            initialDict[k] = ListeningDict(v)

        # call super class method to perform the actual initialisation 
        super().__init__(initialDict)

    # override base class method
    def __setitem__(self, item, value):
        # replace all instances of dict with ListeningDict
        if isinstance(value,dict):
          value = ListeningDict(value)

        # call superclass method to perform actual setting
        super().__setitem__(item, value)

        # write data to file, if there isn't a database, create one from the default below
        with open("database.p", "wb") as FILE:
            pickle.dump(data, FILE)


# this initialization with some default values exists only because some previous tests depend on them
# whatever, just leave it as default values in case database.p disappears or corrupted
data = ListeningDict({
    'users' : {
        35746842521 : {
            'name_first' : 'first_name1',
            'name_last' : 'last_name1',
            'email' : 'example1@hotmail.com',
            'password' : 'password1',
            'handle_str' : 'first_name1last_name',
            'permission_id': 1,
        },
        11753764853 : {
            'name_first' : 'first_name2',
            'name_last' : 'last_name2',
            'email' : 'example2@hotmail.com',
            'password' : 'password2',
            'handle_str' : 'first_name2last_name',
            'permission_id': 2,
        },
    },
    'channels' : {
        14723573315 : {
            'name' : 'channel1',
            'is_public' : True,
            'owner_members' : ['auth_user_id1'],
            'all_members' : ['auth_user_id1', 'auth_user_id2'],
            'messages' : [
                {
                    'message_id': 4561328123,
                    'u_id': 35746842521,
                    'message': 'Hello World1',
                    'time_created': 123416589,
                },
                {
                    'message_id': 61510648893,
                    'u_id': 11753764853,
                    'message': 'Hello World2',
                    'time_created': 123456789,
                },
            ]
        },
        31627643273 : {
            'name' : 'channel2',
            'is_public' : True,
            'owner_members' : [123456789],
            'all_members' : [123456789, 12389473129847],
            'messages' : [
                {
                    'message_id': 12354122383,
                    'u_id': 35746842521,
                    'message': 'Hello World1',
                    'time_created': 45132806512,
                },
                {
                    'message_id': 123156231064,
                    'u_id': 11753764853,
                    'message': 'Hello World2',
                    'time_created': 68741450315603,
                }
            ],
        },
    },
})


# Function to reset the data to default (assists in testing)
def reset_data():
    global data
    data = clear_v1()
    return data

def retrieve_data():
    global data
    return data
