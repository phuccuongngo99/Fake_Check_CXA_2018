# Fake_Check_CXA_2018
CXA 24h Hackathon 2018, Team Singularity, Fake_Check 

The heavy computation part (backend) is handled by the server (only successfully tried on local host lol)
Chrome extension is frontend.


***Setup backend***
Clone this repository
- Activate your python environment
- run '''pip install -r requirements.txt''' to install dependencies
- Download 'glove.6B.50d.txt' from https://drive.google.com/file/d/1d3caSYaHXVhDf8rYDrr91e4HBdWnDqcz/view?usp=sharing and place under backend folder
- Download 'model_audit.bin' from https://drive.google.com/file/d/18RM44Rl5_uy5aAHU93jXWXv9PO4tAgAp/view?usp=sharing and place under backend folder
- Now wreck fake news like a pro

***Setup frontend***
- Go to chrome://extensions/
- Turn on 'Developer Mode' in top right hand corner
- Click 'Load unpacked' in top left hand corner
- Choose 'frontend_extension' directory in your pc
You should see extension in Chrome now

***How to run***
(The backend part)
- Open terminal and cd to repository directory
- cd backend
- python app.py

Open Chrome extension and input your fake news. 

Voila!!!
