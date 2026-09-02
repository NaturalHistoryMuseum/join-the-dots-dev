# Join-the-Dots Web App

This repository is intended for the development of a new Join the Dots (JtD) application. Its purpose is to allow users to input, update, and export collections-level data. The application is a Vue JS frontend served by a Flask Python backend.

## Roadmap

All tasks related to the development of this application can be found on [this planner.](https://github.com/orgs/NaturalHistoryMuseum/projects/43)

## Project Setup

Warning: This repository is set up with the intention of integrating with the NHM's JtD database and does not yet work without a version of this database to connect to.

### Frontend Setup (Vue JS)

Install dependencies

```sh
npm install
```

Compile and Hot-Reload for Development

```sh
npm run dev
```

### Backend Setup (Flask)

Install dependencies

```
cd server
pip install ./
```

Run flask server

```
python -m server.run
```

## Contact

Join-the-Dots - [jointhedots@nhm.ac.uk](mailto:jointhedots@nhm.ac.uk)

Developer - [andrew.roberts@nhm.ac.uk](mailto:andrew.roberts@nhm.ac.uk)
