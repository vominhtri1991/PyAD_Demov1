from pyad import *
import dateparser

#import pyad.adquery
class ADUser:
	def __init__(self,Name,SammAccountName,email):
		self.name=Name
		self.SamAccountName=SammAccountName
		self.email=email

def getDomain(dc):
	domain_lst=dc.split(".")
	domain_str=""
	for i in domain_lst[1::]:
		domain_str=domain_str+" , dc="+i
	return domain_str


DC="DC01.vmt.local"
username="Administrator"
password="P@ssword"
domain_str=getDomain(DC)

pyad.set_defaults(ldap_server=DC, username=username, password=password)
#user = pyad.aduser.ADUser.from_cn("u1@vmt.local")
#user1 = pyad.aduser.ADUser.from_dn("cn=u2, cn=Users, dc=vmt, dc=local")
user1 = pyad.aduser.ADUser.from_dn("cn=u2, cn=Users"+domain_str)
#user1 = pyad.aduser.ADUser.from_cn("u2")
print(user1.get_attribute("samaccountname"))
print(user1.get_attribute("name"))
print(user1.get_attribute("userPrincipalName")[0])
print(user1.get_attribute("whencreated")[0])
print(dateparser(user1.get_attribute("whencreated")[0]))
print(user1.get_attribute("AccountExpirationDate"))

ou = pyad.adcontainer.ADContainer.from_dn("cn=Users"+domain_str)
#newuser=pyad.aduser.ADUser.create("user_test",ou,password="123",enable=True,optional_attributes={'displayName':"Nguyen Van A","givenName":"Nguyen Van A","mail":"nguyenvana@gmail.com"})
AD_Users=[]

for obj in ou.get_children():
	#print(type(obj))
	if(type(obj)==pyad.aduser.ADUser):
		#print(obj.get_attribute("samaccountname"))
		#print(obj.get_attribute("userPrincipalName"))
		#print(obj.get_attribute("whencreated"))
		samaccountname=obj.get_attribute("samaccountname")[0]
		name=obj.get_attribute("name")
		email=datetime.datetime(obj.get_attribute("whenCreated"))
		AUser=ADUser(name,samaccountname,email)
		AD_Users.append(AUser)
print(len(AD_Users))