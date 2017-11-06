#!/usr/bin/env python
try:
    # For Python 3+
    from urllib.request import urlopen
except ImportError:
    # For Python 2
    from urllib2 import urlopen

import sys, getopt
import json
import hashlib

def usage():
	print "-p : link to projects.json file\n-u : link /projects/ folder\n-g : group name"

def getJson(url):
    response = urlopen(url)
    data = str(response.read())
    return json.loads(data)

try:
	opts, args = getopt.getopt(sys.argv[1:], ":p:u:g:")
except getopt.GetoptError as err:
	print str(err)
	usage()
	sys.exit(2)

for opt,val in opts:
	if opt in ('-p'):
		projectsJson = val
	elif opt in ('-u'):
		pathToCatalog = val
	elif opt in ('-g'):
		groupName = val
try:
	if projectsJson and pathToCatalog:
		jsonData = getJson(projectsJson)
		print '[+] projects.json ('+projectsJson+') parsed successfully'
except:
	usage()
	sys.exit(2)

projVars = ['projectName','projectStatus', 'projectShortDescription', 'projectDescription', 'projectContacts','projectMembers','projectSlogan', 'projectLogo', 'whoIsNeeded', 'projectTags']
projVarsContacts = ['www','github', 'telegram', 'email', 'twitter']
projVarsMembers = ['github','telegram','email','twitter']
	
pageHeader = '''
<html>
<head>
    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap theme -->
    <link href="css/bootstrap-theme.min.css" rel="stylesheet">
   
    <link href="jumbotron-narrow.css" rel="stylesheet">
</head>
<title>TITLE_HERE</title>
<br><br><br><br>

<div class="container" role="main">
	<div class="page-header" align=right>
	  <small>'''+groupName+'''</small>
	</div>
'''

pageLinks = '''
	<ul class="nav nav-pills nav-justified"">
		<li role="presentation" PROJECTS_IS_ACTIVE><a href="/projects/">projects</a></li>
		<li role="presentation" IDEAS_IS_ACTIVE><a href="/projects/ideas/">ideas</a></li>
		<li role="presentation" SUBMIT_IS_ACTIVE><a href="/projects/submit/">submit</a></li>
		<li role="presentation" ABOUT_IS_ACTIVE><a href="/projects/about">about</a></li>
	</ul>

	<br>
'''

pageFooter = '''
</div>
</body>
</html>
'''	

def htmlEscape(str):
   str = str.replace("&","&amp;")
   str = str.replace("<", "&lt;")
   str = str.replace(">", "&gt;")
   return str

def processProjectJson(pUrl):
	projectData = getJson(pUrl)
	print projectData['projectContacts']
	for pVar in projVars:
		try:
			if pVar == 'projectContacts' or pVar== 'projectMembers':
				projectData[pVar] = projectData[pVar]
			else:
				projectData[pVar] = htmlEscape(projectData[pVar])
		except:
			if pVar == 'projectContacts' or pVar== 'projectMembers':
				projectData[pVar] = []
			else:
				projectData[pVar] = ''
	
	for pVar in projVarsContacts:
		try:
			projectData['projectContacts'][pVar] = projectData['projectContacts'][pVar]
		except:
			projectData['projectContacts'][pVar] = ''

	for pVar in projectData['projectMembers']:
		for vVal in projVarsMembers:
			try:
				projectData['projectMembers'][pVar][vVal] = projectData['projectMembers'][pVar][vVal]
			except:
				projectData['projectMembers'][pVar][vVal] = ''
			
			
	return projectData

def buildProjectsPage(data):
	page = ''
	for i,k in enumerate(data):
		page = page + '''
		<div class="panel panel-default">
			<div class="panel-heading"><b>Project: </b><a href="'''+pathToCatalog+'''/'''+str(k)+'''/" title="View project page">'''+data[k]['projectName']+'''</a></div>

			<table class="table">
				<tr>
					<td width="90%"><b>Description: </b>'''+data[k]['projectShortDescription']+'''</td><td width="10%"><img src="'''+data[k]['projectLogo']+'''" width="55px" height="55px"></img>
				</tr>
				<tr>
					<td><b>Status: </b>'''+data[k]['projectStatus']+'''</td>
				</tr>

				<tr>
					<td><b>Tags: </b>'''+', '.join(data[k]['projectTags'])+'''</td>
				</tr>
			</table>
		</div>	

		'''

	pageHeaderP = pageHeader.replace('TITLE_HERE','projects')
	pageHeaderP = pageHeaderP.replace('PROJECTS_IS_ACTIVE','class="active"')
	pageHeaderP = pageHeaderP.replace('IDEAS_IS_ACTIVE','')
	pageHeaderP = pageHeaderP.replace('SUBMIT_IS_ACTIVE','')
	pageHeaderP = pageHeaderP.replace('ABOUT_IS_ACTIVE','')
	page = pageHeaderP + pageLinks + page + pageFooter
	return page


def buildContacts(contactsData,elemList):
	pContacts = []
	for pContact in elemList:
		if contactsData[pContact] != '':
			if pContact == 'email':
				pContacts.append('<a href="mailto:'+htmlEscape(contactsData[pContact])+'">'+pContact+'</a>')
			elif pContact== 'twitter':
				pContacts.append('<a href="https://twitter.com/'+htmlEscape(contactsData[pContact])+'">'+pContact+'</a>')
			elif pContact== 'github':
				pContacts.append('<a href="https://github.com/'+htmlEscape(contactsData[pContact])+'">'+pContact+'</a>')
			else:
				pContacts.append('<a href="'+htmlEscape(contactsData[pContact])+'">'+pContact+'</a>')
	
	return pContacts
	
def buildProjectPage(id,data):	
	#print id,data

	page = '''
	<div class="panel panel-default">
		<div class="panel-heading"><b>Project: </b><a href="/projects/'''+str(id)+'''">'''+data['projectName']+'''</a><img src="'''+data['projectLogo']+'''" width="25px" height="25px" align="right"></img></div>
		
		<table class="table">
			<tr>
				<td><b>Slogan: </b>'''+data['projectSlogan']+'''</td>
			</tr>
			<tr>
				<td><b>Description: </b>'''+data['projectDescription']+'''</td>
			</tr>
			<tr>
				<td><b>Status: </b>'''+data['projectStatus']+'''</td>
			</tr>

			<tr>
				<td width="70%"><b>Tags: </b>'''+', '.join(data['projectTags'])+'''</td>
			</tr>

		</table>
	</div>
	
	<div class="panel panel-default">
		<div class="panel-heading"><b>Project needs</b></div>
		<table class="table">
	'''

	for i in data['whoIsNeeded']:
		page = page + '''
			<tr>
			   <td><b>'''+i+'''</b> - '''+data['whoIsNeeded'][i]+'''</td>
			</tr>
		
	'''

	page = page + '''
			<tr>
			   <td><b>You</b> - because you are a part of community</td>
			</tr>
		</table>
	
	</div>
	<div class="panel panel-default">	
		<div class="panel-heading"><b>Contacts</b></div>

		<table class="table">
	'''

	pContacts = buildContacts(data['projectContacts'],projVarsContacts)

	if len(pContacts)>0:
		page = page + '<tr><td>Project related: '+' | '.join(pContacts)+'</td></tr>'
	else:
		page = page + '<tr><td>Project related: none</td></tr>'

	
	print projectData['projectMembers']
	for pVar in projectData['projectMembers']:
		print pVar
		pContacts = buildContacts(data['projectMembers'][pVar],projVarsMembers)
		page = page + '<tr><td>'+htmlEscape(pVar)+': '+' | '.join(pContacts)+'</td></tr>'
		
	aaa='''			<tr>
				<td>username: <a href="mailto:username@local.domain">email</a> | <a href="http://twitter.com/username">github</a> | <a href="http://twitter.com/username">telegram</a> | <a href="http://twitter.com/username">twitter</a></td>
			</tr>
			<tr>
				<td>friend: <a href="http://github.com/project">project</a></td>
			</tr>
	'''		
	page = page + '''
		</table>
	</div>	
	'''
	
	pageHeaderP = pageHeader.replace('TITLE_HERE',data['projectName'])
	pageHeaderP = pageHeaderP.replace('PROJECTS_IS_ACTIVE','')
	pageHeaderP = pageHeaderP.replace('IDEAS_IS_ACTIVE','')
	pageHeaderP = pageHeaderP.replace('SUBMIT_IS_ACTIVE','')
	pageHeaderP = pageHeaderP.replace('ABOUT_IS_ACTIVE','')
	page = pageHeaderP + pageLinks + page + pageFooter
	return page
	
	
projectsPage = {}	

print '[+] Processing projects'
for i, k in enumerate(jsonData):
	projectUrl = k
	projectUrl = 'https://ygoltsev.github.io/projects/project.json'
	projectId = jsonData[k][0]
	projectHash = jsonData[k][1]
	print ' | '+str(projectId)+' : '+projectUrl
	projectData = processProjectJson(projectUrl)
	projectPage = buildProjectPage(projectId,projectData)
	#print projectPage
	projectsPage[projectId] = {'projectName' : projectData['projectName'], 'projectStatus' : projectData['projectStatus'], 'projectShortDescription' : projectData['projectShortDescription'], 'projectLogo' : projectData['projectLogo'],'projectTags' : projectData['projectTags']}
	
print '[+] Done'
print '[~] Generating projects index page'
projectsIndexHtml = buildProjectsPage(projectsPage)
#print projectsIndexHtml
print '[+] Done'
