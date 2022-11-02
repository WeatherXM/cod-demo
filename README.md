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
3. the paths of the `INPUT_DIR` and `OUTPUT_DIR` directories

Then by running
`bacalhau docker run -v ${CID}:/inputs ${IMAGE} python -- QoF.py ${INPUT_DIR} ${OUTOUT_DIR}`
your workload will be submitted for execution to the network. An example would be:
```
bacalhau docker run -v QmVc7o6daLsVoQYUoFmp3rkD8XXD9pXnmsbgyTWmB89w3h:/inputs ghcr.io/weatherxm/cod-demo:latest python -- QoF.py /inputs/ws_lisbon /outputs
```

To take advantage of the sharding capabilities you can use a glob pattern instead of a specific path as `INPUT_DIR`, for example
```
bacalhau docker run -v QmVc7o6daLsVoQYUoFmp3rkD8XXD9pXnmsbgyTWmB89w3h:/inputs --sharding-base-path "/inputs" --sharding-glob-pattern "ws_*" --sharding-batch-size 1 ghcr.io/weatherxm/cod-demo:latest python -- QoF.py /inputs/ws_* /outputs
```

## Developing  

If you want to experiment with the datasets but want to alter the code, all you have to do is to provide your custom image. 
When the code is ready you can build a new image and `TAG` it with 
`docker build -t ${TAG} .`
and later push it to a *public* image repository (eg [docker-hub](https://hub.docker.com/)) 
