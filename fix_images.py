import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import InvestmentAsset

def fix_images():
    vehicles = [
        ("Tesla Semi Truck", "truck", "Heavy duty electric semi truck", 150000, 15, 24, "truck"),
        ("Volvo FH16 Semi", "truck", "Long haul cargo transport truck", 120000, 12, 18, "truck"),
        ("Ford Transit Custom", "van", "Commercial delivery van", 45000, 8, 12, "van"),
        ("Mercedes Sprinter Van", "van", "Large logistics delivery van", 55000, 9, 12, "van"),
        ("Scania Touring Coach", "bus", "Luxury passenger bus", 200000, 18, 36, "bus"),
        ("Yutong E12 Electric Bus", "bus", "City transit electric bus", 180000, 16, 24, "bus"),
        ("John Deere 8R Tractor", "tractor", "Heavy agricultural tractor", 250000, 20, 36, "tractor"),
        ("Massey Ferguson 7S", "tractor", "Farming utility tractor", 130000, 14, 24, "tractor"),
        ("Honda Gold Wing", "motorcycle", "Premium touring motorcycle", 25000, 5, 12, "motorcycle"),
        ("Yamaha MT-09", "motorcycle", "City transport motorcycle", 10000, 4, 6, "motorcycle"),
        ("Tesla Model 3 Fleet", "car", "Ride-sharing electric car", 40000, 8, 12, "car"),
        ("Toyota Camry Hybrid", "car", "Standard city taxi vehicle", 30000, 7, 12, "car"),
        ("Peterbilt 579 Semi", "truck", "Long distance heavy truck", 145000, 14, 24, "truck"),
        ("Kenworth T680", "truck", "Aerodynamic cargo truck", 135000, 13, 24, "truck"),
        ("Ram ProMaster", "van", "Urban delivery cargo van", 42000, 8, 12, "van"),
        ("Nissan NV Cargo", "van", "Commercial business van", 38000, 7, 12, "van"),
        ("Hyundai Universe", "bus", "Intercity travel bus", 175000, 15, 24, "bus"),
        ("Volvo 7900 Hybrid", "bus", "Eco-friendly public transit bus", 190000, 17, 36, "bus"),
        ("Case IH Steiger", "tractor", "High horsepower tractor", 300000, 22, 36, "tractor"),
        ("New Holland T7", "tractor", "Multi-purpose farm tractor", 160000, 15, 24, "tractor"),
        ("Kawasaki Ninja", "motorcycle", "Express delivery motorcycle", 15000, 5, 6, "motorcycle"),
        ("BMW R 1250 GS", "motorcycle", "All-terrain transport motorcycle", 20000, 6, 12, "motorcycle"),
        ("Chevrolet Malibu", "car", "Corporate rental car", 28000, 6, 12, "car"),
        ("Honda Accord", "car", "Premium ride-sharing car", 32000, 7, 12, "car"),
        ("Mack Anthem", "truck", "Highway freight truck", 125000, 12, 18, "truck"),
        ("Freightliner Cascadia", "truck", "Fuel-efficient heavy truck", 140000, 14, 24, "truck"),
        ("Volkswagen Crafter", "van", "Spacious logistics van", 50000, 9, 12, "van"),
        ("Setra ComfortClass", "bus", "Premium charter bus", 220000, 19, 36, "bus"),
        ("Fendt 900 Vario", "tractor", "Advanced technology tractor", 280000, 21, 36, "tractor"),
        ("Suzuki Hayabusa", "motorcycle", "High-speed courier motorcycle", 18000, 5, 12, "motorcycle"),
    ]
    
    count = 0
    for name, v_type, desc, price, daily_roi, months, img_cat in vehicles:
        asset = InvestmentAsset.objects.filter(name=name).first()
        if asset:
            asset.image.name = f'invest/assets/{img_cat}.jpg'
            asset.save()
            count += 1
            print(f"Updated image for {name}")
    
    print(f"Updated {count} assets.")

if __name__ == '__main__':
    fix_images()
