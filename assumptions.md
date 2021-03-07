### belows are assumptions made when writing the corresponding modules 

#### auth_login_v1 

#### auth_register_v1 

#### channel_invite_v1

#### channel_details_v1

#### channel_messages_v1

#### channel_join_v1
Users who are already members of a channel will not attempt to join again
There will be no duplicate entries
Users will be unable to join servers that are private

#### channels_list_v1
The returned channels will list in the order they were created
Users can call the command without being a part of any official channel, it will only return an empty list


#### channels_listall_v1

#### channels_create_v1

#### message_send_v1
