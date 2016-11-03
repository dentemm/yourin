from django.core.exceptions import ValidationError

def validate_image_min(value):

	if value.width < 600 or value.height < 330:
		raise ValidationError('Deze afbeelding voldoet niet aan de minimum afmeting vereisten (600x330px)')

def validate_blog_image(value):

	if value.width < 600 or value.height < 330:
		raise ValidationError('Een blog afbeelding dient tenminste 500x500px te zijn')