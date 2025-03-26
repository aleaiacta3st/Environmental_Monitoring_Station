# Environmental_Monitoring_Station
This project creates a virtual environmental monitoring station. It simulates data for  temperature, humidity and CO2 levels. The generated data is then published to AWS IoT via the MQTT protocol.

The setup is simple. Install the paho library. Place the required certificates and keys in the same directory as the main python file. Make note of your AWS endpoint and use it in the code. Then run the python file.

Subscribe to the topic on AWS and you can monitor live sensor readings.
