from django import template
from django.template.defaultfilters import stringfilter
import json

#custom filters
#https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/#template-filters-that-expect-strings

register = template.Library()

@register.filter(name="disp")
@stringfilter
def getCategoryDisplayNames(value):

  DISPLAY_NAMES = {
    'MT2020M': "Master's Male SAC",
    'MT2020F': "Master's Female SAC",
    'MT2020M1': "Master's Male SAC 1",
    'MT2020M2': "Master's Male SAC 2",
    'MT2020F1': "Master's Female SAC 1",
    'MT2020F2': "Master's Female SAC 2",
    'IMT2019M1': "iMtech 2019 Male SAC",
    'IMT2019F1': "iMtech 2019 Female SAC",
    'IMT2018M1': "iMtech 2018 Male SAC",
    'IMT2018F1': "iMtech 2018 Female SAC",
    'IMT2019M': "iMtech 2019 Male SAC",
    'IMT2019F': "iMtech 2019 Female SAC",
    'IMT2018M': "iMtech 2018 Male SAC",
    'IMT2018F': "iMtech 2018 Female SAC",
    'imtech': "iMtech",
    'mtech': "Master's"
  }

  try:
    name = DISPLAY_NAMES[value]
  except:
    name = ''
  
  return name

@register.filter(name="disp_1")
@stringfilter
def getCategoryDisplayNames(value):

  DISPLAY_NAMES = {
    'MT2020M1': "Master's SAC Nominee",
    'MT2020M2': "Master's SAC Nominee",
    'MT2020F1': "Master's SAC Nominee",
    'MT2020F2': "Master's SAC Nominee",
    'IMT2019M1': "iMtech 2019 SAC Nominee",
    'IMT2019F1': "iMtech 2019 SAC Nominee",
    'IMT2018M1': "iMtech 2018 SAC Nominee",
    'IMT2018F1': "iMtech 2018 SAC Nominee",
    'F': 'Female',
    'M': 'Male'
  }

  try:
    name = DISPLAY_NAMES[value]
  except:
    name = ''
  
  return name


@register.filter(name="getslug")
@stringfilter
def getSlug(value):
  SLUG_VALUES = {
    'IMT': 'imtech',
    'MT': 'mtech',
    'DT': 'mtech',
    'MS': 'mtech',
    'PH': 'mtech',
  }

  try:
    slug = SLUG_VALUES[value]
  except:
    slug = ''
  
  return slug

  return SLUG_VALUES


@register.filter(name="gethash")
@stringfilter
def getCategoryDisplayNames(value):
  value = value
  batch, hashed = value.split("@#@")
  hashed = hashed.replace("\'","\"")
  hashed = json.loads(hashed)
  return hashed[batch]
