global data
data = {
    'users' : {
        'auth_user_id1' : {
            'name_first' : 'first_name1',
            'name_last' : 'last_name1',
            'email' : 'example1@hotmail.com',
            'password' : 'password1',
        },
        'auth_user_id2' : {
            'name_first' : 'first_name2',
            'name_last' : 'last_name2',
            'email' : 'example2@hotmail.com',
            'password' : 'password2',
        },
        'auth_user_id3' : {
            'name_first' : 'first_name3',
            'name_last' : 'last_name3',
            'email' : 'example3@hotmail.com',
            'password' : 'password3',
        },
        'auth_user_id4' : {
            'name_first' : 'first_name4',
            'name_last' : 'last_name4',
            'email' : 'example4@hotmail.com',
            'password' : 'password4',
        },
    },
    'channels' : {
        'channel_id1' : {
                'name' : 'channel1',
                'is_public' : False,
                'owners' : ['auth_user_id1'],
                'members' : ['auth_user_id2'],
        },
        'channel_id2' : {
                'name' : 'channel2',
                'is_public' : True,
                'owners' : ['auth_user_id3'],
                'members' : ['auth_user_id4'],
        },
    },
}