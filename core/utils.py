import json
import random
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify
from core.models import Vehicle, Category, VehicleImage, VehicleFeature, GeminiAPIKey

def get_gemini_client():
    import google.generativeai as genai
    keys = GeminiAPIKey.objects.filter(is_active=True)
    if not keys.exists():
        raise Exception("No active Gemini API keys found.")
    # Auto-switch keys to avoid rate limits by picking a random one
    selected_key = random.choice(keys).key
    genai.configure(api_key=selected_key)
    return genai

def generate_vehicle_data(car_name):
    import random
    import re
    
    # Extract year if present
    year = 2024
    match = re.search(r'\b(20\d{2})\b', car_name)
    if match:
        year = int(match.group(1))
    
    # Extract make
    parts = car_name.split(' ')
    make = parts[1] if match and len(parts) > 1 else parts[0]
    
    # Generic realistic descriptions
    desc_template = f"<p>Experience the thrill of the {car_name}, an absolute marvel of modern automotive engineering. From its sleek, aerodynamic exterior to its meticulously crafted interior, every detail has been designed to provide an unparalleled driving experience.</p><p>Under the hood, it boasts a powerful engine that delivers responsive performance and exceptional handling. The premium cabin is equipped with state-of-the-art technology, ensuring both driver and passengers are connected, entertained, and comfortable throughout every journey.</p><p>Whether you're cruising through city streets or embarking on a long-distance road trip, the {car_name} offers the perfect blend of luxury, safety, and exhilaration. Don't miss the opportunity to elevate your daily drive.</p>"
    
    # Categories: suv, sedan, family, sports, heavy duty, electric, luxury
    category = 'Sedan' # default
    name_lower = car_name.lower()
    
    if any(x in name_lower for x in ['suv', 'g63', 'defender', 'cullinan', 'urus', 'purosangue', 'r1s', 'range rover']):
        category = 'SUV'
    elif any(x in name_lower for x in ['gt3', 'corvette', 'm5', 'rs6', 'nsx', 'gt-r', 'supra', 'mc20', 'chiron', 'jesko', 'utopia', 'nevera', 'amg gt', 'artura', '765lt']):
        category = 'Sports'
    elif any(x in name_lower for x in ['taycan', 'lucid', 'tesla']):
        category = 'Electric'
    elif any(x in name_lower for x in ['bentley', 'rolls-royce', 'aston martin']):
        category = 'Luxury'
    elif any(x in name_lower for x in ['silverado', 'f-150', 'ram', 'heavy']):
        category = 'Heavy Duty'
    elif any(x in name_lower for x in ['sienna', 'odyssey', 'pacifica', 'family']):
        category = 'Family'
        
    return {
        "make": make,
        "model": car_name.replace(str(year), '').replace(make, '').strip() or "Model",
        "year": year,
        "price": random.randint(150, 800) * 10,
        "mileage": random.randint(0, 15000),
        "fuel_type": "Electric" if category == 'Electric' else "Petrol",
        "transmission": "Automatic",
        "description": desc_template,
        "features": ["Leather Seats", "Apple CarPlay", "Sunroof", "Premium Audio", "Heated Seats", "Navigation System", "Backup Camera", "Bluetooth"],
        "category": category
    }

def fetch_vehicle_image(car_name, year):
    import subprocess
    import os
    import requests
    
    try:
        # Call the Node.js scraper
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fetch_image.mjs')
        result = subprocess.run(['node', script_path, car_name, str(year)], capture_output=True, text=True, check=True)
        img_src = result.stdout.strip()
        
        if img_src and img_src != 'NONE':
            # Download the image bytes
            img_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            img_res = requests.get(img_src, headers=img_headers, timeout=10)
            if img_res.status_code == 200:
                return img_res.content
    except Exception as e:
        print(f"Failed to fetch image for {car_name}: {e}")
        
    return None

def process_bulk_import(car_list_text):
    import re
    # Split by comma or newline
    cars = [c.strip() for c in re.split(r'[,\n]+', car_list_text) if c.strip()]
    results = []
    
    for car_name in cars:
        try:
            # 1. Generate Data
            data = generate_vehicle_data(car_name)
            
            # 2. Get or create category
            category, _ = Category.objects.get_or_create(
                name=data['make'],
                defaults={'slug': slugify(data['make'])}
            )
            
            # 3. Create Vehicle
            full_name = f"{data['year']} {data['make']} {data['model_name']}"
            vehicle = Vehicle.objects.create(
                name=full_name,
                category=category,
                make=data['make'],
                model=data['model_name'],
                year=data['year'],
                price_per_day=data['price_per_day'],
                full_price=data['full_price'],
                mileage=data['mileage'],
                condition=data['condition'],
                engine_type=data['engine_type'],
                drivetrain=data['drivetrain'],
                exterior_color=data['exterior_color'],
                interior_color=data['interior_color'],
                description=data['description'],
                status='available',
                financing_eligible=True
            )
            
            # 4. Attach Features
            for feat_name in data.get('features', []):
                feature, _ = VehicleFeature.objects.get_or_create(name=feat_name)
                vehicle.features.add(feature)
                
            # 4. Fetch Image
            search_query = f"{data['year']} {data['make']} {data['model_name']}"
            img_content = fetch_vehicle_image(search_query, data['year'])
            if img_content:
                file_name = f"{slugify(full_name)}.jpg"
                
                # Main Image
                vehicle.main_image.save(file_name, ContentFile(img_content), save=True)
                
                # Gallery Image
                VehicleImage.objects.create(
                    vehicle=vehicle,
                    image=vehicle.main_image
                )
                
            results.append({"name": full_name, "status": "success"})
        except Exception as e:
            results.append({"name": car_name, "status": f"error: {str(e)}"})
            
    return results

def generate_bill_of_sale_pdf(plan):
    from io import BytesIO
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from django.utils import timezone
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    Story = []
    
    title_style = styles['Heading1']
    title_style.alignment = 1
    Story.append(Paragraph("BILL OF SALE / PROOF OF OWNERSHIP", title_style))
    Story.append(Spacer(1, 20))
    
    normal_style = styles['Normal']
    normal_style.fontSize = 12
    normal_style.leading = 14
    
    text = """
    This document serves as the official Bill of Sale and Proof of Ownership for the vehicle described below,
    sold by RyderPro to the buyer listed below. The vehicle has been paid in full and is entirely owned by the buyer.
    """
    Story.append(Paragraph(text, normal_style))
    Story.append(Spacer(1, 20))
    
    user_name = plan.user.get_full_name() or plan.user.username
    vin = plan.vehicle.vin or 'N/A'
    
    details = f"""
    <b>Date of Document:</b> {timezone.now().strftime('%B %d, %Y')}<br/>
    <br/>
    <b>Buyer Information:</b><br/>
    Name: {user_name}<br/>
    Email: {plan.user.email}<br/>
    <br/>
    <b>Vehicle Information:</b><br/>
    Make: {plan.vehicle.make}<br/>
    Model: {plan.vehicle.model}<br/>
    Year: {plan.vehicle.year}<br/>
    VIN: {vin}<br/>
    <br/>
    <b>Financial Information:</b><br/>
    Total Purchase Price: ${plan.total_amount:,.2f}<br/>
    Total Amount Paid: ${plan.total_amount:,.2f}<br/>
    Balance Due: $0.00 (PAID IN FULL)<br/>
    """
    Story.append(Paragraph(details, normal_style))
    Story.append(Spacer(1, 40))
    
    Story.append(Paragraph("Authorized Signature: ___________________________", normal_style))
    Story.append(Paragraph("RyderPro Sales Department", normal_style))
    
    doc.build(Story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
