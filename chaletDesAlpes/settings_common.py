# -*- coding: utf-8 -*-
############################ COMMON SETTINGS ###########################
"""
Django settings for chaletDesAlpes project.
The settings in this file are purported to be used in both
developpemnt and deployment phase 
"""
########################################################################



############################### BASE PATH ##############################
import os
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
# if the absoulte name of the settings file is 
#/pathToTheProject/projectName/projectName/settings.py
#the base_path is then : pathToTheProject/projectName

################################# DEBUG ################################
DEBUG = True
TEMPLATE_DEBUG = DEBUG 

########################### GEOIP DIRECTORY ############################
GEOIP_PATH=BASE_PATH +"/geoip/"


################################# EMAIL ################################
#not defined in this file


##################### ADMINISTRATION AND SECURITY ######################
#not defined in this file


############################## DATABASE ################################
#not defined in this file


########################## LANGUAGE AND I18N ###########################
TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'fr-FR'
USE_I18N = True  
USE_L10N = True
USE_TZ = True

SITE_ID = 1 #id used int he django_site databse, 
#useful to save data from diferent websites in a single database
gettext = lambda x: x # we create a false gettext function in order to 
#avoid importing django.utils.translation
#for this might cause an infinite import loop

LANGUAGES = (
   ('fr', gettext('French')),
   ('en', gettext('English')),
)


############################ PATHS AND URLS ############################
STATIC_URL = '/static/'
APPEND_SLASH = True  # Ajoute un slash en fin d'URL
STATICFILES_DIRS = (
BASE_PATH +"/static/",#directory name to put static files: JS CSS Imgs
)
MEDIA_ROOT=BASE_PATH +"/media/" 
MEDIA_URL="/media/" # is the URL that makes the static media accessible over HTTP.
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

TEMPLATE_DIRS = (
  BASE_PATH +'/templates/'
)
#path to the translation files
LOCALE_PATHS = (
    BASE_PATH +'/locale/',
)
# The absolute path to the directory where collectstatic will collect 
#static files for deployment.
STATIC_ROOT = BASE_PATH + '/static_collected/'
# URL to use when referring to static files located in STATIC_ROOT.
# Examples: "/static/", "http://static.example.com/"
STATIC_URL = '/static/'

########################### TEMPLATE_LOADERS ###########################
#not defined in this file (useless in developpement)


########################## MIDDLEWARE_CLASSES ##########################
#The order in MIDDLEWARE_CLASSES matters because a middleware can depend
#on others. For instance, AuthenticationMiddleware stores the 
#authenticated user in the session; therefore, it must run after 
#SessionMiddleware.
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware', #for i18n
    'website.middleware.ViewNameMiddleware',#to have access to the view name
)



############################ INSTALLED APPS ############################
INSTALLED_APPS = (
    'django.contrib.sites',     # not used in production
    'django.contrib.admindocs', # not used in production
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'nouvelles',
    'django.contrib.formtools',
    'django_cleanup', 
    'south',
    'visites',
    'captcha', # used in website/forms.py to intall:pip install  django-simple-captcha 
)

###################### TEMPLATE_CONTEXT_PROCESSORS #####################
TEMPLATE_CONTEXT_PROCESSORS = (
"django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n", # for i18n ; important for the set_language redirect view
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages",
#"chaletDesAlpes.context_processors.view_name_context_processor",
)

########################### TEMPLATE_LOADERS ###########################
# List of callables that know how to import templates from various
#sources - only used in production
TEMPLATE_LOADERS = (
#    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
#    )),
)
################################# DEBUG ################################
DEBUG = True
TEMPLATE_DEBUG = DEBUG 
# this value might be changed by the  settings_deployement.py 
#called by the script init.py

ROOT_URLCONF = 'chaletDesAlpes.urls'

######################## LUKE ICH BIN DEIN VATER #######################
WSGI_APPLICATION = 'chaletDesAlpes.wsgi.application'

ALLOWED_HOSTS = '*'

