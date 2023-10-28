from django.contrib import admin

from credentials_app.models import User, Credentials, BlacklistToken

admin.site.register(User)
admin.site.register(Credentials)
admin.site.register(BlacklistToken)