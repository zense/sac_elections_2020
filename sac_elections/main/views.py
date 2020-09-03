from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from main.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from main.graph_helper import get_user, get_calendar_events
import dateutil.parser
from django.core.exceptions import PermissionDenied



# controller level check for unique voting
def assertNotVoted(user, category):
  voted = Vote.objects.filter(voter = user, category = category)
  if voted:
    raise PermissionDenied("You have already voted for this category")

# returns the votable dictionary
def getVotableHash():
  votable = {'IMT2019': ['IMT2019M', 'IMT2019F'], 'IMT2018': ['IMT2019M', 'IMT2019F', 'IMT2018M', 'IMT2018F']} # {'voter' : 'candidate'}
  return votable

def canVoteCategory(user, category):
  return category in getVotableHash()[user.batch_programme + str(user.batch_year)]

# Function returns user from session, raises 403 if not found
def requireValidUser(request):
  if 'user' not in request.session or 'uid' not in request.session['user']:
    raise PermissionDenied("You must be logged in to access this page")

  user = UserProfile.objects.filter(id = request.session['user']['uid'])[0]
  if not user:
    raise PermissionDenied("You must be logged in to access this page")

  return user

# <HomeViewSnippet>
def home(request):
  context = initialize_context(request)
  return render(request, 'main/home.html', context)
# </HomeViewSnippet>

# <InitializeContextSnippet>
def initialize_context(request):
  context = {}

  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  # context['user'] = request.session.get('user', {'is_authenticated': False})
  if request.session.get('user', False):
    user = UserProfile.objects.get(id = request.session['user']['uid'])
    context['user'] = {
      'name': " ".join(user.username.split(" ")[1:]),
      'rollno': user.username.split(" ")[0],
      'batch_programme': user.batch_programme,
      'batch_year': user.batch_year,
      'is_authenticated': True,
    }
  else:
    context['user'] = {
      'is_authenticated': False,
    }
  return context
# </InitializeContextSnippet>

# <SignInViewSnippet>
def sign_in(request):
  # Get the sign-in URL
  sign_in_url, state = get_sign_in_url()
  # Save the expected state so we can validate in the callback
  request.session['auth_state'] = state
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(sign_in_url)
# </SignInViewSnippet>

# <SignOutViewSnippet>
def sign_out(request):
  # Clear out the user and token
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('home'))
# </SignOutViewSnippet>

# <CallbackViewSnippet>
def callback(request):
  # Get the state saved in session
  expected_state = request.session.pop('auth_state', '')
  # Make the token request
  token = get_token_from_code(request.get_full_path(), expected_state)

  # Get the user's profile
  user = get_user(token)

  # Save token and user
  store_token(request, token)
  store_user(request, user)

  return HttpResponseRedirect(reverse('home'))
# </CallbackViewSnippet>

# @login_required(login_url="/")
def vote(request):
  user = requireValidUser(request)

  votable =  getVotableHash()

  context = {}
  context['user'] = {
      'name': " ".join(user.username.split(" ")[1:]),
      'rollno': user.username.split(" ")[0],
      'batch_programme': user.batch_programme,
      'batch_year': user.batch_year,
      'is_authenticated': True,
    }
  context['votable'] = votable[user.batch_programme + str(user.batch_year)]
  votes = Vote.objects.filter(voter = user)
  voted_cats = [ vote.candidate.batch_programme + str(vote.candidate.batch_year) for vote in votes] # voted categories
  context['voted_cats'] = voted_cats

  return render(request, 'main/vote.html', context)


def dashboard(request):

  user = requireValidUser(request)
  if not user.isAdmin:
    return render(request, 'http/401.html', {"message": "Only admins can access this page"}, status = 401)
  #TEMPORARY LIST
  batches = {'IMT' : [2018, 2019] }

  context = {}
  context = initialize_context(request)
  context['candidates'] = {}
  
  for program in batches.keys():
    candidates = UserProfile.objects.filter( batch_programme = program )
    candidates = candidates.filter( isCandidate = True )

    for year in batches[program]:
      candidates_1 = candidates.filter( batch_year=year )
      
      context['candidates'][str(program) + str(year)] = candidates_1

  # print( context )

  
  return render(request, 'main/dashboard.html', context)


def poll(request, category):

  user = requireValidUser(request)
  votable = getVotableHash()
  assertNotVoted(user, category)

  # TODO: raise 404 if invalid category

  if not canVoteCategory(user, category):
    raise PermissionDenied("You are not permitted to vote for this category")

  # TODO: handle post here

  # category[:-1] is the batch, category[-1] is the gender
  context = {}
  candidates = UserProfile.objects.filter(batch = category[:-1], gender = category[-1])
  context['candidates'] = candidates

  return render(request, 'main/poll.html', context)
