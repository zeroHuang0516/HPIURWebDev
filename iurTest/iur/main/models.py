from mongoengine import *
from django.db import models

class Employee(Document):
    name = StringField(max_length=50)
    age = IntField(required=False)

class Unit(Document):
	move_in_date = StringField(max_length=50)
	owner = StringField(max_length=50)
	core_team = StringField(max_length=50)
	platform = StringField(max_length=50)
	phase = StringField(max_length=30)
	sku = StringField(max_length=30)
	cat_no = StringField(max_length=30)
	s_n = StringField(max_length=50)
	comment = StringField(max_length=50)
	status = StringField(max_length=50)
	borrow_date = StringField(max_length=50)
	borrow_purpose = StringField(max_length=50)

class Dash_request(Document):
	status = StringField(max_length=30)
	fill_in_datetime = StringField(max_length=50)
	press_send_btn_time = StringField(max_length=50)
	applicant_email = StringField(max_length=100)
	department = StringField(max_length=50)
	project_name = StringField(max_length=50)
	requirement = StringField(max_length=50)
	phase = StringField(max_length=30)
	bios_version = StringField(max_length=30)
	os = StringField(max_length=50)
	language = StringField(max_length=50)
	use = StringField(max_length=100)
	password = StringField(max_length=50)
	issue = StringField(max_length=50)

class UserInfo(Document):
	username = StringField(max_length=30)
	password = StringField(max_length=30)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    photo = models.URLField(blank=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)