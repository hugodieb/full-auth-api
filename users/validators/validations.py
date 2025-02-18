import re
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

def validate_phone(value):
  phone_regex = RegexValidator(
        regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
        message="O número de telefone deve estar no formato: '(XX) XXXXX-XXXX'."
    )
  return phone_regex
  
def validate_cpf(cpf):
  
  cpf = re.sub(r'[^0-9]', '', str(cpf))  

  if len(cpf) != 11:
    return False
  
  if cpf == cpf[0] * 11:
    return False
  
  soma = 0
  for i in range(9):
    soma += int(cpf[i]) * (10 - i)
  resto = soma % 11
  first_digit = 0 if resto < 2 else 11 - resto

  soma = 0
  for i in range(10):
    soma += int(cpf[i]) * (11 - i)
  resto = soma % 11
  second_digit = 0 if resto < 2 else 11 - resto

  return int(cpf[9]) == first_digit and int(cpf[10]) == second_digit
  
def validate_min_value(value):
  return MinValueValidator(value)

def validate_max_value(value):
  return MaxValueValidator(value)
