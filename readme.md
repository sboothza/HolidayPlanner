## Project
### Plan

Create models for database 
- customer: basic customer info
- city: locations with gps coordinates
- schedule: the schedule the customer will create, the trip they intend to take
- stop: each location they stop off on the way, along with dates

- Create basic crud views for the database.  
- Create custom view for weather information.  
  - This should take the schedule_id
  - collect the gps and date data
  - pass it to the 3rd party service to get weather info
  - collate it and return

### Issues
- Had problems with the custom view - couldn't get the serializer to work correctly, so had to do a workaround
- Had issues deploying to docker - the app runs ok on my local machine, but seems to have namespace issues on deployment.  Regardless of what I tried, it didn't work properly in docker.

### Result
- I have included the docker files, and the source code.  There is also a screenshot of the app working on local.
- I took slightly longer than 3 hours, struggling with docker.

### Limitations
- Very little error checking
- The custom view needs work
- The docker image doesn't run as is

### Commands to Create Docker Image
docker build -t holidayplanner .  
docker create --name holidayplanner --hostname holidayplanner -p 8000:8000 holidayplanner  
docker start holidayplanner  
docker exec -it holidayplanner bash  
. /HolidayPlanner/venv/bin/activate  