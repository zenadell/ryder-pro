import os

filepath = '/Users/mac/Desktop/ryder-pro/core/models.py'
with open(filepath, 'r') as f:
    content = f.read()

# I need to restore the Review model properly.
import re

review_model_bad = """class Review(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} star - {self.vehicle.name} by {self.reviewer_name}"
"""

review_model_good = """class Review(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    reviewer_name = models.CharField(max_length=255)
    reviewer_image = models.ImageField(upload_to='reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer_name}"
"""

content = content.replace(review_model_bad, review_model_good)

with open(filepath, 'w') as f:
    f.write(content)
print("Restored Review model.")
