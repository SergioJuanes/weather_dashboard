# Weather Dashboard

## Project description

https://weather-juanes.herokuapp.com/

## Requirements

You need python3 installed in your machine. 

You need a API key from https://www.weatherapi.com/.

## Installation

Clone this repository in your local machine: 

```
$ git clone git@github.com:SergioJuanes/weather_dashboard.git
```

Navigate into `./weather_dashboard` folder and create a virtual environment:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
```

You can read more about creating and using a virtual environment [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment).


Install the required packages with:

```
$ pip install -r requirements.txt
```

Create a `.env` file with the following variables:

```
WEATHER_API_KEY={YOUR_WEATHER_API_KEY}
```

To run the application just execute the following command:

```
$ python app.py
```
