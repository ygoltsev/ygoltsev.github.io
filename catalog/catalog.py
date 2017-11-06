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
		<li role="presentation" class="active"><a href="/projects/">projects</a></li>
		<li role="presentation"><a href="/projects/ideas/">ideas</a></li>
		<li role="presentation"><a href="/projects/submit/">submit</a></li>
		<li role="presentation"><a href="/projects/about">about</a></li>
	</ul>

	<br>
'''

pageFooter = '''
</div>
</body>
</html>
'''	

def processProjectJson(pUrl):
	projectData = getJson(pUrl)
	projVars = ['projectName','projectStatus', 'projectShortDescription', 'projectDescription', 'projectContacts','projectMembers','projectSlogan', 'projectLogo', 'whoIsNeeded', 'projectTags']

	for pVar in projVars:
		try:
			projectData[pVar] = projectData[pVar]
		except:
			projectData[pVar] = ''
	
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
	page = pageHeaderP + pageLinks + page + pageFooter
	return page

	
def buildProjectPage(id,data):	
	print id,data
	
projectsPage = {}	

print '[+] Processing projects'
for i, k in enumerate(jsonData):
	projectUrl = k
	projectUrl = 'https://ygoltsev.github.io/projects/project.json'
	projectId = jsonData[k][0]
	projectHash = jsonData[k][1]
	print ' | '+str(projectId)+' : '+projectUrl
	projectData = processProjectJson(projectUrl)
	buildProjectPage(projectId,projectData)
	projectsPage[projectId] = {'projectName' : projectData['projectName'], 'projectStatus' : projectData['projectStatus'], 'projectShortDescription' : projectData['projectShortDescription'], 'projectLogo' : projectData['projectLogo'],'projectTags' : projectData['projectTags']}
	
print '[+] Done'
print '[~] Generating projects index page'
projectsIndexHtml = buildProjectsPage(projectsPage)
print projectsIndexHtml
print '[+] Done'

