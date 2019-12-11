You need the document collection and query logs on data folder at the root of the project.

The Document Collections is in [Wikipedia1.6M](https://drive.google.com/a/u.boisestate.edu/file/d/1M-Ya0Ybnc_4qEJZVIpztAwZvnhMzZAip/view?usp=drive_web)
The Query Log is in [AOL Query Logs](https://drive.google.com/file/d/1G3-aghOhWcBU00ykr_hwvFeHwgOsru-s/view?usp=sharing)

To create the db structure and logs file, just run:
```python
python3 commander.py
```

To start the web app just execute: 
```python
python3 app.py
```

All of our dev stack relies on python for the front-end and back-end in all areas from Text Processing to UI. These are the technologies we use:

* Python 3.7: Our programming language of choice.
* Python Multiprocessing: We used this type of programming to create the inverted index faster.
* Pickles file Manager: We needed this technology in the batch processing of index creation.
* Pandas Dataframes: We used it for the Query Suggestion operations.
* MongoDB: A fast and reliable document storage.
* Flask: A simple and fast web framework.
* Jquery: A javascript library used for DOM manipulations and ajax calls to the server.


We use python virtual environment for development and pip for dependency management. We recommend to use that for development.
