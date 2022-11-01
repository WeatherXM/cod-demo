# cod-demo

Compute on Weather using Compute over Data!

## Prerequisites

- [Docker](https://www.docker.com/get-started/)
- [Bacalhau cli](https://docs.bacalhau.org/getting-started/installation)
- Datasets of weather data from WeatherXM weather stations - both observations and forecasts

## Code

A simple script is provided that caclulates statistical indexes, produces helpful images for the researcher and lastly prints out the results.
It expects exactly two command line arguments:
- the path to the directory with the weather data
- the path to the directory where the images should be stored

## Running 

All you need to do to run the workload on Bacalhau is to provide
1. the `CID` of the folder with your datasets
2. the *public* URI of your `IMAGE`
3. the paths of the ${INPUT_DIR} and ${OUTOUT_DIR} directories

Then by running
`bacalhau docker run -v ${CID}:/inputs ${IMAGE} python -- QoF.py ${INPUT_DIR} ${OUTOUT_DIR}`
your workload will be submitted for execution to the network. An example would be:
`bacalhau docker run -v QmXBfz2h5nTL2EjCvHvDia3y6aAdEcBEBGRTo2sN1yAR8f:/weather ghcr.io/weatherxm/cod-demo:latest python -- QoF.py /weather /outputs`

## Developing  

If you want to experiment with the datasets but want to alter the code, all you have to do is to provide your custom image. 
When the code is ready you can build a new image and `TAG` it with 
`docker build -t ${TAG} .`
and later push it to a *public* image repository (eg [docker-hub](https://hub.docker.com/)) 
