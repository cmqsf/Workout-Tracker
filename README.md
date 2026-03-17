# Workout Tracker

### Purpose of the project
The primary goal is to flex some of my backend skills, specifically skills related to building apis and using MongoDB.  
The secondary goal is to continue learning frontend skills, including (hopefully): 
- React
- Forms

### Backend Walkthrough
#### auth
I am fully aware that there are many better ways to create and authenticate a user than to store personal information, including passwords, in a MongoDB database. However, I don't want to pay for anything related to AWS for a small project (I best know how to authenticate using Cognito), and I currently do not want to focus on building a better way to log a user in, especially since I intend to be the only user.
In the future, it is entirely possible that I will play around with sending bearer tokens, possibly using oauth2 or some other method. That is a project for later, however. 

#### data
For now, connecting to Mongo is pretty easy since I'm just connecting to a local server. However, if I were to connect to MongoDB Atlas, I would need to specify a username and password, as well as a more proper connection_string. However, again, I don't want to pay for anything for a small practice project. 
