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
	print "-p : link to projects.json file\n-u : link /projects/ folder"

def getJson(url):
    response = urlopen(url)
    data = str(response.read())
    return json.loads(data)


	
try:
	opts, args = getopt.getopt(sys.argv[1:], ":p:u:")
except getopt.GetoptError as err:
	print str(err)
	usage()
	sys.exit(2)

for opt,val in opts:
	if opt in ('-p'):
		projectsJson = val
	elif opt in ('-u'):
		pathToCatalog = val

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
<style> 

#project {
    border-radius: 25px;
	background: white;
    border: 2px solid grey;
    padding: 20px; 
    width: 800px;
    height: HEIGHT_HEREpx;    
}

</style>
</head>
<title>TITLE_HERE</title>
<body bgcolor=white>
<br><br><br><br>

<center>
'''

pageLinks = '''
	<a href="'''+pathToCatalog+'''/">projects</a>
	<a href="'''+pathToCatalog+'''/ideas">ideas</a>
	<a href="'''+pathToCatalog+'''/about">about</a>
'''

pageFooter = '''
</center>
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
		<p id="project">
			<table align="left">
				<tr>
					<td width="70%"><b>Project: </b><a href="'''+pathToCatalog+'''/'''+str(k)+'''/" title="View project page">'''+data[k]['projectName']+'''</a></td><td width="30%"><b>Status: </b>'''+data[k]['projectStatus']+'''</td>
				</tr>
				<tr>
					<td width="70%"><b>Description: </b>'''+data[k]['projectShortDescription']+'''</td><td width="30%"><img src="'''+data[k]['projectLogo']+'''" width="55px" height="55px"></img></td>
				</tr>
				<tr>
					<td width="70%"><b>Tags: </b>'''+', '.join(data[k]['projectTags'])+'''</td>
				</tr>
			</table>
		</p>
		'''
	pageHeaderP = pageHeader.replace('HEIGHT_HERE','100')
	pageHeaderP = pageHeaderP.replace('TITLE_HERE','projects')
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
print '[+] Done'

