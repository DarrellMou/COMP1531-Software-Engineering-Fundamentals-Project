# COMP1531 Assignment Iteration 2 Assumptions
## auth_register_v2 (winston)
* Users can have the same first_name, last_name and password.
* Users' first name, last name can be composed of any characters supported by python3, including symbols like '@#[]&^'
* auth_user_id will be stored in the users key of the data dictionary.
* Registration acts as a login, a new user after registration is automatically granted a session to DREAMS.

## auth/login/v2 (winston)
* N/A

## auth/logout/v1 (winston)
* Token associated with a session on device A can be used to logout that session on device B.

## user/profile/v2 (winston)
* A user can access the profile of another user by their auth_user_id, given his token is valid.

## user/profile/setname/v2 (winston)
* It is valid for a user to update name to a previous name.
* Users' name can be composed of any characters supported by python3, including symbols like '@#[]&^'.

## user/profile/setemail/v2 (winston)
* It is valid for a user to update email to a previous email.

## user/profile/sethandle/v2 (winston)
* It is valid for a user to update handle to a previous handle.
* Users' handle can be composed of any characters supported by python3, including symbols like '@#[]&^'.

## users/all/v1 (winston)
* Users are displayed in order of registration.

## channel_invite_v2 (darrell)
* No existing members can invite themselves.
* All members can invite users in any type of channel.
* Only can invite members that are not already invited.

## channel_details_v2 (darrell)
* The member of all_members appears the same order as they joined the channel.
* The member of owner_members appears the same order as they became the owner of the channel.

## channel_messages_v2 (brendan)
* Given start will never be negative. 
* An out of index message within the messages list of a channel (i.e data['channels'][channel_id]['messages']) will never be accessed and therefore, there is no need to raise an index error. E.g. trying to access data['channels'][channel_id]['messages'][1] when there # is only 1 message in that specific channel_id, which has an index of 0.
* If there are no messages in the channel then that means the most recent message has been returned, therefore 'end' = -1.
* If there are 50 messages in a channel and the start is 0, then the 50th message IS the last message - return 'end': -1 rather than 'end': 50.

## channel_join_v2 (kellen)
* There will be no duplicate users.

## channel_addowner_v1 (kellen)
* Users outside of the channel can be added into the owner member pool, and will also be added into the all members pool.

## channel_removeowner_v1 (kellen)
* Users will be removed from the owner member pool, but will remain in all members. 

## channel_leave_v1 (darrell)
* A channel remains even if there are no members left.

## notifications/get/v1 (kellen)
* If there are no notifications, the function will return an empty list.

## channels_list_v2 (kellen)
* The channels will appear in the order they were created.
* Users can call the command without being a part of any official channel - it will only return an empty list.

## channels_listall_v2 (nikki)
* Any valid auth_user_id can see all the channels - public or private. 
* The returned channels list is in the order as they were created. 

## channels_create_v2 (nikki)
* The user who creates the channel automatically becomes the owner of the channel.
* Different channels can have the same name. 
* Channels can be created without a name.

## dm_create_v1 (darrell)
* The function is never given an empty u_ids list.
* If even one of the dm_id in the u_ids list is removed or invalid, a dm is NOT created.
* The user who called dm_create_v1 is the owner, i.e. first person on dm_members list.
* Users can create as many dms with the exact same users.

## dm_details_v1 (darrell)
* The members appears the same order as they joined the dm.

## dm_list_v1 (darrell)
* The dms will appear in the order they were created.
* Users can call the command without being a part of any official dm - it will only return an empty list.

## dm_remove_v1 (darrell)
* N/A

## dm_invite_v1 (darrell)
* No existing members can invite themselves.
* All members can invite users in any type of dm.
* Only invite members that are not already invited.

## dm_leave_v1 (darrell)
* If the dm owner leaves or is removed, the next user in the dm member list gets the dm creator privileges.
* A dm remains even if there are no members left.

## dm_messages_v1 (brendan, darrell)
* Given start will never be negative. 
* An out of index message within the messages list of a channel (i.e data['dm'][dm_id]['messages']) will never be accessed and therefore, there is no need to raise an index error. E.g. trying to access data['dm'][dm_id]['messages'][1] when there is only 1 message in that specific dm_id, which has an index of 0.
* If there are no messages in the dm then that means the most recent message has been returned, therefore 'end' = -1.
* If there are 50 messages in a dm and the start is 0, then the 50th message IS the last message - return 'end': -1 rather than 'end': 50.

## message_send_v1 (brendan)
* An empty message can be sent.

## message_edit_v2 (brendan)
* The first member of the dm in the dm list is the owner. Only they are allowed to remove and edit any messages within that dm regardless of if they sent the message or not.

## message_remove_v1 (brendan)
* Same as message_edit_v2.
* 'Removing' a message just removes the text from the message and tags the message as removed.
* It is impossible for a user to 'remove' a message when there are no messages in the channel/dm.

## message_share_v1 (brendan)
* Sharing a message will add a new message to the data['messages'] list and to the channel's or dm's messages list.
* The way messages are shared in the http://dreams-unsw.herokuapp.com/ app is the correct way of sharing messages.

## message_senddm_v1 (brendan, nikki)
* Message inputs "" and " " will append to the message list.

## search_v2 (nikki)
* Query search will return messages in channels even before the user has joined.
* Message input "" will return all messages.
* Message input " " will return messages with spaces in them, e.g. " Hi", "Back End"
* Global owners can only see messages from channels and dms they've joined.

## admin_user_remove_v1 (nikki)
* Removed users do not have valid tokens and hence cannot access any feature of Dreams. They also no longer possess a valid u_id, so other users cannot interact with them unless it is through user/profile/v2.
* A removed user's profile is only retrievable with user/profile/v2 and nothing else.

## admin_userpermission_change_v1 (nikki)
* N/A



# ARCHIVE
# COMP1531 Assignment Iteration 1 Assumptions

## auth_register_v1 (winston)
* The auth_user_id is generated by int(uuid.uuid(4)) which creates a unique number. 
* Users can have the same first_name, last_name and password.
* auth_user_id will be stored in the users key of the data dictionary.

## channel_invite_v1 (darrell)
* No existing members can invite themselves.
* All members can invite users in any type of channel.
* Only can invite members that are not already invited.
* When invited, the user's auth_user_id will be added to the channel key of the data dictionary.

## channel_details_v1 (darrell)
* The member of all_members appears the same order as they joined the channel.
* The member of owner_members appears the same order as they became the owner of the channel.

## channel_messages_v1 (brendan)
* Given start will never be negative. 
* Start refers to the starting index of the data['channels'][channel_id]['messages'] list.
* An out of index message within the messages list of a channel (i.e data['channels'][channel_id]['messages']) will never be accessed and therefore, there is no need to raise an index error. E.g. trying to access data['channels'][channel_id]['messages'][1] when there # is only 1 message in that specific channel_id, which has an index of 0.
* Messages are originally appended to our message list when they are sent.
* If there are no messages in the channel then that means the most recent message has been returned, therefore 'end' = -1.
* If there are 50 messages in a channel and the start is 0, then the 50th message IS the last message - return 'end': -1 rather than 'end': 50.

## channel_join_v1 (kellen)
* Users who are already members of a channel will not attempt to join again.
* There will be no duplicate entries.
* Global owners do not become an owner member, but has owner permissions.

## channels_list_v1 (kellen)
* The channels will appear in the order they were created.
* Users can call the command without being a part of any official channel - it will only return an empty list.

## channels_listall_v1 (nikki)
* Any valid auth_user_id can see all the channels - public or private. 
* The returned channels list is in the order as they were created. 

## channels_create_v1 (nikki)
* The user who creates the channel automatically becomes the owner of the channel.
* Channel_id is generated by int(uuid.uuid(1)) which creates a unique number based on the hostID and current time.
* Different channels can have the same name. 

## data 
* Owner_members are also part of all_members.
