# Iteration 1 test data
data = {
    'users' : {
        35746842521 : {
            'u_id' : 1,
            'name_first' : 'first_name1',
            'name_last' : 'last_name1',
            'email' : 'example1@hotmail.com',
            'password' : 'password1',
            'handle_str' : 'first_name1last_name',
        },
        11753764853 : {
            'u_id' : 2,
            'name_first' : 'first_name2',
            'name_last' : 'last_name2',
            'email' : 'example2@hotmail.com',
            'password' : 'password2',
            'handle_str' : 'first_name2last_name',
        },
    },
    'channels' : {
        14723573315 : {
            'name' : 'channel1',
            'is_public' : True,
            'owner_members' : ['auth_user_id1'],
            'all_members' : ['auth_user_id1', 'auth_user_id2'],
            'messages' : [
                {'message_id1' : {
                    'auth_user_id' : 35746842521,
                    'message' : 'Hello World1',
                    'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)',
                    },
                },
                {'message_id2' : {
                    'auth_user_id' : 11753764853,
                    'message' : 'Hello World2',
                    'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)',
                    },
                },
            ],
        },
        31627643273 : {
            'name' : 'channel2',
            'is_public' : True,
            'owner_members' : ['auth_user_id1'],
            'all_members' : ['auth_user_id1', 'auth_user_id2'],
            'messages' : [
                {'message_id1' : {
                    'auth_user_id' : 35746842521,
                    'message' : 'Hello World1',
                    'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)',
                    },
                },
                {'message_id2' : {
                    'auth_user_id' : 11753764853,
                    'message' : 'Hello World2',
                    'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)',
                    },
                },
            ],
        },
    },
}

def retrieve_data():
    global data
    return data





