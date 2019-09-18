# Temperature Application

Test's purpose is to create a Backend service that returns sensor data from the database. Database (iot_db.sqlite) has around 250k rows of sensor data.

We can decide not to continue recruitment process based on this test, so it is recommended that you have good proficiency in the language you choose to use and also show it in this test.

#### To get started

* Unpack provided archive
* Select technology you want to use
  * C, C++, C#, Java, Node.js, PHP, Python, Rust, Scala, Clojure, Go (if you want use something else, ask first)
  * You can use supporting libraries and frameworks
* Create your application

#### Functionality

Service should have these functionalities.

##### Sensor data summary

1. Get data from database table (cubesensors_data) as fast as possible
2. Count amount of data per sensor and average temperature for each sensor
    * Temperatures are stored as hundredths of degrees (e.g. 1234 is 12.34)
3. Return data in JSON format
```json
{
    "sensors" : [
        { "sensorId" : "000A1F0003141E11", "count" : 500, "avgTemp" : 21.4 },
        { "sensorId" : "000B2F0003141E22", "count" : 20, "avgTemp" : 19.7 }
    ]
}
```

##### Temperature difference

1. Get selected sensor's latest temperature
2. Get Helsinki's current temperature from <http://wttr.in/Helsinki>. Temperature is in the first element that ends with ``</span> �C`` e.g. ``<span class="xxxx">-1</span> �C``
3. Calculate the difference of these two values
4. Return data in JSON format
```json
{
    "difference" : 14.56
}
```

#### Architecture and design

1. Implement interface so _htmlapp/index.html_ can get data from the service
    * There should be no need to modify the app
2. Write understandable code
3. Design a good architecture that will support different application scenarios

Other applications that could use this service:

* C++/C#/Java/Go/... client
* Another application that uses this magnificent service's code base
    * Maybe as a Node module, Maven dependency, Class library or whatever it is called in that technology you selected to use

> Important!
>
> Anyone can write (or copy/paste) basic small app, so remember to show your design/architecture skills


### Tips

* You can also comment what you would do
    * Be ready to explain things in the interview
* Testing / mocking etc. Treat this as it would be production code

