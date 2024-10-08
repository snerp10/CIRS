


def month_bill(present,previous):
    
    consumption = present - previous
    
    charge = consumption * 24.90
    
    water_bill = charge + 25.00
    
    print(consumption)
    print(charge)
    print(water_bill)
    
    x = int(input("persent"))
    y = int(input("previous"))
    
    month_bill(x,y)
    
x = int(input("persent"))
y = int(input("previous"))

month_bill(x,y)