import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

transactions = 400
arrival_factor_before_10 = 50  
arrival_factor_after_4 = 50   
arrival_factor_closed=5
arrival_factor_day=20
start_year,start_month,start_day=2024,1,1
end_year,end_month,end_day=2024,1,10


def simulate_arrivals(transactions, start_year,start_month,start_day,end_year,end_month,end_day, arrival_factor_before_10, arrival_factor_after_4,arrival_factor_closed,arrival_factor_day ):
    arrivals=[]
    
    start_datetime = datetime(start_year, start_month, start_day)
    end_datetime = datetime(end_year, end_month, end_day)

    for day in range((end_datetime - start_datetime).days + 1):

    
        current_day = start_datetime + timedelta(days=day)

        while len(arrivals) < transactions:
            arrival_time= random.uniform(0, 24*60*60)
            arrival_datetime = current_day+timedelta(seconds=arrival_time)

            # Calculate arrival rate based on desired number of arrivals per minute
            if arrival_datetime.time()<datetime(current_day.year, current_day.month,current_day.day,8,0).time() or arrival_datetime.time()>datetime(current_day.year, current_day.month,current_day.day,18,0).time():
                arrival_rate = arrival_factor_closed / 60.0
            elif arrival_datetime.time() < datetime(current_day.year, current_day.month,current_day.day,10,0).time():
                arrival_rate = arrival_factor_before_10 / 60.0
            elif arrival_datetime.time() > datetime(current_day.year, current_day.month,current_day.day,16,0).time():
                arrival_rate = arrival_factor_after_4 / 60.0
            else:
                arrival_rate = arrival_factor_closed/60

            if random.uniform(0, 1) < arrival_rate:
                arrivals.append(arrival_datetime)

    return sorted(arrivals)


arr = simulate_arrivals(transactions, start_year,start_month,start_day,end_year,end_month,end_day,  arrival_factor_before_10, arrival_factor_after_4,arrival_factor_closed,arrival_factor_day )
arrivals = pd.DataFrame({'ArrivalTimes': arr})


print("Arrival times:")
for arrival in arr:
    print(arrival.strftime('%Y-%m-%d %H:%M:%S'))


#check for differences
morning_rush = []
evening_rush = []
opening = []
night = []

for arrival in arr:
    arrival_datetime = datetime.strptime(arrival.strftime("%H:%M"), "%H:%M")

    if  arrival_datetime < datetime.strptime("8:00", "%H:%M") or  arrival_datetime > datetime.strptime("18:00", "%H:%M"):
        night.append(arrival_datetime)
    elif arrival_datetime < datetime.strptime("10:00", "%H:%M"):
        morning_rush.append(arrival_datetime)
    elif arrival_datetime > datetime.strptime("16:00", "%H:%M"):
        evening_rush.append(arrival_datetime)
    else:
        opening.append(arrival_datetime)

print("Morning rush:", len(morning_rush))
print("evening rush:", len(evening_rush))
print("opening, no rush", len(opening))
print("closing: ", len(night))
print("total: ",len(morning_rush)+len(evening_rush)+len(opening)+len(night))
print(len(arr))
print("_________________________________")
print("Morning rush:", len(morning_rush)/2)
print("After 4 pm per hour:", len(evening_rush)/2)
print("Between 10 am and 4 pm:", len(opening)/6)
print("closing: ", len(night)/14)


