# DFS graph dispersion with robots

*Authors: Zsohár András, Balázs Bence, Pukánszky Péter*

*Date: 2022.04.28.*

<br>

This project is for the ELTE-IK (MSc) network algorithms course. The essence of the project is to simulate a DFS-based graph dispersion.

<br>

## The engine (back-end)
The algorithm engine is written in [Python](https://www.python.org/) and the web server is provided by the [Flask](https://flask.palletsprojects.com/en/2.1.x/) framework. We used a SQLite-based database to save the simulation results, and the results were visualized using a Jupyter notebook. 

To start the web server, follow these steps:

 - Install the required Python packages in **dispersion-engine** folder with: `pip install -r requirements.txt`
 - Create the `memory.sqlite` database in **dispersion-engine/db** folder and run the following schema creation code from `DDL.txt`
 - Start the web server: `python app.py`

<br>

## The application (front-end)

We used the [Angular](https://angular.io/) framework for the simulation interface, which you can read more about starting and using in the **dispersion-app** folder. We used the [Vis.js](https://visjs.org/) package to create and simulate graphs spectacularly.

To start the application you should create first a `proxy.conf.json` file in the **dispersion-app** folder with the following lines of code: 

`{
    "/api": {
      "target": "LOCAL_IP_ADDRESS_OF_ENGINE",
      "secure": false
    }
}`
