# Updated data file so we have a clear data section

data = {
    "users" : [],
    "channels" : [],
    "messages" : []
}

def reset_data():
    global data
    data = {
        "users" : [],
        "channels" : [],
        "messages" : []
    }
    return data
