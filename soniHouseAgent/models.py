from django.db import models
from datetime import date, timedelta

# 🔵 Landlord Model
class Landlord(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=7)
    email = models.EmailField()
    address = models.TextField()
    id_card = models.CharField(max_length=50)  
    is_deleted = models.BooleanField(default=False) #this is to enanle bin restre

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    # 🔁 For all three models

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()



# 🏠 House Model
class House(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)  # Monthly price
    location = models.CharField(max_length=255)
    num_bedrooms = models.IntegerField()
    num_bathrooms = models.IntegerField()
    is_available = models.BooleanField(default=True)
    listed_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='house_images/', blank=True, null=True)

    owner = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name='houses')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.location}"
    # 🔁 For all three models

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()



# 👤 Tenant Model
class Tenant(models.Model):
    PAYMENT_OPTIONS = [
        ('6_months', '6 Months'),
        ('1_year', '1 Year'),
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    id_card = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=7)
    house = models.OneToOneField(House, on_delete=models.CASCADE)
    move_in_date = models.DateField(auto_now_add=True)
    payment_option = models.CharField(max_length=10, choices=PAYMENT_OPTIONS)
    last_payment_date = models.DateField(auto_now_add=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    has_paid = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)# bin check for delete

    def save(self, *args, **kwargs):
        # Automatically calculate payment amount based on house price and payment duration
        if self.house and self.house.price:
            if self.payment_option == '6_months':
                self.payment_amount = self.house.price * 6
            elif self.payment_option == '1_year':
                self.payment_amount = self.house.price * 12
            else:
                self.payment_amount = self.house.price  # default fallback

        # Mark house as unavailable if it is currently available
        if self.house.is_available:
            self.house.is_available = False
            self.house.save()

        super().save(*args, **kwargs)

    def get_next_due_date(self):
        if self.payment_option == '6_months':
            return self.last_payment_date + timedelta(days=182)
        elif self.payment_option == '1_year':
            return self.last_payment_date + timedelta(days=365)
        return self.last_payment_date

    def get_payment_status(self):
        today = date.today()
        due_date = self.get_next_due_date()
        if not self.has_paid and today > due_date:
            return 'overdue'
        elif self.has_paid and (due_date - today).days <= 30:
            return 'due_soon'
        return 'paid'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.house.title}"

    # 🔁 For all three models

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
