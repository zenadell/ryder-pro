import random
from core.models import Vehicle

vehicles = Vehicle.objects.all()

transmissions = ['Automatic', 'Manual', 'Automatic', 'Automatic']
fuels = ['Petrol', 'Diesel', 'Electric', 'Hybrid', 'Petrol']
luggages = ['1 bag', '2 bags', '3 bags', '4 bags']
seats_options = [2, 4, 5, 7, 5, 5]

# Specific updates for realism based on car name/make
for v in vehicles:
    name_lower = v.name.lower()
    
    if 'tesla' in name_lower or 'electric' in name_lower or 'lucid' in name_lower:
        v.fuel_type = 'Electric'
        v.transmission = 'Automatic'
    elif 'hybrid' in name_lower or 'prius' in name_lower:
        v.fuel_type = 'Hybrid'
    elif 'porsche' in name_lower or 'mustang' in name_lower or '911' in name_lower:
        v.fuel_type = 'Petrol'
        v.transmission = random.choice(['Automatic', 'Manual'])
    elif 'truck' in name_lower or 'f-150' in name_lower:
        v.fuel_type = random.choice(['Diesel', 'Petrol'])
    else:
        v.fuel_type = random.choice(fuels)
        v.transmission = random.choice(transmissions)
        
    if 'suv' in name_lower or 'escalade' in name_lower or 'tahoe' in name_lower:
        v.seats = 7
        v.luggage = '4 bags'
    elif 'porsche' in name_lower or 'mustang' in name_lower or 'coupe' in name_lower:
        v.seats = 2
        v.luggage = '1 bag'
    else:
        v.seats = random.choice(seats_options)
        v.luggage = random.choice(luggages)
        
    v.save()

print(f"Updated {vehicles.count()} vehicles successfully.")
