
https://fastapi.tiangolo.com/#example

Run,

```
uvicorn main:app --reload
```

About the command uvicorn main:app --reload...
The command uvicorn main:app refers to:

main: the file main.py (the Python "module").
app: the object created inside of main.py with the line app = FastAPI().
--reload: make the server restart after code changes. Only do this for development.

```
curl http://127.0.0.1:8000/items/5?q=somequery
```

Interactive API docs¶
Now go to http://127.0.0.1:8000/docs
You will see the automatic interactive API documentation (provided by Swagger UI):

Alternative API docs¶

And now, go to http://127.0.0.1:8000/redoc

You will see the alternative automatic documentation (provided by ReDoc):