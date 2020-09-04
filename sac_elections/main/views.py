from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from main.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from main.graph_helper import get_user, get_calendar_events
import dateutil.parser
from django.core.exceptions import PermissionDenied, SuspiciousOperation


## HELPER FUNCTIONS

# controller level check for unique voting
def assertNotVoted(user, category):
  voted = Vote.objects.filter(voter = user, category = category)
  if voted:
    raise PermissionDenied("You have already voted for this category")

def getCategories():
  MTECH_CANDIDATES = ['MT2020F1', 'MT2020F2', 'MT2020M1', 'MT2020M2']
  IMTECH_CANDIDATES = ['IMT2019M1', 'IMT2019F1', 'IMT2018M1', 'IMT2018F1']

  return {'imtech': IMTECH_CANDIDATES, 'mtech': MTECH_CANDIDATES}
# returns the votable dictionary
def getVotableHash():
  
  MTECH_CANDIDATES = getCategories()['mtech']
  IMTECH_CANDIDATES = getCategories()['imtech']
  # {'voter' : 'candidate'}
  votable = {
    'IMT2019': ['IMT2019M1', 'IMT2019F1'], 
    'IMT2018': IMTECH_CANDIDATES,
    'IMT2017': IMTECH_CANDIDATES,
    'MT2020': MTECH_CANDIDATES,
    'DT2020': MTECH_CANDIDATES,
    'MS2020': MTECH_CANDIDATES,
    'PH2020': MTECH_CANDIDATES,
    }
  return votable

# What all batches can vote
def checkBatch(batch):
  if batch not in getVotableHash().keys():
    raise PermissionDenied("Sorry, you are not allowed to vote")

# What all categories exist
def checkCategory(category):
  MTECH_CANDIDATES = getCategories()['mtech']
  IMTECH_CANDIDATES = getCategories()['imtech']
  MTECH_CANDIDATES.extend(IMTECH_CANDIDATES)
  return category in MTECH_CANDIDATES

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

def getCandidatesWithVoteCount():
  MTECH_CANDIDATES = getCategories()['mtech']
  categories = getCategories()['imtech']
  categories.extend(MTECH_CANDIDATES)
  votes = {}
  for category in categories:
    # TODO: remove hardcode
    batch = [category[:-2]]
    if category[:-2] == "MT2020":
      batch = ['MT2020', 'DT2020', 'MS2020', 'PH2020']
    candidates = UserProfile.objects.filter(batch__in = batch, isCandidate = True)
    votes[category[:-2]] = {}
    for candidate in candidates:
      votes[category[:-2]][candidate.username] = Vote.objects.filter(candidate = candidate).count() 
  
  return votes

## CONTROLLER FUNCTIONS

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
      'role': user.role,
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
  url_query = request.GET.get('m')
  votable =  getVotableHash()

  checkBatch(user.batch)
    
  context = {}
  context['user'] = {
      'name': " ".join(user.username.split(" ")[1:]),
      'rollno': user.username.split(" ")[0],
      'batch_programme': user.batch_programme,
      'batch_year': user.batch_year,
      'is_authenticated': True,
      'role': user.role,
    }
  context['votable'] = votable[user.batch]
  votes = Vote.objects.filter(voter = user)
  voted_cats = [ vote.category for vote in votes] # voted categories
  context['voted_cats'] = voted_cats
  context['q'] = "Your vote was recorded" if url_query == 'done' else None

  return render(request, 'main/vote.html', context)


def dashboard(request):

  batches={}
  user = requireValidUser(request)
  if user.role == 'NA':
    return render(request, 'http/401.html', {"message": "Only admins can access this page"}, status = 401)
  if user.role == 'DV':
    batches = {'IMT' : [2018, 2019], 'MT' : [2020] } #DEV
  if user.role == 'IM':
    batches = {'IMT' : [2018, 2019] } #IMTECH SAC
  if user.role == 'MT':
    batches = {'MT' : [2020] } #MTECH_SAC

  print(getCandidatesWithVoteCount())
  return HttpResponse(200)

  # context = {}
  # context = initialize_context(request)
  # context['candidates'] = {}
  
  # for program in batches.keys():
  #   candidates = UserProfile.objects.filter( batch_programme = program )
  #   candidates = candidates.filter( isCandidate = True )

  #   for year in batches[program]:
  #     candidates_1 = candidates.filter( batch_year=year ).order_by( '-vote_count' )
      
  #     context['candidates'][str(program) + str(year)] = candidates_1

  # print( context )

  
  return render(request, 'main/dashboard.html', context)


def poll(request, category):

  user = requireValidUser(request)
  votable = getVotableHash()
  assertNotVoted(user, category)

  checkBatch(user.batch)

  if not checkCategory(category):
    return render(request, 'http/404.html', {'message': "Invalid voting category"}, status = 404)

  if not canVoteCategory(user, category):
    raise PermissionDenied("You are not permitted to vote for this category")

  # category[:-2] is the batch, category[-2:-1] is the gender
  # TODO: remove hardcode
  context = {}
  batch = [category[:-2]]
  # let MS, PH candidates contest for MTECH elections
  if category[:-2] == "MT2020":
    batch = ['MT2020', 'DT2020', 'MS2020', 'PH2020']
  candidates = UserProfile.objects.filter(batch__in = batch, gender = category[-2:-1], isCandidate = True)
  context['candidates'] = candidates
  context['user'] = {
      'name': " ".join(user.username.split(" ")[1:]),
      'rollno': user.username.split(" ")[0],
      'batch_programme': user.batch_programme,
      'batch_year': user.batch_year,
      'is_authenticated': True,
      'role': user.role,
    }

  return render(request, 'main/poll.html', context)

def confirmation(request, category):
  if request.method != 'POST':
    return render(request, 'http/405.html', {'message': 'Invalid http method for the resource'} ,status = 405)
  user = requireValidUser(request)
  assertNotVoted(user, category)

  # legitimacy checks
  checkBatch(user.batch)
  if not checkCategory(category):
    return render(request, 'http/404.html', {'message': "Invalid voting category"}, status = 404)

  if not canVoteCategory(user, category):
    raise PermissionDenied("You are not permitted to vote for this category")

  # post data checks
  email = request.POST.get('vote', None)
  if not email:
    raise SuspiciousOperation('The request was cancelled')

  candidate = UserProfile.findByEmail(email)

  if not candidate:
    raise SuspiciousOperation('The request was cancelled')

  # Prevent cross category request forgery
  # TODO: remove hardcode
  batch = [category[:-2]]
  if category[:-2] == "MT2020":
    batch = ['MT2020', 'DT2020', 'MS2020', 'PH2020']

  if candidate.batch not in batch:
    raise SuspiciousOperation('The request was cancelled due to attempt at request forgery')

  # if not after confirmation
  if not request.POST.get('confirm', False):
    context = {}
    context['candidate'] = candidate
    context['category'] = category
    context['user'] = {
      'name': " ".join(user.username.split(" ")[1:]),
      'rollno': user.username.split(" ")[0],
      'batch_programme': user.batch_programme,
      'batch_year': user.batch_year,
      'is_authenticated': True,
      'role': user.role,
    }
    return render(request, 'main/confirm.html', context)

  else:
    # create and save the vote
    vote = Vote.objects.create(candidate = candidate, voter = user, category = category)
    # increment candidate's vote_count, easier for dashboard
    vote.save()

    # return redirect(reverse('vote', kwargs={'m': "done"}))
    return redirect('/vote/?m=done')
