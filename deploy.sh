#!/bin/sh

echo '--- deployment started ----'

# Push
git push heroku master

# Migrate
heroku run 'python manage.py migrate'

# Build
heroku run '(cd crowdpact/static && npm run build)'

# Collect
heroku run 'python manage.py collectstatic --noinput'

echo '--- deployment finished ---'
