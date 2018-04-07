from django.shortcuts import render

# Create your views here.
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from main.models import Employee
from main.models import Unit, Dash_request

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files import File
from django.http import HttpResponseRedirect

import csv
import json
import codecs
import xlrd
from datetime import datetime
from xlrd import xldate_as_tuple

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def hello_world(request):
    return render(request, 'hello_world.html')

def check_in_units(request):
	return render(request, 'checkIn.html')

def units_borrow(request):
	
	if request.method == 'POST' and 'search_box' in request.POST : # If the form is submitted
		search_data = []
		search_query = request.POST.get('search_box', None)		
		search_query = str(search_query)
		print(search_query)
		if search_query !="":
			for u in Unit.objects.all():
				if u["move_in_date"].lower() == search_query.lower() \
							or u["owner"].lower() == search_query.lower() \
							or u["core_team"].lower() == search_query.lower() \
							or u["platform"].lower() == search_query.lower() \
							or u["phase"].lower() == search_query.lower() \
							or u["sku"].lower() == search_query.lower() \
							or u["cat_no"].lower() == search_query.lower() \
							or u["s_n"].lower() == search_query.lower() \
							or u["comment"].lower() == search_query.lower() \
							or u["status"].lower() == search_query.lower():
					r = {}
					r['move_in_date'] = (u["move_in_date"])
					r['owner'] = (u["owner"])
					r['core_team'] = (u["core_team"])
					r['platform'] = (u["platform"])
					r['phase'] = (u["phase"])
					r['sku'] = (u["sku"])
					r['cat_no'] = (u["cat_no"])
					r['s_n'] = (u["s_n"])
					r['comment'] = (u["comment"])
					r['status'] = (u["status"])
					search_data.append(r)
		print(len(search_data))
		search_data = json.dumps(search_data)
		print(search_data)
		request.session['search_data'] = search_data
		return HttpResponseRedirect('/search/result/')
		#url = reverse('')
		#return HttpResponseRedirect('/search/result/',{'search_data': search_data})
		#return render(request,'search_result.html',{'search_data': search_data})
	

	elif request.method == 'POST' and 'borrow_cat' in request.POST:
	   
	   borrow_person = request.POST.get('borrow_person', None)
	   borrow_cat = request.POST.get('borrow_cat', None)
	   borrow_date = request.POST.get('borrow_date', None)
	   borrow_purpose = request.POST.get('borrow_purpose', None)
	   return_status = {'status': ""}

	   if borrow_cat !="":
		   for u in Unit.objects.all():
		   		if u["cat_no"] == borrow_cat:
		   			if u["status"] == "In Pool":
		   				u["status"] = "Borrowed"
		   				existing_unit = u
		   				existing_unit["owner"] = borrow_person
		   				existing_unit["borrow_date"] = borrow_date
		   				existing_unit["borrow_purpose"] = borrow_purpose
		   				print(borrow_person)
		   				existing_unit.save()
		   				return_status = { 'status': "Send Borrow Request Success!!!"}
		   			else:
		   				return_status = {'status': "The Unit has been borrowed!!!"}
		   			break
		   		else:
		   			return_status = {'status': "The Unit cannot be found!!!"}
	   #print(borrow_cat)
	   #print(return_status)	
	   return_status = json.dumps(return_status)
	   if not request.POST._mutable:
   			request.POST._mutable = True
	   del request.POST['borrow_person']
	   del request.POST['borrow_cat']
	   del request.POST['borrow_date']
	   del request.POST['borrow_purpose']
	   #print(request.POST)
	   return render(request,'borrow.html',{'return_status': return_status})
	return render(request,'borrow.html')

def search_results(request):
	search_data = []
	if request.session.has_key('search_data'):
		search_data = request.session.get('search_data')
		del request.session['search_data']
	return render(request,'search_result.html',{'search_data': search_data})

def units_list(request):
	if request.method == 'POST' and 'borrow_cat' in request.POST :   
	   print(request.POST.get('borrow_cat'))
	   existing_unit = Unit.objects(cat_no= request.POST.get('borrow_cat'))[0]
	   existing_unit["status"] = "Borrowed"
	   existing_unit["owner"] = request.POST.get('borrow_person')
	   existing_unit["borrow_date"] = request.POST.get('borrow_date')
	   existing_unit["borrow_purpose"] = request.POST.get('borrow_purpose')	   
	   existing_unit.save()
	elif request.method == 'POST' and 'return_no' in request.POST :
	   print(request.POST.get('return_no')) 
	   existing_unit = Unit.objects(cat_no= request.POST.get('return_no'))[0]
	   existing_unit["status"] = "In Pool"
	   existing_unit["owner"] = "TDC"
	   existing_unit["borrow_date"] = ""
	   existing_unit["borrow_purpose"] = ""   
	   existing_unit.save()

	data=[]
	for u in Unit.objects.all():
		r = {}
		r['move_in_date'] = (u["move_in_date"])
		r['owner'] = (u["owner"])
		r['core_team'] = (u["core_team"])
		r['platform'] = (u["platform"])
		r['phase'] = (u["phase"])
		r['sku'] = (u["sku"])
		r['cat_no'] = (u["cat_no"])
		r['s_n'] = (u["s_n"])
		r['comment'] = (u["comment"])
		r['status'] = (u["status"])
		r['borrow_date'] = (u["borrow_date"])
		r['borrow_purpose'] = (u["borrow_purpose"])
		data.append(r)
	data = json.dumps(data)
	#print(data)
	return render(request, 'units_list.html',{'list_data':data})

class myView(View):
    def post(self,request):
        csvfile = request.FILES['csv_file']
        workbook = xlrd.open_workbook(file_contents=csvfile.read())
        #csvfile = csvfile.read().decode('utf-8')
        sheet = workbook.sheet_by_index(0)
        offset = 1
        data = []
        for i, row in enumerate(range(sheet.nrows)):
        	if i <= offset:
        		continue
        	r = []
        	for j, col in enumerate(range(sheet.ncols)):
        		cell = sheet.cell_value(i, j)
        		# move_in_date
        		if j == 0 and cell !='':
        			date = datetime(*xldate_as_tuple(cell,0))
        			cell = date.strftime('%Y/%m/%d')
        		r.append(cell)
        	data.append(r)

        print(len(data))
        print((data[30]))
        print(type(data[30][0]))

        for each_row in range(len(data)):
        	new_unit = Unit( move_in_date = str(data[each_row][0]),
        					 	owner = str(data[each_row][1]),
        					 	core_team = str(data[each_row][2]),
        					 	platform = str(data[each_row][3]),
        					 	phase = str(data[each_row][4]),
        					 	sku = str(data[each_row][5]),
        					 	cat_no = str(data[each_row][6]),
        					 	s_n = str(data[each_row][7]),
        					 	comment = str(data[each_row][8]),
        						status = "In Pool",
        						borrow_date = "",
        						borrow_purpose ="",
        					)
        	if (len(Unit.objects(cat_no= str(data[each_row][6]))) == 0):
        		new_unit.save()

        
        return HttpResponseRedirect('/index/')

def send_mail_via_com():
	info = ''
	info += ('\n'+u'how are you'+'\n')
	
	 

	gmail_user = 'erica.huang@hp.com'
	gmail_pwd = '@wtf09830927'

	smtpserver = smtplib.SMTP('smtp-mail.outlook.com', 587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo()

	smtpserver.login(gmail_user, gmail_pwd)
	 

	fromaddr = "erica.huang@hp.com"

	toaddrs = ['fantastic0516@gmail.com', 'erica.huang@hp.com']
	 

	msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n" % (fromaddr, ", ".join(toaddrs), u'*********for test'))
	 
	smtpserver.sendmail(fromaddr, toaddrs, msg+info)
	 

	smtpserver.quit()
	print("send email")

def send_email(request):
	if request.method == 'POST':
		send_mail_via_com()
	return render(request, 'send_email.html')

def b_d_request(request):
	if request.method == 'POST' and 'fill_in_datetime' in request.POST:
	   
	   fill_in_datetime = request.POST.get('fill_in_datetime', None)
	   applicant_email = request.POST.get('applicant_email', None)
	   department = request.POST.get('department', None)
	   project_name = request.POST.get('project_name', None)
	   phase = request.POST.get('phase', None)
	   bios_version = request.POST.get('bios_version', None)
	   OS = request.POST.get('OS', None)
	   language = request.POST.get('language', None)
	   issue = request.POST.get('issue', None)
	   return_status = {'status': ""}
	   
	   new_dash_request = Dash_request(
	   							pick_up = "X",
	   							status = "Not YET",
	   							fill_in_datetime = fill_in_datetime,
        					 	applicant_email = applicant_email,
        					 	department = department,
        					 	project_name = project_name,
        					 	phase = phase,
        					 	bios_version = bios_version,
        					 	os = OS,
        					 	language = language,
        					 	issue = issue,
        					)
	   if(len(Dash_request.objects(fill_in_datetime= str(fill_in_datetime))) == 0):
   			new_dash_request.save()
	   
	   return_status = json.dumps(return_status)
	   if not request.POST._mutable:
   			request.POST._mutable = True
	   #del request.POST['borrow_person']
	   #del request.POST['borrow_cat']
	   #del request.POST['borrow_date']
	   #del request.POST['borrow_purpose']
	   #print(request.POST)
	   return render(request,'b_d_request.html',{'return_status': return_status})
	return render(request,'b_d_request.html')

def b_d_request_list(request):
	if request.method == 'POST' :
		print(request.POST.get('fill_in_datetime'))
		existing_request = Dash_request.objects(fill_in_datetime= request.POST.get('fill_in_datetime'))[0]
		#print(existing_request[0]["status"])
		existing_request["status"] = "Completed"
		existing_request.save()

	data = []
	for u in Dash_request.objects.all():
		r = {}
		r['pick_up'] = (u["pick_up"])
		r['status'] = (u["status"])
		r['fill_in_datetime'] = (u["fill_in_datetime"])
		r['applicant_email'] = (u["applicant_email"])
		r['department'] = (u["department"])
		r['project_name'] = (u["project_name"])
		r['phase'] = (u["phase"])
		r['bios_version'] = (u["bios_version"])
		r['os'] = (u["os"])
		r['language'] = (u["language"])
		r['issue'] = (u["issue"])
		data.append(r)
	data = json.dumps(data)

	return render(request, 'b_d_request_list.html',{'list_data':data})
