import json
import urllib
import urllib2
import sched, time
from subprocess import call


trafficLightColour = ""

# server List
serverNameList = ['EU', 'EU1', 'NA1', 'NA2', 'DEMO', 'Customer Service', 'Headquarter']
serverIdList = {'EU': 6, 'EU1': 7, 'NA1':1, 'NA2':2, 'DEMO':4, 'Customer Service':8, 'Headquarter':9}
servers = []


####### SERVER Class #######
class Server:

	#trafficLightColour = ""

	def __init__(self, name, serverId):
		self.name = name
		self.serverId = serverId
		self.colour = None
		self.id = None

####### END CLASS SERVER #######



# Instantiate each server object
def createServersObject():
	for num in range(0,len(serverNameList)):
		serverName = serverNameList[num]
		servers.append(Server(serverNameList[num], serverIdList[serverName])) 

#Instantiate server object
createServersObject();





#######******************************************########

# Entire method that check and set the Colour of Traffic light
def runFullCheck():

	# Create a JsonObject based on URL provided
	def createJson (urlParam):
		baseUrl = "https://trust.docusign.com/events-api/v1/"
		req = urllib2.Request(baseUrl+ urlParam)
		response = urllib2.urlopen(req)
		json_object = json.load(response)
		return json_object




	# Collect ids of all open events
	def collecOpenEventIds():
		allIds = []
		for event in allEvents:
			if event["end"] == None:
				allIds.append(event["id"])
		return allIds




	# Set Each server its colour and Event ID
	def setServerColour():
		for event in reversed(allOpenEventIds):
			openEvent = createJson("event/" + str(event) + "?format=json")
			sName =  openEvent["event_state_changes"][len(openEvent["event_state_changes"])-1]["environment"]["name"]
			for server in servers:
				if server.name ==  sName:
					server.colour = openEvent["event_state_changes"][len(openEvent["event_state_changes"])-1]["severity"]["code"]
					server.id = openEvent["id"]






	# Set Traffic light its colour
	def setTrafficLightcolour():
		tColour = "GRN"
		for server in servers:
			#print(server.name + " " + server.colour)
			if server.colour == "YLLW":
				if tColour != "RED":
					tColour = "YLLW"
			elif server.colour == "RED":
				tColour = "RED"
				#Means the server color is GRN
		return tColour



	allEvents = createJson("events/?format=json")
	allOpenEventIds = collecOpenEventIds()
	setServerColour()
	trafficLightColour = setTrafficLightcolour()

	return trafficLightColour

#######******************************************########


# Scheduled task every 60 - runFullCheck() and output the colour to traffic light
s = sched.scheduler(time.time, time.sleep)

def scheduledCheck(sc): 
	statusColour = runFullCheck()
	print(statusColour)
	try:
		if(statusColour == "GRN"):
			call(["light-control", "GRN","on"])
			call(["light-control", "YLLW","off"])
			call(["light-control", "RED","off"])
		elif(statusColour == "YLLW"):
			call(["light-control", "GRN","off"])
			call(["light-control", "YLLW","on"])
			call(["light-control", "RED","off"])
		elif(statusColour == "RED"):
			call(["light-control", "GRN","off"])
			call(["light-control", "YLLW","off"])
			call(["light-control", "RED","off"])
	except:
		print("something wrong happen while switch a light")
	sc.enter(60, 1, scheduledCheck, (sc,))

s.enter(60, 1, scheduledCheck, (s,))
s.run()




#################################
