# Remote-Health-Monitoring
An IoT architecture that integrates health sensors, embedded devices, with the lightweight MQTT communication protocol to perform patient health anomaly detection using machine learning and data analytics.

## Architecture
We leverage the Publisher-Subscriber communication paradigm for the project's implementation. It is an event-driven model, where the publisher and subscriber are decoupled from each other and allow for instant updates whenever associated values change.

![project architecture](https://github.com/HassanMahmoodKhan/Remote-Health-Monitoring/assets/97694796/a219ea45-52f1-46c7-8fc4-403aeafbd746)

The architecture supports a Publisher that resides on the Raspberry Pi and a Broker and Subscriber on the Gateway Server. These entities communicate with each other under a constrained environment.

## Message Queuing Telemetry Transport (MQTT)

A light-weight communication protocol that operates in an event-driven fashion. To transfer information MQTT uses proprietary name-based methods called topics. These topics are usually known during the design phase of an application. A subscriber sends a message to inform the broker indicating the topic it is interested in, whereas a publisher sends a message that contains the data along with the topic to be published. If there is a match between the publisher’s and the subscriber’s topics, the broker transfers the message to the subscriber.

## Logistic Regression Classifier

Data received at the Subscriber is appended to a Comma Separated File (CSV), which is then fed to the ML workflow. The model trains on the dataset consisting of sensor readings/features to predict the output i.e., patient's condition, using unseen/test data. We evaluate the model's performance using a number of evaluation metrics.

## AWS S3 Storage

The final output is stored on the Cloud for accessibility and analytics. This information can be used to generate actionable insights and perform additional processing.
