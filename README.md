## This is a test POC of a custom trained Personal AI for dog owners call PetAI.

You can chat with the AI assistant about your dog needs, behaviours, care, grooming and breeds.

This is a recommended app for new and old dog owners

Live Android app to be out soon.

Right now you can clone with

` git clone {this_repo}`

Then run with

`python app.py`

Once you run it successfully go to your browser and search

`http://127.0.0.1:7860`

The enter your search text in the search input box and wait for a response

It has a data scrapper extension to add more context data to the training material

Requirements:

- OPEN AI Secret
- Redis

New Features:

- Add auth to the app
- Flesh it out as a fully function api call
- Personalize with user session and id after auth
- Increase data soure material
- Speed up response time (average is 25s)
