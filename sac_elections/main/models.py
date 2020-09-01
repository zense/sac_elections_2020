from django.db import models
from django.utils import timezone

def validate_email(email_value):

	VALID_DOMAIN = [
		'iiitb.org',
		'iiitb.ac.in',
	]

	email_domain = email_value[ email_value.find('@')+1:]

	if email_domain not in VALID_DOMAIN:
		raise ValidationError(
				_( str(email_domain) + " is not a valid domain."),
		)
class User(models.Model):
	batch = models.CharField(max_length = 10) # ex. 'IMT, MT...'
	userame = models.CharField(max_length = 255, unique = True) # ex. 'IMT2020518 John Doe'
	email = models.EmailField(max_length = 255, unique = True, validators = [validate_email])
	isCandidate = models.BooleanField(default = False)


	def __str__(self):
		return self.username

class Vote(models.Model):
	candidate = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "candidate") # candidate voted
	voter = models.OneToOneField(User, unique = True, on_delete = models.RESTRICT, related_name = "voter") # Dont let the profile be deleted if they cast a vote
	time = models.DateTimeField("voted on", default = timezone.now)

	def __str__(self):
		return f"Vote by {self.voter} to {self.candidate}"