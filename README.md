# Gridlock

## Gridlock is a service status dashboard

Gridlock was built with the idea that the same service is deployed in many sites. I specifically wrote it to display the status' of Openstack apis across many installations. I use sensu to monitor the apis and services and the same script pushes a status update to Gridlock. Why the two systems you ask? Well, as much as I like sensu, I find the interface can get cluttered when you have all the operating system checks, network checks etc. So, I wanted a simple and very visual dashboard.

Each square on the main page displays the last known state for each service in each location. Each square is clickable for a historical view of the service. By default it shows the last 20 reports. To get more, append &offset=100 to the url.

Gridlock does no polling itself, it expects the data to be sent to it. I've included a bash and python script as examples.
Currently it uses an sqlalchemy/sqlite3 db but should be easy to use any database via sqlalchemy.

My python foo is not strong, please look at this as more of intent than a polished, safe, secure piece of code.
Forks and pull requests are most welcome!

![Alt text](/screenshots/ss1.png?raw=true "Overview Page")
![Alt text](/screenshots/ss2.png?raw=true "Detail Page")


Color legend is simple:
```
Green   -   up (status 0)
Yellow  -   warn (status 1)
Red     -   down (status 2)
Black   -   no data or unknown (status 3)
Grey    -   timeout (a service has not reported in for 10 minutes) (status 4)
```

### Inputs 
When sending data to the api, it expects the following fields in json format
```
{ "description": "",
  "service":"",
  "status":"",
  "location":"",
  "env":"",
  "timestamp":""
}
```
#### Description
A description of the status, eg execution timing. Will be displayed as a tooltip
#### Service
The service name
#### Status
Must be one of `0|1|2|3`
#### Location
Where the service lives
#### Env
Currently unused, I default to "prod"
#### Timestamp
Epoch time as an int

## Testing
- install flask and SQLAlchemy
- run python app.py to start the app
- browse to localhost:5000 to see the status page
- run scripts/put_to_gridlock.sh to populate test data
- to inspect DB use sqlite3 db/gridlock.db
