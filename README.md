
# Smart Helmet With IOT

#### Enhancing motorcyclist safety and emergency response through smart helmet technology. 

Through out this project our team members are dedicated to build a safety solution for riders who may make contact with death or injuries. We introduce a Smart Helmet that saves riders' life from any accident. This can be considered as an activity which IOT is used for the sake of human lives. 


## The Identified Problem 

Motorcycling, while offering efficiency and convenience, carries significant risks, some times 
concerning accidents.

In a case of severe accident (involving 2nd party or not), the rider may 
become incapacitated, temporarily disabled, unable to call help or sometimes provide critical 
information (such as accurate location) to authorities due to the injuries and shock he had to face.
 
This delay in first responses combined with absolute lack of riders vitals, can significantly 
worsen the situation of rider leading to prolonged suffering, in worst case fatalities and death. 

Current emergency protocols often relies on bystanders or the victim of the accident themselves 
to report the accident, which is really unreliable and completely useless system when the rider is 
unconscious or disoriented. Especially on remote areas while solo riding. The situation is 
much worse when it comes to the time after midnight in many suburban or rural areas, with less 
to non-bystanders in the roadside.
## Proposed Solution

This novel IOT 
powered Smart Helmet will address the problem of communication in motorbike accidents by 
integrating reliable sensors, communication devices and robust protocols with a reliable central 
database and data relaying infrastructure.

## Core Functionalities

- Automatic accident detection:  The proposed helmet/ helmets will continuously monitor for sudden deacceleration, impact, change of angle or combine of them to detect accidents. 
- Distress signal transmitting: When helmet monitors that accident occurred, after a set time period if there is not any override actionperformed, it will send distress information to central database. Central infrastructure will then relay the incident to authorities. 
- Location transmitting: simultaneously to the transmitting distress signal, helmet will transmit the location data, by using the riders mobile GPS/ inbuilt GPRS through mobile phones cellular connection. 
- Vital information collecting and transmitting: After the distress signal transmission, the helmet will collect vital signal using heart rate senser and transmit(heart rate, blood infused O2 level) of rider 
- Transmitting rider details: When the distress signal being sent to emergency services, with it the basic information like riders name, NIC, vehicle number plate, vehicle model and color of vehicle  will be attached and sent. These information will be stored in central database and in case of emergency will be accessed using the special unique identification number given to each helmet. 
- Manual cancelation button: The helmet will be equipped with an manual override button that can be use by rider to cancel any false alarms happens due to mistakes like dropping the helmet accidently while it is active.
- The smart breaklight: When a deacceleration detected by the accellerometer the breaklight which attached to the helmet will turn on.
- Battery charging level monitor: Monitor the battery charging percentage using the output valtage. 


## Project Objectives

The overall objective of this project is to build a ‘smart helmet’ that act as an proactive safety 
system for motorbike riders to reduce emergency response time and increase the response 
accuracy. 

### SMART objectives 

- Build a working prototype of helmet circuitry itself that could transmit the required data by connecting to a network. 
- Testing the data accuracy. 
- Improve data accuracy of sensors. 
- Testing whether helmet can identify a accident and the intensity of an accident. 
- Testing the communication system reliability and robustness. 
- Build a working prototype using a commercially available helmet. 
- Testing the  robustness of the designed package (helmet + electronics) 
- Building a web infrastructure that can handle data transmitted by helmets and relay them to emergency contacts. 
- Testing the web system. 
- Testing the web system combined with helmet.

## Product Overview

As a real world, problem solving IOT project The Smart Helmet Solution consists and operates with five main components.

- Smart Helmet
- Mobile Application
- Web Application
- Back-End
- Database

### Smart Helmet

Based on the NodeMCU(esp8266) module this smart device mainly Transmit data that collected from sensors to the firebase for store and further uses of data. Following sensors are using to gather data through out process, 

![esp8266](https://github.com/user-attachments/assets/4af4ca1f-7f86-4937-851a-b4c007449a5d)


- Accelerometer (mpu6050)  - Sense the speed which bike is going, acceleration, deacceleration, altitude, tilt (angle) when the accident took place.
  
 ![WhatsApp Image 2025-07-04 at 20 36 31_a56eb1d8](https://github.com/user-attachments/assets/92969ae9-32ed-4496-ae27-98510ba2c195)


- GPS Module (neo-6m-0-001) - Transmit the current location when the accident occurred.
![WhatsApp Image 2025-07-04 at 20 37 49_fde36517](https://github.com/user-attachments/assets/5d5cfcc2-86c3-4f3f-a99c-63a48f640e9e)


- Heart rate sensor (gy-max30102) - Monitor rider's heart rate and update the real-time database. Also it can be used to detect whether the rider has worn the helmet or not.
  
![462549598-7706755b-322d-434e-ac2d-7cb76e92e74b](https://github.com/user-attachments/assets/fec5144e-e366-442a-ba9f-98a2c0d6a71c)

The following circuit diagram is a prototype of this smart helmet project. 
![image](https://github.com/user-attachments/assets/ce0018a1-b872-4286-baf5-227704bb7704)


When an accident took place helmet will transfer all necessary data related to the accident to the fire store. Afterward it will continuously transfer heart beat data to the real-time database.  
Arduino IDE and C++ was used to program the esp8266 with sensor's.

### Mobile Application


This is the user-interface which helps users to connect with the smart helmet. With the unique id attached to the helmet user can activate the helmet through the mobile app and access its features. 

![a](https://github.com/user-attachments/assets/85a9eb82-db1f-4e9b-b835-51ee8662d70a)

Withing the login process users can enter their details to their profile which can also update later. This data will be saved in the Fire store and can be fetch in to the web application when needed. 

Android studio and Java with xml were used to create this application.  

### Back-End

This can be identify as the core of this project. It will monitor the fire store for a change with the aid of a thread. If any changes detected (adding a helmet id) from the fire store it will identified as an accident occurred. 

when an accident occurred a link with the access to the web Application is sent via a SMS service to the relevant parties such as 119 and 1990.

Python flask is used to implement the backend

### Web Application

After accessing to the application they can monitor rider details, accident details, heart beat and any vital details. With the help of this web application they can easily track the accident location and recover the injured rider or pedestrian following a vehicular collision. 

![image](https://github.com/user-attachments/assets/fb90070d-56c9-4db1-8dee-63a70ff33957)

React-js is used to create the web application.

### Database

Store all relevant data of the rider, bike and the accident. Firebase is the used database server and two databases are used to store data. 

#### Realtime database

Store Heartbeat in real-time since changes in heartbeat are need to monitor frequently after accident occurred.

#### Fire store

Store static data which does not change frequently.

## Bibliography 

1. Divyasudha N, Arulmozhivarman P, Rajkumar E.R, A. (2019) ‘Analysis of Smart 
helmets and Designing an IoT based smart helmet: A cost effective solution for Riders', 
ICIICT, pp. 1-4. Available at: https://doi.org/10.1109/ICIICT1.2019.8741415  (Accessed: 
25 May 2025). 

2. P Koteswara Rao, P Tarun Sai, N Vinay Kumar, SK Yusuf Vidya Sagar, A. (2020) 
‘Design And Implementation Of Smart Helmet Using IoT’, SSRN, pp. 1-3. Available at:  
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3643615  (Accessed: 27 May 2025).
