## IntelliSafe: A Safe and Decentrally Connected Future

IntelliSafe solution leverages sensor information from multiple modalities from the smart vehicle and provides driving assistance to its own drivers as well as others. The architecture diagram below highlights our solution in a qualitative sense, where we first obtain a stream from the eCAL to real time and all-weather collision prevention information. And, further we utilize the capabilities of this Pub/Sub architecture to connect other nearby vehicles to provide collision prone behavior related information from other vehicles.

<p align="center">
  <img src="assets/figures/IntelliSafe-conceptual-ideation.svg" width="800" />
</p>
<p align="center">
    <b>IntelliSafe Conceptual Idea</b> 
</p>


## Our Implementation Architecture 

Here, we represent different exact components actually utilized by us for implementing our conceptual ideation. The diagram below highlights the our foundational pillers of keeping the driver "safe" via real time collision prevention alert insights and "decentrally" providing nearby unexpected break behavior information alerts as well.

<p align="center">
  <img src="assets/figures/IntelliSafe-architecture-diagram.svg" width="800" />
</p>
<p align="center">
   <b>IntelliSafe Architecture Diagram</b>
</p>

## Real Time Drive Assist System

In our proposed near real time solution we collect image and speed sensor data from the eCAL and make the road object detection on multiple objects like pedestrians, other cars etc. Further, we incorporate a brake application assist bar as well which raises alert whenever objects appear in front of the car. Additionally, we utilize the speed data from eCAL to dynamically increase the range of the break application area whenever speed increases as highlighted in the below recordings. Here, we observe that the region of brake application increases whenever the car attains higher speed. And, this can help our IntelliSafe tool to preemptively raise at further locations for the in trajectory objects.
 
<p align="center">
  <img src="assets/demonstrations/predicted-speed-test-recording-one.gif" width="400" />
  <img src="assets/demonstrations/predicted-speed-test-recording-two.gif" width="400" />
</p>
<p align="center">
    <b> Speed based increase on the driver assist detector</b>
</p>


## Alert Notification Application

Based on the sequential inputs by multiple publishers, the subscriber with the help of a notifier application generates insightful panic break based alerts. And, we are also directed towards a screen that quantifies the vicinity of the collision when we click on "More Info".


<p align="center">
  <img src="assets/figures/IntelliSafe-alert-app-ui.svg" width="500" />
</p>
<p align="center">
   <b>IntelliSafe Alert Notification Application</b>
</p>
