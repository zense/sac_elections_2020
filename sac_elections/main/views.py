from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from main.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from main.graph_helper import get_user, get_calendar_events
import dateutil.parser
from django.http import HttpResponseForbidden


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

# <CalendarViewSnippet>
def calendar(request):
  context = initialize_context(request)

  token = get_token(request)

  events = get_calendar_events(token)

  if events:
    # Convert the ISO 8601 date times to a datetime object
    # This allows the Django template to format the value nicely
    for event in events['value']:
      event['start']['dateTime'] = dateutil.parser.parse(event['start']['dateTime'])
      event['end']['dateTime'] = dateutil.parser.parse(event['end']['dateTime'])

    context['events'] = events['value']

  return render(request, 'main/calendar.html', context)
# </CalendarViewSnippet>

def vote(request):
  if not request.session['user']['is_authenticated']:
    return HttpResponseForbidden()
  # temporary hardcode for voting
  votable = {'IMT2019': ['IMT2019'], 'IMT2018': ['IMT2019', 'IMT2018']} # {'voter' : 'candidate'}


  user = UserProfile.objects.get(id = request.session['user']['uid'])
  if not user:
    return HttpResponseForbidden() # should ideally never reach this state

  context = {}
  context['user'] = {
      'name': " ".join(user.username.split(" ")[1:]),
      'rollno': user.username.split(" ")[0],
      'batch_programme': user.batch_programme,
      'batch_year': user.batch_year,
      'is_authenticated': True,
    }
  context['votable'] = votable[user.batch_programme + str(user.batch_year)]

  return render(request, 'main/vote.html', context)