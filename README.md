# factwise Project using FastAPI 

This is a project for managing project boards and team-user linking using FastAPI.

## Getting Started

### Prerequisites

To run this project, you will need:

- Python 3.7 or later
- [FastAPI](https://fastapi.tiangolo.com/) and its dependencies (can be installed with `pip install fastapi[all]`)
- [uvicorn](https://www.uvicorn.org/) server (can be installed with `pip install uvicorn`)

### Installation

1. Clone the repository and navigate into the project directory:
   ```
   git clone https://github.com/your-username/fastapi-project.git
   cd fastapi-project
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv env
   source env/bin/activate  # for Linux or macOS
   env\Scripts\activate.bat  # for Windows
   ```

3. Install the project dependencies:
   ```
   pip install -r requirements.txt
   ```

### Usage
The application exposes several API endpoints that can be accessed using the appropriate HTTP methods:
The documentation for all the available apis with the request and response formats 
can be found at http://localhost:8000/docs

To run the FastAPI app, use the following command:

```
uvicorn main:app --reload
```

You can then access the endpoints by navigating to `http://localhost:8000` in your web browser or by sending HTTP
requests to the appropriate endpoints using a tool like [Postman](https://www.postman.com/).




## Folder Structure

```
fastapi-project/
├── board/
│   ├── __init__.py
│   └── controller.py
│   └── router.py
│   └── schema.py
├── team/
│   ├── __init__.py
│   └── controller.py
│   └── router.py
│   └── schema.py
├── users/
│   ├── __init__.py
│   └── controller.py
│   └── router.py
│   └── schema.py
├── common/
│   ├── __init__.py
│   ├── router.py
│   ├── user_team_linking.py
├── db/
│   ├── __init__.py
│   ├── 
├── output/
│   ├── __init__.py
│   ├── 
├── __init__.py
├── main.py
├── requirements.txt
└── README.md
```

- `board/`, `teams/`, and `users/` contain endpoint definitions for their respective categories.
- `common/router.py` is where all the api routes are added to the app
- `common/user_team_linking.py` is a common file user to store and retrive the user and team linking, the functions defined in this class are used across modules
- The `db` folder contains all the files created to persist the application data.
- The `output` folder stores the response of the `/board/export_board` api in a .txt file
- `requirements.txt` has all the required packages
- `main.py` is the main entry point of the application.
- `README.md` is this file!

The apis available for each module is defined in the router.py fle in their respective module folders.
The JSON schema for request and response data for each endpoint can be found in the schemas.py file in their respective classes.

The application uses the local file storage for persistence. The data is stored in .json format