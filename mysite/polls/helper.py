

def get_seconds_from_string(time_string):
    splited_time_string = time_string.split(":")
    seconds = (int(splited_time_string[0]) * 3600 + int(splited_time_string[1]) * 60 + int(round(float(splited_time_string[2]))))
    return seconds

def get_string_from_seconds(timestamp):
    timestamp = round(timestamp)
    hours = timestamp // 3600
    minutes = (timestamp - hours * 3600) // 60
    seconds = (timestamp - hours * 3600) % 60
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'