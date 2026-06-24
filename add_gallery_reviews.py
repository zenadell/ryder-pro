import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import Vehicle, VehicleImage, Review
from django.core.files.base import ContentFile
import urllib.request

def run():
    vehicles = Vehicle.objects.all()[:5]
    
    review_contents = [
        "Absolutely amazing vehicle. Drives like a dream and the interior is spotless.",
        "Great experience! The car was exactly as described. Highly recommended.",
        "Smooth process from start to finish. The vehicle performed perfectly on our trip.",
        "Very comfortable and fuel efficient. Will definitely rent again.",
        "Stunning car! Got so many compliments. Worth every penny."
    ]
    reviewers = ["John Doe", "Sarah Jenkins", "Michael Chen", "Emily Davis", "Robert Smith"]
    
    # We will use the car's main image as dummy gallery images to just populate it
    count_imgs = 0
    count_revs = 0
    
    for v in vehicles:
        # Add 3 reviews
        for i in range(3):
            Review.objects.get_or_create(
                vehicle=v,
                title="Fantastic Car",
                content=random.choice(review_contents),
                rating=random.randint(4, 5),
                reviewer_name=random.choice(reviewers)
            )
            count_revs += 1
            
        # Add 3 gallery images if the car has a main image
        if v.main_image and not v.images.exists():
            for i in range(3):
                VehicleImage.objects.create(
                    vehicle=v,
                    image=v.main_image, # reusing main image as dummy gallery image for now
                    order=i
                )
                count_imgs += 1

    print(f"Added {count_revs} reviews and {count_imgs} gallery images.")

if __name__ == '__main__':
    run()
