from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
import re

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
class UserProfile(models.Model):
	batch = models.CharField(max_length = 10, default = "NOBATCH") # ex. 'IMT, MT...'
	username = models.CharField(max_length = 255, unique = True) # ex. 'IMT2020518 John Doe'
	email = models.EmailField(max_length = 255, unique = True, validators = [validate_email])
	isCandidate = models.BooleanField(default = False)
	hasVoted = models.BooleanField(default = False)

	@staticmethod
	def findByEmail(email):
		try:
			return UserProfile.objects.get(email = email)
		except UserProfile.DoesNotExist:
			return None # returns None if not found, so that the user can be added

	# take username and get batch
	@staticmethod
	def createUser(username, email, isCandidate, hasVoted):
		roll = username.split(" ")[0]
		batch = "NOBATCH"
		if re.match("^(IMT|MT|MS|DT|SMT)[0-9]*$", roll):
			batch = re.findall("^(IMT|MT|MS|DT|SMT)", roll)[0]

		user = UserProfile.objects.create(batch = batch, email = email, username = username, isCandidate = isCandidate, hasVoted = hasVoted )
		return user


	def __str__(self):
		return self.username



class Vote(models.Model):
	candidate = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = "candidate") # candidate voted
	time = models.DateTimeField("voted on", default = timezone.now)
	# for anonimity do not store the voter

	def __str__(self):
		return f"Vote id {self.id} to {self.candidate}"