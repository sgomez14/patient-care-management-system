# patient-care-management-system
Patient Care Management System Developed for BU EC 530 Software Engineering

# Documentation for Device and Chat Modules
Documentation for the Device and Chat modules is maintained in this repository's [wiki section](https://github.com/sgomez14/patient-care-management-system/wiki).

> [Branching Strategy](https://github.com/sgomez14/patient-care-management-system/wiki/Branching-Strategy) 
>
> [Device Measurement Data Packet Structure](https://github.com/sgomez14/patient-care-management-system/wiki/Device-Measurement-Data-Packet)
>
> [Device Interface API](https://github.com/sgomez14/patient-care-management-system/wiki/Device-Interface-API)
>
> [Chat Module Data Packet Structure](https://github.com/sgomez14/patient-care-management-system/wiki/Chat-Module-Data-Structure)
>
>[Chat Interface API](https://github.com/sgomez14/patient-care-management-system/wiki/Chat-Interface-API)


# Progress Report
Full progress report is located in the [wiki](https://github.com/sgomez14/patient-care-management-system/wiki).


# Documentation for User Module
Documentation for the User module resides on here on the main README.

The User module provide applications access to user related information. Applications can request the following data:

> - [Login Authentication](https://github.com/sgomez14/patient-care-management-system/blob/main/README.md#get-usersauthenticate-loginlogin_json)
> - [User Full Name](https://github.com/sgomez14/patient-care-management-system/blob/main/README.md#get-usersget-user-fullnameuser_id)
> - [Doctor/Patient Assignments](https://github.com/sgomez14/patient-care-management-system/blob/main/README.md#get-usersget-assignmentsuser_id)
> - [Patient Summary]
> - [Patient Recent Measurements]

## User API Endpoints
### `GET` /users/authenticate-login/{login_json}
- This is basic plaintext authentication. Production version will utilize proper encryption methods.
- Login json has the following format: `{"user_id":20544,"password":"ec544"}`


Successful Response


![Image of Login Successful Response JSON](https://user-images.githubusercontent.com/30096097/167271854-6b2bfbc6-79bf-4d60-9c75-82b30f2d1e8a.png)


</br></br>
### `GET` /users/get-user-fullname/{user_id}

Successful Response


![Image of Successful Get User Fullname Response JSON](https://user-images.githubusercontent.com/30096097/167272530-57ea44a8-2ad4-4951-9cde-c1c9a59d3d59.png)


</br></br>
### `GET` /users/get-user-fullname-concatenated/{user_id}

Successful Response


![Image of Successful Get User Fullname Concatenated Response JSON](https://user-images.githubusercontent.com/30096097/167272330-d99582a7-6153-42dc-8a81-2b9d15ed0ed5.png)


</br></br>
### `GET` /users/get-assignments/{user_id}
- The assignments are in an array.

Successful Response


![Image of Successful Get User Assignments Response JSON](https://user-images.githubusercontent.com/30096097/167273306-30b574fc-65df-4ab4-9203-9ee1305b559b.png)


</br></br>
### `GET` /users/get-patient-summary/{user_id}

Successful Response


![Image of Successful Get Patient Summary Response JSON](https://user-images.githubusercontent.com/30096097/167273584-57eeb5ec-9d7c-44f6-99d5-f0c945790be6.png)


</br></br>
### `GET` /users/get-all-recent-measurements/{user_id}

Successful Response


![Image of Successful Get Patient Recent Measurements Response JSON](https://user-images.githubusercontent.com/30096097/167274537-5f2ef0cf-e177-4dc3-903e-2bf1bc846059.png)


# Patient Care Management System Android App

Patients and doctors of the healthcare organization using our Patient Care Management System can interact with each other via a mobile Android app. This mobile app enables patients and doctors to easily see their most recent health data. It also facilitates direct 1-to-1 chat.

## App Start Up

![Image of Patient Care Management System Android App Startup Screen](https://user-images.githubusercontent.com/30096097/167276701-55f32f2e-2eb6-4e93-9c9b-ee88388c56b3.png)



## Login

![Image of Patient Care Management System Android App Login Screen](https://user-images.githubusercontent.com/30096097/167276741-7c56b873-69b1-484c-b04e-eb593e344230.png)


## Assignments 

- On this screen a patient sees all of the doctors assigned to them. If a doctor is using the app, then they will see all of the patients assigned to them.

![Image of Patient Care Management System Android App Assignments Screen](https://user-images.githubusercontent.com/30096097/167276975-69f8b3b0-0f5b-4d55-b217-e363e9788940.png)

