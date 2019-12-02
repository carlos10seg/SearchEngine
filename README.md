All of our dev stack relies on python for the front-end and back-end in all areas from Text Processing to UI. These are the technologies we use:
	• Python 3.7: Our programming language of choice.
	• Python Multiprocessing: We used this type of programming to create the inverted index faster.
	• Pickles file Manager: We needed this technology in the batch processing of index creation.
	• Pandas Dataframes: We used it for the Query Suggestion operations.
	• MongoDB: A fast and reliable document storage.
	• Flask: A simple and fast web framework.
	• Jquery: A javascript library used for DOM manipulations and ajax calls to the server.

We use python virtual environment for development and pip for dependency management.

To create the db structure just uncomment these lines from tester.py and execute python3 tester.py:
controller = Controller()
controller.build_structure()

To create the query logs file follow these steps: #suggestionManager = SuggestionManager()
print("loading logs")
suggestionManager.load_logs()

To start the web app just execute: python3 app.py