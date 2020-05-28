from django.shortcuts import render
from pyad import *
import pythoncom 
class ADUser:
	def __init__(self,Name,SammAccountName,created):
		self.name=Name
		self.SamAccountName=SammAccountName
		self.created=created


def home(request):
	return render(request,'AD/home.html')

def getDomain(dc):
	domain_lst=dc.split(".")
	domain_str=""
	for i in domain_lst[1::]:
		domain_str=domain_str+" , dc="+i
	return domain_str


def listusers(request):
	AD_Users=[]
	DC=request.POST.get('DC')
	username=request.POST.get('username')
	password=request.POST.get('password')
	domain_str=getDomain(DC)
	pyad.set_defaults(ldap_server=DC, username=username, password=password)
	try:
		pythoncom.CoInitialize()
		ou=pyad.adcontainer.ADContainer.from_dn("cn=Users"+domain_str)
		pythoncom.CoUninitialize()
		for obj in ou.get_children():
			#print(obj)
			if(type(obj)==pyad.aduser.ADUser):
				samaccountname=obj.get_attribute("samaccountname")
				name=obj.get_attribute("name")
				print(name)
				created=obj.get_attribute("whenCreated")[0]
				AUser=ADUser(name,samaccountname,created)
				AD_Users.append(AUser)
		#print("Length:"+str(AD_Users.length()))
		
		return render(request,'AD/listusers.html',{"DC":DC,"ADUsers":AD_Users})
	except:	
		return render(request,'AD/error_connect.html')
# Create your views here.
