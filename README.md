# Python library to interact with the MyQ smart home API

Believe it or not there is an undocumented API into the MyQ smart home applications. 

This repo is a python script that you can put into an AWS lambda function.  From there you can enable a trigger from an AWS IOT device and it can open your garage door.  Figured I'd do it for kicks since my kids needed a way to open the door when they got home from school.

I didn't put that much time into this.  I have a liftmaster device so just got that to work.  It should work with liftmaster, chamberlain, craftsman, or merlin. I have all the appid's, just change to suit your needs.

If you want to use it for something else and need some assistance give me a shout and I'll assist getting it to work with anything behind the MyQ smart home.

# How to use

If you have a liftmaster device you may change the following parameters in the code to match your needs and the lambda function should work:

MyQ smart home username: "username"
MyQ smart home password: "Password"

Then under the "lambda_handler" funtion change "GarageDoor" to match whatever your garage door device name is within the MyQ smart home application.
