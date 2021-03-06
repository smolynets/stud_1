# -*- coding: utf-8 -*-
from django.contrib import admin
from .models.student import Student
from .models.group import Group
from .models.exam import Exam
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

class StudentFormAdmin(ModelForm):
  def clean_student_group(self):
    """Check if student is leader in any group.
    If yes, then ensure it's the same as selected group."""
    # get group where current student is a leader
    groups = Group.objects.filter(leader=self.instance)
    if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
      raise ValidationError(u'Студент є старостою іншої групи.',
      code='invalid')
    return self.cleaned_data['student_group']
class StudentAdmin(admin.ModelAdmin):
  list_display = ['last_name', 'first_name', 'ticket', 'student_group_id']
  list_display_links = ['last_name', 'first_name']
  list_editable = ['student_group_id']
  ordering = ['last_name']
  list_filter = ['student_group_id']
  list_per_page = 10
  search_fields = ['last_name', 'first_name', 'middle_name', 'ticket','notes']
  def view_on_site(self, obj):
    return reverse('students_edit', kwargs={'pk': obj.id})
admin.site.register(Student,StudentAdmin)
admin.site.register(Group)
admin.site.register(Exam)


