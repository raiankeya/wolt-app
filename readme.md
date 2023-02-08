# wolt-app-demo
An API that takes JSON-formatted opening/closing hours of a restaurant as an input and outputs hours in a more human readable format.

## Docker-Configuration
  - To run the project from docker, run command - `docker-compose up --build` for the first time
  - For later use only - `docker-compose up`

## Test Runner (after docker-compose up)
  - To check tests - `docker exec  -it wolt-app pytest`
  - To check mypy  - `docker exec  -it wolt-app mypy .` (Intentionally leave few error)
  - To check flake8  - `docker exec  -it wolt-app flake8 .` (Intentionally leave few error)
  - To check black formatting  - `docker exec  -it wolt-app black .`

## Run Project

  - `docker-compose up --build` or `docker-compose up`
    ### Check Status
      - `http://127.0.0.1:5002/`
      - check response
      ```
      {
        "status": "OK"
      }
      ```
    #### API
      - `http://127.0.0.1:5002/api`
      - Use postman or any other client to test the API
      - Resources -
        - Method [POST]
        - `payload` send the json format data
        ```
        {
            "friday":[
                {
                    "type":"open",
                    "value":64800
                }
            ],
            "sunday":[
                {
                    "type":"close",
                    "value":3600
                },
                {
                    "type":"open",
                    "value":32400
                },
                {
                    "type":"close",
                    "value":39600
                },
                {
                    "type":"open",
                    "value":57600
                },
                {
                    "type":"close",
                    "value":82800
                }
            ]
        }```


## Thoughts on Different Data Format

Perhaps if the input data was formatted in a slightly different manner, writing serializers would have been easier.
The payload will look like below -

```
{
  "data": [
    {
        "day": "friday",
        "events": [
          {
            "type": "open",
            "value": 36000
          },
          {
            "type": "close",
            "value": 57600
          },
        ]
    }
  ]
}
```

or another format could be change the type key to open/close and set timestamp value for respective key.

```
{
  "data": [
    {
        "day": "friday",
        "events": [
          {
            "open": "36000",
            "close": 57600
          },
        ]
    }
  ]
}
```
or another format could be, not to mention anything about closing, it could be a range only for opening hour and the rest of hour will mark as closing time by default.

```
{
  "data": [
    {
        "day": "friday",
        "opening_hour": ["36000", "72000"] // 10:00 AM - 20:00 PM
    }
    {
        "day": "saturday",
        "opening_hour": ["36000", "52000", "72000", "86399"] // open 10:00 AM to 14:26 PM, 20:00 PM to 23:59 PM
    }
    {
        "day": "sunday",
        "opening_hour": ["36000"] // 10:00 am to till 23:59 pm as the default closing timestam 86399, if there is no other index.
    },
    {
        "day": "saturday",
        "opening_hour": [] // Closing Day
    }
  ]
}

```
if the opening hour index is able to divisible by 2 then we will assume the day has time range for opening hour, if its not then we can always go for default value for closing the time.
