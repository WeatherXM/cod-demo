# cod-demo

Compute on Weather using Compute over Data!

## Prerequisites

- [Docker](https://www.docker.com/get-started/)
- [Bacalhau cli](https://docs.bacalhau.org/getting-started/installation)
- Datasets of weather data from WeatherXM weather stations - both observations and forecasts

## Datasets

The data are expected to be in the following format:
```
{
  epoch: {
    temperature,
    humidity,
    wind_speed
  },
  ...
}
```

for example: 
```
{
  "1640988000000": { "temperature": 11.2, "humidity": 64.7, "wind_speed": 1.23 },
  "1640991600000": { "temperature": 11.2, "humidity": 65.4, "wind_speed": 0.84 },
  "1640995200000": { "temperature": 11.4, "humidity": 66.1, "wind_speed": 1.19 }
}
```

A couple of datasets for demonstration purposes can be found [here](https://ipfs.io/ipfs/QmPvzQ5ciXdEqXsJqiCyewcryqhACxaPTsksugawa8TQrv) 

## Code

A simple script is provided that caclulates the RMSE between the forecasted and actual value of each weather measurement and then prints it out.
It expects exactly two command line arguments:
- the path to the file of observations
- the path to the file of forecasts

## Running 

All you need to do to run the workload on Bacalhau is to provide
1. the `CID` of the folder with your datasets
2. the *public* URI of your `IMAGE`
3. the filenames of the `OBSERVATIONS` and `FORECAST` datasets

Then by running
`bacalhau docker run -v ${CID}:/inputs ${IMAGE} node -- index.js /inputs/${OBSERVATIONS} /inputs/${FORECAST}`
your workload will be submitted for execution to the network. A couple of examples would be:
`bacalhau docker run -v QmPvzQ5ciXdEqXsJqiCyewcryqhACxaPTsksugawa8TQrv:/inputs ghcr.io/chatper/accuracy-tracking:latest node -- index.js /inputs/mall-actual.json /inputs/mall-forecast.json`
`bacalhau docker run -v QmPvzQ5ciXdEqXsJqiCyewcryqhACxaPTsksugawa8TQrv:/inputs ghcr.io/chatper/accuracy-tracking:latest node -- index.js /inputs/ymittos-actual.json /inputs/ymittos-forecast.json`

## Developing  

If you want to experiment with the datasets but want to alter the code, all you have to do is to provide your custom image. 
When the code is ready you can build a new image and `TAG` it with 
`docker build -t ${TAG} .`
and later push it to a *public* image repository (eg [docker-hub](https://hub.docker.com/)) 
