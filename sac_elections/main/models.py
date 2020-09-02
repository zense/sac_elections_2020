from django.db import models
from django.utils import timezone
from datetime import datetime
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
def validate_batch_year(year):
	minYear = datetime.now().year - 5
	maxYear = datetime.now().year

	if year < minYear or year > maxYear:
		raise ValidationError(
				_("Invalid batch year")
		)

class UserProfile(models.Model):
	batch_programme = models.CharField(max_length = 10, default = "NOBATCH") # ex. 'IMT, MT...'
	batch_year = models.IntegerField(validators = [validate_batch_year])
	username = models.CharField(max_length = 255, unique = True) # ex. 'IMT2020518 John Doe'
	email = models.EmailField(max_length = 255, unique = True, validators = [validate_email])
	isCandidate = models.BooleanField(default = False)
	isAdmin = models.BooleanField(default = False) #for SAC and 2 of us, to access dashboard
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
		year = "0000"
		if re.match("^(IMT|MT|MS|DT|SMT)[0-9]*$", roll):
			batch = re.findall("^(IMT|MT|MS|DT|SMT)", roll)[0]
			year = re.findall("[0-9]{4}", roll)[0]

		user = UserProfile.objects.create(batch_programme = batch, batch_year = year, email = email, username = username, isCandidate = isCandidate, hasVoted = hasVoted )
		return user


	def __str__(self):
		return self.username



class Vote(models.Model):
	candidate = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = "candidate") # candidate voted
	time = models.DateTimeField("voted on", default = timezone.now)
	voter = models.OneToOneField(UserProfile, on_delete = models.RESTRICT, related_name = "voter", default = 0) # dont let the user delete after voting

	def __str__(self):
		return f"Vote by {self.voter} to {self.candidate}"