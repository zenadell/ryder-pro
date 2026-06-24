import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import BlogPost, Vehicle

def run():
    vehicles = list(Vehicle.objects.exclude(main_image=''))
    
    posts = [
        {
            "title": "Top 5 Luxury SUVs for the Ultimate Family Road Trip",
            "excerpt": "When it comes to family vacations, comfort and space are non-negotiable. Discover why these top 5 luxury SUVs offer the perfect blend of performance and premium amenities.",
            "content": """<h3>The Importance of Comfort on Long Drives</h3>
<p>Planning a family road trip is exciting, but nothing ruins the mood faster than a cramped back seat. A luxury SUV ensures that every passenger, from the front row to the third row, enjoys the journey as much as the destination.</p>
<h4>1. The Premium Experience</h4>
<p>Modern luxury SUVs offer features like multi-zone climate control, panoramic sunroofs, and advanced entertainment systems. Vehicles like the Cadillac Escalade or Range Rover provide an unmatched level of refinement.</p>
<h4>2. Safety First</h4>
<p>When traveling with family, safety is paramount. These vehicles come equipped with the latest advanced driver assistance systems (ADAS), including adaptive cruise control and lane-keeping assist.</p>
<p>Ready to hit the road? Browse our premium SUV collection today and elevate your next family adventure.</p>"""
        },
        {
            "title": "Why Renting a Porsche 911 Will Change Your Weekend",
            "excerpt": "Looking to inject some adrenaline into your weekend? Here is why getting behind the wheel of a Porsche 911 is an experience every driving enthusiast must have.",
            "content": """<h3>The Legacy of the 911</h3>
<p>There is arguably no sports car more iconic than the Porsche 911. With its distinctive silhouette and rear-engine layout, it has been the benchmark for performance for decades.</p>
<h4>The Driving Dynamics</h4>
<p>What makes the 911 truly special is its steering feel and chassis balance. Renting one for the weekend allows you to experience carving through canyon roads or cruising along the coast with unparalleled precision.</p>
<h4>A Symphony of Sound</h4>
<p>The flat-six engine note is legendary. Whether you opt for a naturally aspirated model or a modern turbocharged Carrera, the acoustic experience is half the thrill.</p>
<p>Don't just dream about it. Book a Porsche 911 with us and make your weekend unforgettable.</p>"""
        },
        {
            "title": "Electric Vehicles: The Future of Premium Car Rentals",
            "excerpt": "As EV technology advances rapidly, more renters are opting for electric luxury. From silent cabins to instant torque, see why an EV might be your best choice.",
            "content": """<h3>The Silent Luxury</h3>
<p>One of the most defining characteristics of an electric vehicle is the absolute silence of the cabin. Without the noise and vibration of a combustion engine, the driving experience becomes incredibly serene and relaxing.</p>
<h4>Instant Performance</h4>
<p>Don't confuse silence with sluggishness. EVs like the Tesla Model S or Porsche Taycan offer instant torque, providing acceleration that easily rivals traditional supercars.</p>
<h4>Eco-Friendly Travel</h4>
<p>Renting an EV allows you to travel guilt-free, knowing you are producing zero tailpipe emissions while still enjoying a premium driving experience. Plus, with the growing network of fast chargers, range anxiety is becoming a thing of the past.</p>"""
        },
        {
            "title": "The Best Scenic Routes for Your Next Convertible Rental",
            "excerpt": "Nothing beats the feeling of the wind in your hair and the sun on your face. We have compiled the ultimate list of scenic routes perfect for a convertible.",
            "content": """<h3>Pacific Coast Highway, California</h3>
<p>Arguably the most famous coastal drive in the world. The PCH offers stunning views of the Pacific Ocean, dramatic cliffs, and winding roads that are perfect for a convertible like the Mazda MX-5 or a drop-top Mustang.</p>
<h4>The Amalfi Coast, Italy</h4>
<p>If your travels take you to Europe, the Amalfi Coast is a must-drive. The narrow, twisting roads and breathtaking cliffside villages demand a nimble, open-top vehicle.</p>
<h4>Tips for Open-Top Driving</h4>
<p>Always remember sunscreen, sunglasses, and a good hat! The sun can be deceiving when the wind is keeping you cool.</p>
<p>Browse our convertible selection and start planning your scenic getaway.</p>"""
        },
        {
            "title": "How to Choose the Right Rental Car for Your Business Trip",
            "excerpt": "Making a good impression is crucial in business. Learn how to select a rental vehicle that perfectly balances professionalism, comfort, and practicality.",
            "content": """<h3>First Impressions Matter</h3>
<p>Pulling up to a client meeting in a clean, sophisticated executive sedan sets a tone of professionalism before you even step out of the car. Vehicles like the Mercedes-Benz E-Class or BMW 5 Series are perfect choices.</p>
<h4>Comfort for the Commute</h4>
<p>Business trips often involve long hours and stressful schedules. A comfortable, quiet cabin with excellent connectivity features allows you to decompress or take important calls on the go.</p>
<h4>Practical Considerations</h4>
<p>Consider your luggage needs and the driving environment. If you're navigating tight city streets, a compact luxury car might be more practical than a large sedan.</p>"""
        }
    ]
    
    count = 0
    for post_data in posts:
        blog, created = BlogPost.objects.get_or_create(
            title=post_data['title'],
            defaults={
                'excerpt': post_data['excerpt'],
                'content': post_data['content'],
            }
        )
        if created:
            # Assign a random image from a vehicle if available
            if vehicles:
                v = random.choice(vehicles)
                blog.featured_image = v.main_image
                blog.save()
            count += 1
            
    print(f"Successfully generated {count} dummy blog posts!")

if __name__ == '__main__':
    run()
