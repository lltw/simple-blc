# Simple Benford's Law Checker

This is a simple web application consisted of python server (Flask) and Vue client for checking if the numbers in specified column in user submitted file are following the Benford's Law.

# Current state

This is a second draft - currently I'm adding Vue client to it.

## Getting Started

Prerequisites: docker-compose (to run docker-compose.yml) and npm (to run vue client)

In order to tun the app you need to, clone the repository, run the following command from the top directory of cloned repository:

```
docker-compose up -d
docker-compode logs -f
```

Then open a new terminal and navigate to client directory to run Vue client:

```
cd client
npm run serve
```

You can now open http://127.0.0.1:8080/ in your browser, to see the page. If you open http://127.0.0.1:5000/ you'll see the old page, still being rendered by the python server.
