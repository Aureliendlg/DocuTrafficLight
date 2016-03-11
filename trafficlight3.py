import json
import urllib
import urllib2
import sched, time
import RPi.GPIO as GPIO


trafficLightColour = ""

# server List
serverNameList = ['EU', 'EU1', 'NA1', 'NA2', 'DEMO']
serverIdList = {'EU': 6, 'EU1': 7, 'NA1':1, 'NA2':2, 'DEMO':4}
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

# Setup Raspnerry GPIO
def setupGPIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(18, GPIO.OUT)
	GPIO.setup(24, GPIO.OUT)
	GPIO.setup(24, GPIO.OUT)

# GPIO set up 
setupGPIO()


# Scheduled task every 60 - runFullCheck() and output the colour to traffic light
s = sched.scheduler(time.time, time.sleep)

def scheduledCheck(sc): 
	statusColour = runFullCheck()
	print(statusColour)
	try:
		if(statusColour == "GRN"):
			GPIO.output(18, 1)
			GPIO.output(24, 0)
			GPIO.output(25, 0)
		elif(statusColour == "YLLW"):
			GPIO.output(18, 0)
			GPIO.output(24, 1)
			GPIO.output(25, 0)
		elif(statusColour == "RED"):
			GPIO.output(18, 0)
			GPIO.output(24, 0)
			GPIO.output(25, 1)
	except:
		GPIO.cleanup()
	sc.enter(60, 1, scheduledCheck, (sc,))

s.enter(60, 1, scheduledCheck, (s,))
s.run()


#statusColour = runFullCheck()





#################################
#statusColour = runFullCheck()   #
#print(statusColour)             #
#################################





