from django.db import models
import datetime

class BannedDate(models.Model):
    date = models.DateField()

    def __str__(self):
        return str(self.date)

class Room(models.Model):
    title = models.CharField(max_length=60)
    image = models.ImageField()
    active = models.BooleanField(default=True)
    description = models.TextField()
    banned_dates = models.ManyToManyField(BannedDate, blank=True, help_text='You may ban certain dates from being reserved for this room by adding them to this list.')
    amount_per_night = models.IntegerField(help_text='Amount in USD')
        
    def __str__(self):
        return self.title

    @classmethod
    def is_avaliable(self, start_date, end_date, room):
        date_format = '%Y-%m-%d'
        a = datetime.datetime.strptime(start_date, date_format)
        b = datetime.datetime.strptime(end_date, date_format)
        query = Reservation.objects.filter(
            models.Q(start_date__gte=start_date), 
            models.Q(end_date__lte=end_date), 
            models.Q(room=room)).exists()

        return query

    def to_json(self):
        return {
            "title": self.title,
            "image": self.image.url,
            "amount_per_night": self.amount_per_night
        }

class Reservation(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    stripe_id = models.CharField(max_length=120, blank=True)
    stripe_payment_intent = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=15, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


