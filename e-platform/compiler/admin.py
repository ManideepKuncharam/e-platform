from django.contrib import admin
import nested_admin
from .models import Cquestions,Ctestcases,Pyquestions,Pytestcases

class CtestcasesInline(nested_admin.NestedTabularInline):
	model = Ctestcases

class CquestionsAdmin(nested_admin.NestedModelAdmin):
	inlines = [CtestcasesInline]

admin.site.register(Cquestions,CquestionsAdmin)

class PytestcasesInline(nested_admin.NestedTabularInline):
	model = Pytestcases

class PyquestionsAdmin(nested_admin.NestedModelAdmin):
	inlines = [PytestcasesInline]

admin.site.register(Pyquestions,PyquestionsAdmin)



