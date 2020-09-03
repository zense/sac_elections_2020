from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
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

	DEVS = "DV"
	IMTECHSAC = "IM"
	MTECHSAC = "MT"
	NA = "NA"
	
	ROLES = [
		(DEVS, "Developers"),
		(IMTECHSAC, "iMtech SAC"),
		(MTECHSAC, "Mtech SAC"),
		(NA, "Not Applicable"),
		]
	
	batch_programme = models.CharField(max_length = 10, default = "NOBATCH") # ex. 'IMT, MT...'
	batch_year = models.IntegerField(validators = [validate_batch_year]) # ex. 2019, 2018...
	batch = models.CharField(max_length = 20, default = "NOBATCH")
	username = models.CharField(max_length = 255, unique = True) # ex. 'IMT2020518 John Doe'
	email = models.EmailField(max_length = 255, unique = True, validators = [validate_email])
	isCandidate = models.BooleanField(default = False)
	role = models.CharField(max_length=2, choices=ROLES, default=NA) #admin roles
	gender = models.CharField(max_length = 2, default = "NA") # only for candidates. Use M and F
	vote_count = models.IntegerField(default=0)

	@staticmethod
	def findByEmail(email):
		try:
			return UserProfile.objects.get(email = email)
		except UserProfile.DoesNotExist:
			return None # returns None if not found, so that the user can be added

	# take username and get batch
	@staticmethod
	def createUser(username, email, isCandidate):
		roll = username.split(" ")[0]
		batch = "NOBATCH"
		year = "0000"
		if re.match("^(IMT|MT|MS|DT|SMT)[0-9]*$", roll):
			batch = re.findall("^(IMT|MT|MS|DT|SMT)", roll)[0]
			year = re.findall("[0-9]{4}", roll)[0]
		full_batch = batch + str(year)
		user = UserProfile.objects.create(batch_programme = batch, batch_year = year, batch = full_batch, email = email, username = username, isCandidate = isCandidate )
		return user

	# save batch from batch programme and batch year
	def save(self, *args, **kwargs):
		self.batch = self.batch_programme + str(self.batch_year)
		super(UserProfile, self).save(*args, **kwargs)

	def __str__(self):
		return self.username



class Vote(models.Model):
	candidate = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = "candidate") # candidate voted
	time = models.DateTimeField("voted on", default = timezone.now)
	voter = models.ForeignKey(UserProfile, on_delete = models.RESTRICT, related_name = "voter", default = 0) # dont let the user delete after voting
	category = models.CharField(max_length = 20, default = "NOBATCH")

	# override save to default category to candidate's batch
	def save(self, *args, **kwargs):
		if not self.category:
			self.category = self.candidate.batch + self.candidate.gender
		super(Vote, self).save(*args, **kwargs)

	def __str__(self):
		return f"Vote by {self.voter} to {self.candidate}"

	# make voter and category pair unique
	class Meta:
		# failsafe model level check for one vote per person
		unique_together = (('voter', 'category'), ('voter', 'candidate'))