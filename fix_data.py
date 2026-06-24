import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from core.models import Vehicle

updates = {
    "Porsche 911 GT3 RS": {"seats": 2, "fuel": "Petrol", "trans": "Automatic", "lug": "1 bag", "make": "Porsche", "model": "911 GT3 RS"},
    "Land Rover Defender 110": {"seats": 7, "fuel": "Petrol", "trans": "Automatic", "lug": "4 bags", "make": "Land Rover", "model": "Defender 110"},
    "Tesla Model X Plaid": {"seats": 7, "fuel": "Electric", "trans": "Automatic", "lug": "3 bags", "make": "Tesla", "model": "Model X Plaid"},
    "Chevrolet Corvette Z06": {"seats": 2, "fuel": "Petrol", "trans": "Automatic", "lug": "1 bag", "make": "Chevrolet", "model": "Corvette Z06"},
    "BMW M5 Competition": {"seats": 5, "fuel": "Petrol", "trans": "Automatic", "lug": "2 bags", "make": "BMW", "model": "M5 Competition"},
    "Audi RS6 Avant": {"seats": 5, "fuel": "Petrol", "trans": "Automatic", "lug": "4 bags", "make": "Audi", "model": "RS6 Avant"},
    "Mercedes-Benz G63 AMG": {"seats": 5, "fuel": "Petrol", "trans": "Automatic", "lug": "4 bags", "make": "Mercedes-Benz", "model": "G63 AMG"},
    "Lamborghini Urus": {"seats": 5, "fuel": "Petrol", "trans": "Automatic", "lug": "3 bags", "make": "Lamborghini", "model": "Urus"},
    "Ferrari Purosangue": {"seats": 4, "fuel": "Petrol", "trans": "Automatic", "lug": "2 bags", "make": "Ferrari", "model": "Purosangue"},
    "Rolls-Royce Cullinan": {"seats": 5, "fuel": "Petrol", "trans": "Automatic", "lug": "4 bags", "make": "Rolls-Royce", "model": "Cullinan"},
    "Bentley Continental GT": {"seats": 4, "fuel": "Petrol", "trans": "Automatic", "lug": "2 bags", "make": "Bentley", "model": "Continental GT"},
    "Aston Martin DB12": {"seats": 4, "fuel": "Petrol", "trans": "Automatic", "lug": "2 bags", "make": "Aston Martin", "model": "DB12"},
    "McLaren 765LT": {"seats": 2, "fuel": "Petrol", "trans": "Automatic", "lug": "1 bag", "make": "McLaren", "model": "765LT"},
    "Porsche Taycan Turbo S": {"seats": 4, "fuel": "Electric", "trans": "Automatic", "lug": "2 bags", "make": "Porsche", "model": "Taycan Turbo S"},
    "Lucid Air Sapphire": {"seats": 5, "fuel": "Electric", "trans": "Automatic", "lug": "3 bags", "make": "Lucid", "model": "Air Sapphire"},
    "Rivian R1S": {"seats": 7, "fuel": "Electric", "trans": "Automatic", "lug": "5 bags", "make": "Rivian", "model": "R1S"},
    "Dodge Challenger SRT Hellcat": {"seats": 5, "fuel": "Petrol", "trans": "Automatic", "lug": "2 bags", "make": "Dodge", "model": "Challenger SRT Hellcat"},
    "Toyota Sienna": {"seats": 8, "fuel": "Hybrid", "trans": "Automatic", "lug": "5 bags", "make": "Toyota", "model": "Sienna"},
    "Honda Odyssey": {"seats": 8, "fuel": "Petrol", "trans": "Automatic", "lug": "5 bags", "make": "Honda", "model": "Odyssey"},
    "Chrysler Pacifica": {"seats": 7, "fuel": "Hybrid", "trans": "Automatic", "lug": "5 bags", "make": "Chrysler", "model": "Pacifica"},
    "Ford F-150 Raptor": {"seats": 5, "fuel": "Petrol", "trans": "Automatic", "lug": "5 bags", "make": "Ford", "model": "F-150 Raptor"},
    "Chevrolet Silverado 2500HD": {"seats": 5, "fuel": "Diesel", "trans": "Automatic", "lug": "5 bags", "make": "Chevrolet", "model": "Silverado 2500HD"},
    "Ram 3500 Heavy Duty": {"seats": 5, "fuel": "Diesel", "trans": "Automatic", "lug": "5 bags", "make": "Ram", "model": "3500 Heavy Duty"},
    "Toyota Camry": {"seats": 5, "fuel": "Hybrid", "trans": "Automatic", "lug": "2 bags", "make": "Toyota", "model": "Camry"},
    "Honda Accord": {"seats": 5, "fuel": "Hybrid", "trans": "Automatic", "lug": "2 bags", "make": "Honda", "model": "Accord"},
    "Hyundai Sonata": {"seats": 5, "fuel": "Petrol", "trans": "Automatic", "lug": "2 bags", "make": "Hyundai", "model": "Sonata"},
    "Lexus LC 500": {"seats": 4, "fuel": "Petrol", "trans": "Automatic", "lug": "1 bag", "make": "Lexus", "model": "LC 500"},
    "Toyota Supra GR": {"seats": 2, "fuel": "Petrol", "trans": "Manual", "lug": "1 bag", "make": "Toyota", "model": "Supra GR"},
    "Mercedes-AMG GT 63": {"seats": 4, "fuel": "Petrol", "trans": "Automatic", "lug": "2 bags", "make": "Mercedes-Benz", "model": "AMG GT 63"},
    "Range Rover SVAutobiography": {"seats": 5, "fuel": "Petrol", "trans": "Automatic", "lug": "4 bags", "make": "Land Rover", "model": "Range Rover SVAutobiography"},
}

for vehicle in Vehicle.objects.all():
    data = updates.get(vehicle.name)
    if data:
        vehicle.seats = data["seats"]
        vehicle.fuel_type = data["fuel"]
        vehicle.transmission = data["trans"]
        vehicle.luggage = data["lug"]
        vehicle.make = data["make"]
        vehicle.model = data["model"]
        vehicle.save()

# Let's check the Sienna Image
sienna = Vehicle.objects.get(name="Toyota Sienna")
if sienna.main_image:
    print(f"Sienna Image Path: {sienna.main_image.name}")
else:
    print("Sienna has no image.")
