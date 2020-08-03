from django.contrib import admin
from account.models import Account
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
	list_display 		= ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
	search_fields 		= ('username', 'email', 'first_name', 'last_name')
	readonly_fields 	= ('last_login', 'date_joined')

	filter_horizontal 	= ()
	list_filter 		= ()
	fieldsets			= ()



admin.site.register(Account, AccountAdmin)
