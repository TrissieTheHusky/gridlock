# Gridlock
Gridlock is a service status dashboard

It was built with the idea that the same service is deployed in many sites. I specifically wrote it to display the status' of Openstack apis across many installations. I use sensu to monitor the apis and services and the same script pushes a status update to Gridlock. Why the two systems you ask? Well, as much as I like sensu, I find the interface can get cluttered when you have all the operating system checks, network checks etc. So, I wanted a simple and very visual dashboard.

Gridlock does no polling itself, it expects the data to be sent to it. I've included a bash and python script as examples.
Currently it uses an sqlalchemy/sqlite3 db but should be easy to use any database via sqlalchemy.

My python foo is not strong, please look at this as more of intent than a polished, safe, secure piece of code.
Forks and pull requests are most welcome!

Color legend is simple:
Green   -   up
Yellow  -   warn
Red     -   down
Grey    -   timeout (a service has not reported in for 10 minutes)
Black   -   no data

When sending data to the api, it expects the following fields in json format

{ "description": "",
  "service":"",
  "status":"",
  "location":"",
  "env":"",
  "timestamp":""}

Description : A description of the status, eg execution timing. Will be displayed as a tooltip
Service : The service name
Status : Must be one of "up|down|warn"
Location: Where the service lives
Env: Currently unused, I default to "prod"
Timestamp: Epoch time as an int
