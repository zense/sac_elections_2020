import random
import pprint
import json

def generate_candidates(count):

  batches={
    'IMT': [2018, 2019],
    'MT': [2020]
    }

  candidates = []

  for n in range(1, count+1):
    program = random.choice( list(batches.keys()) )
    year = random.choice( batches[program] )

    username = "_".join( ["candidate", str(program), str(year), str(n)] )
    email = username + "@iiitb.org"
    batch = program + str(year)
    gender = random.choice( ["M", "F"] )

    user = {
      "model": "main.UserProfile",
      "pk": n,
      "fields": {
        "batch_programme": str(program),
        "batch_year": year,
        "batch": batch,
        "username": username,
        "email": email,
        "isCandidate": "True",
        "gender": gender,
      }
    }
    candidates.append(user)

  pprint.pprint( candidates)

  return candidates

candidates = generate_candidates(10)

with open( "./fixtures/candidates.json", mode='w') as outfile:
  json.dump(candidates, outfile)