from django.contrib import admin
from .models import Member, ProcedureCost, Claim

admin.site.register(Member)
admin.site.register(ProcedureCost)
admin.site.register(Claim)
