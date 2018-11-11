### Video Recommender Service for LoL

Consists of:

1. HTTP service of add/update/delete data about users and videos into DB with address:

    http://data-science-morelegends.westus2.cloudapp.azure.com:7003 with routes
    
    ```python
    app = Application([
            (r'/api/users',      UserHandler),
            (r'/api/users/\d+',  UserHandler),
            (r'/api/videos',     VideoHandler),
            (r'/api/videos/\d+', VideoHandler),
            (r'/api/event',      EventHandler),
        ])
    ```    

2. Service of DB is based on PostgreSQL

3. HTTP service of backend request for making video recommendations with address:

    http://data-science-morelegends.westus2.cloudapp.azure.com:7004 with routes
    
    ```python
    app = Application([
            (r'/api/videos/recommendations', RecommenderHandler),
        ])
    ```    
    
    Request for video recommendation can be one of two forms:
    * ```/api/videos/recommendations?locale=en&user_id=1``` for usual users
    * ```/api/videos/recommendations?locale=ru"``` for anonymous users

4. Service of video recommendation is based on algorithm [SVD](https://surprise.readthedocs.io/en/stable/matrix_factorization.html#surprise.prediction_algorithms.matrix_factorization.SVD)
from python library [surprise](https://surprise.readthedocs.io/en/stable/index.html)


#### Manage ```bash``` scripts
* ```start_services.sh``` starts all (four) services above
* ```kill_services.sh``` kills all available (working) services above
* ```restart_services.sh```is a serial applying of two scripts above for start and kill

All services (both HTTP services and both service processes) after starting write their PID into:

* ```pid_db_service.json```
* ```pid_recommend_service.json```

#### Logging
Logs are store in files:
* ```db_service.log```
* ```recommend_service.log```


