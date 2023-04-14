# Stephen Project

###
In order to receive the output from systems A,B and C after the celery task is done. There are two approahces to this.
1) Setup django websockets which, once the processing is done, send out a notification to the frontend, notifying the users that the process is complete.

2) We can inside of celery, create a Notification records inside of the DB. The user will see that notification once they refresh or reroute to a new page, which will tell them that the process has been completed.
We will obviously be storing the results of systems A, B and C inside of our DB