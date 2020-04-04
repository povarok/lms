

def get_seconds_from_string(time_string):
    splited_time_string = time_string.split(":")
    seconds = (int(splited_time_string[0]) * 3600 + int(splited_time_string[1]) * 60 + int(splited_time_string[2]))
    return seconds