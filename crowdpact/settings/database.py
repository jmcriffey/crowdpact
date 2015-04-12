import dj_database_url

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
dev_defaults = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'crowdpact_dev',
    'USER': 'crowdpact_dev',
    'PASSWORD': 'crowdpact_dev',
    'HOST': 'localhost',
}

print dj_database_url.config()

DATABASES = {
    'default': dj_database_url.config() or dev_defaults
}
