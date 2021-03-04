# Updated data file so we have a clear data section

# Data dictionary which will be used throughout the project
data = {
    "users" : [],
    "channels" : [],
    "messages" : []
}

# Function to reset the data to default (assists in testing)
def reset_data():
    global data
    data = {
        "users" : [],
        "channels" : [],
        "messages" : []
    }
    return data