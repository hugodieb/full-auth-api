from django.db import models
from django.utils import timezone


class Stock(models.Model):
  symbol = models.CharField(max_length=10, unique=True)
  company_name = models.CharField(max_length=100)
  sector = models.CharField(max_length=50)
  last_update = models.DateTimeField(default=timezone.now())

  def __str__(self):
    return f"{self.symbol} - {self.company_name}"
  
class StockPrice(models.Model):
  stoke = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='prices')
  date = models.DateField()
  open_price = models.DecimalField(max_digits=10, decimal_places=2)
  close_price = models.DecimalField(max_digits=10, decimal_places=2)
  high = models.DecimalField(max_digits=10, decimal_places=2)
  low = models.DecimalField(max_digits=10, decimal_places=2)
  volume = models.BigIntegerField()

  class Meta:
    unique_together = ('stok', 'date')

class Dividend(models.Model):
  stok = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='dividends')
  date = models.DateField()
  value = models.DecimalField(max_digits=10, decimal_places=2)

  class Meta:
    unique_together = ('stock', 'date')

