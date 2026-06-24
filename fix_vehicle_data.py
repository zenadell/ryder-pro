import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import Vehicle

def run():
    vehicles = Vehicle.objects.all()
    
    transmissions = ['Automatic', 'Manual', 'Automatic'] # Weight automatic more
    fuel_opts = ['Petrol', 'Diesel', 'Electric', 'Hybrid']
    
    count = 0
    for v in vehicles:
        model_low = v.model.lower()
        make_low = v.make.lower()
        
        if make_low in ['tesla', 'rivian', 'lucid']:
            v.fuel_type = 'Electric'
        else:
            v.fuel_type = random.choice(fuel_opts)
            
        if any(word in model_low for word in ['coupe', 'sports', '911', 'huracan', 'spider', 'convertible', 'r8', 'mclaren']):
            v.seats = 2
            v.luggage = '1 bag'
            v.transmission = random.choice(['Automatic', 'Automatic', 'Manual'])
        elif any(word in model_low for word in ['suv', 'escalade', 'suburban', 'tahoe', 'navigator', 'x7', 'gls']):
            v.seats = random.choice([5, 7])
            v.luggage = random.choice(['3 bags', '4 bags', '5 bags'])
            v.transmission = 'Automatic'
        else:
            v.seats = random.choice([4, 5])
            v.luggage = random.choice(['1 bag', '2 bags', '3 bags'])
            v.transmission = random.choice(transmissions)
            
        v.save()
        count += 1
        
    print(f"Successfully updated specs for {count} vehicles!")

if __name__ == '__main__':
    run()
