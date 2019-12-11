Steps to deploy the app in Docker container with sample data of 1k documents:
1. Run the following command in the src folder
```bash
	docker-compose up --build
```
2. Wait until the two containers (searchengine and mongodb) are up
3. Go to http://localhost:5000/build and wait until you get a response from the server.
4. Finally, go to http://localhost:5000/ and now you can use the search engine.

The detailed project design decisions are on file Project - Carlos Segura.pdf in the root of the project.

All of our dev stack relies on python for the front-end and back-end in all areas from Text Processing to UI. These are the technologies we use:

* Python 3.7: Our programming language of choice.
* Python Multiprocessing: We used this type of programming to create the inverted index faster.
* Pickles file Manager: We needed this technology in the batch processing of index creation.
* Pandas Dataframes: We used it for the Query Suggestion operations.
* MongoDB: A fast and reliable document storage.
* Flask: A simple and fast web framework.
* Jquery: A javascript library used for DOM manipulations and ajax calls to the server.


We use python virtual environment for development and pip for dependency management. We recommend to use that for development.

To start the web app just execute: python3 app.py
