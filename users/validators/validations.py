import re
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

def validate_phone(value):
  phone_regex = RegexValidator(
        regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
        message="O número de telefone deve estar no formato: '(XX) XXXXX-XXXX'."
    )
  
def validate_cpf(value):
  cpf_regex = RegexValidator(
        regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
        message="Use o formato 000.000.000-00.."
    )
  
def validate_min_value(value):
  MinValueValidator(value)

def validate_max_value(value):
  MaxValueValidator(value)
