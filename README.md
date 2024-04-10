# MCBound framework 

This is the offical repository for the MCBound framework. 

## Requirements  

MCBound requires an installed `Python3` version to run the scripts. The version used to develop the project is `Python3.11`. 
For convenience, we provide a `requirements.txt` file listing all the packages needed to run the scripts, which can all be installed at once by running: 

```
pip install -r requirements.txt 
```

## Deployment 

The framework can be deployed to a machine by running the `deoploy_framework.py` script. 
Optionally, it is possible to specify the port on which the service will run with the `-p` arguments, which defaults to `8080`. 

```
python deploy_framework.py -p 8080 
```

In order for MCBound to work, the system needs to support a job data storage (e.g. relational db, non-relational db, distributed file system, etc). A `Python` class able to interact with the job data storage must be created. The class should extend `IDataFetcher` (`service/data_fetcher/data_fetcher.py`). If interested in installing MCBound on your system, we offer assistance in developing this class and deploying the framework. 

For questions and assistance, please contact francesco.antici@unibo.it
