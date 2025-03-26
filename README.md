# Environmental_Monitoring_Station
This project creates a virtual environmental monitoring station. It simulates data for  temperature, humidity and CO2 levels. The generated data is then published to AWS IoT via the MQTT protocol.
I have used python to simulate 3 sensors - temperature, humidity and CO2 levels.
I have used paho python library using which I connected to AWS
I first tested if the code was running and generating data as expected on my computer.
I have then started connecting to AWS via MQTT protocol.
I then created a thing, a policy and generated certificates on AWS.
As the code was running on my computer, the data was being transmitted via MQTT protocol and I was able to see it on AWS.


The setup is simple. Install the paho library. Place the required certificates and keys in the same directory as the main python file. Make note of your AWS endpoint and use it in the code. Then run the python file. 

In AWS,  I created a policy. In the policy I selected the options for connecting, publishing and subscribing. Next I created a thing and attached it to the policy I have created.

Subscribe to the topic on AWS and you can monitor live sensor readings.
