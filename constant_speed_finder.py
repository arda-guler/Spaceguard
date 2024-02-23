from datetime import datetime, timedelta

def calculate_position(x1, y1, x2, y2, time1, time2, time_position3):
    time1 = datetime.strptime(time1, "%H:%M:%S")
    time2 = datetime.strptime(time2, "%H:%M:%S")
    time_position3 = datetime.strptime(time_position3, "%H:%M:%S")

    speed_x = (x2 - x1) / (time2 - time1).total_seconds()
    speed_y = (y2 - y1) / (time2 - time1).total_seconds()

    time_difference = (time_position3 - time1).total_seconds()

    x_position3 = x1 + speed_x * time_difference
    y_position3 = y1 + speed_y * time_difference

    return x_position3, y_position3

x1, y1 = 976, 1033
x2, y2 = 982, 1037
time1 = "07:53:14"
time2 = "08:38:07"
time_position3 = "12:10:08"

result = calculate_position(x1, y1, x2, y2, time1, time2, time_position3)
print(f"Position of the object at {time_position3}: ({result[0]}, {result[1]})")
