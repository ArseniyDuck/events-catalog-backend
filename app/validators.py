from django.core.validators import RegexValidator

phone_validator = RegexValidator(
   regex=r'^\+?1?\d{11}$',
   message='Phone number must be entered in the format: \'+XXXXXXX\'. Only 11 digits allowed.'
)

color_validator = RegexValidator(
   regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
   message='Color must be in hex'
)