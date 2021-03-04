data = {
    'users' : [
        {
            'id' : 1,
            'name_first' : 'first_name',
            'name_last' : 'last_name',
            'email' : 'random@hotmail.com',
            'password' : 'password123',
            'auth_user_id' : 1,

        },
        {
            'id' : 2,
            'name_first' : 'first_name',
            'name_last' : 'last_name',
            'email' : 'random@hotmail.com',
            'password' : 'password123',
            'auth_user_id' : 2,
        },
    ],
    'channels' : [
        {
            'channel_id' : 1,
            'name' : 'channel1',
            'is_public' : True,
            'owner_members' : [
                {
                    'auth_user_id' : 1
                    'name_first' : 'first_name'
                    'name_last' : 'last_name'
                }
            ],
            'all_members' : [
                {
                    'auth_user_id' : 1
                    'name_first' : 'first_name'
                    'name_last' : 'last_name'
                },
                {
                    'auth_user_id' : 2
                    'name_first' : 'first_name'
                    'name_last' : 'last_name'
                }
            ],
            'messages' : [
                {
                    'message_id' : 0
                    'auth_user_id' : 1
                    'message' : 'Hello World'
                    'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)'
                },
                {
                    'message_id' : 1
                    'auth_user_id' : 2
                    'message' : 'Hello World2'
                    'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)'
                }
            ],
        },
        {
            'channel_id' : 2,
            'name' : 'channel2',
            'is_public' : False,
            'owner_members' : [
                {
                    'auth_user_id' : 1
                    'name_first' : 'first_name'
                    'name_last' : 'last_name'
                }
            ],
            'all_members' : [
                {
                    'auth_user_id' : 1
                    'name_first' : 'first_name'
                    'name_last' : 'last_name'
                },
                {
                    'auth_user_id' : 2
                    'name_first' : 'first_name'
                    'name_last' : 'last_name'
                }
            ],
            'messages' : [
                {
                    'message_id' : 0
                    'auth_user_id' : 1
                    'message' : 'Hello World'
                    'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)'
                },
                {
                    'message_id' : 1
                    'auth_user_id' : 2
                    'message' : 'Hello World2'
                    'timecreated' : 'datetime(YYYY, MM, DD, HH, MM)'
                }
            ],
        },
    ],
}
