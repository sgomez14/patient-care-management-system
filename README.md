# Patient Care Management System
Patient Care Management System Developed for BU EC 530 Software Engineering



# Documentation for User Module
Documentation for the User module resides on here on the main README.

The Users module provide applications access to user related information. Applications can request the following data:

> - [Login Authentication](https://github.com/sgomez14/patient-care-management-system/blob/main/README.md#get-usersauthenticate-loginlogin_json)
> - [User Full Name](https://github.com/sgomez14/patient-care-management-system/blob/main/README.md#get-usersget-user-fullnameuser_id)
> - [Doctor/Patient Assignments](https://github.com/sgomez14/patient-care-management-system/blob/main/README.md#get-usersget-assignmentsuser_id)
> - [Patient Summary](https://github.com/sgomez14/patient-care-management-system/blob/main/README.md#get-usersget-patient-summaryuser_id)
> - [Patient Recent Measurements](https://github.com/sgomez14/patient-care-management-system/blob/main/README.md#get-usersget-all-recent-measurementsuser_id)


This module also supports a mobile app.
> - [Patient Care Management System Android App](https://github.com/sgomez14/patient-care-management-system/blob/main/README.md#patient-care-management-system-android-app)


## Users Module Architecture

![Image of Users Module Architecture](https://user-images.githubusercontent.com/30096097/167279657-5cb61466-ca8a-483c-88c3-4dd124332543.png)

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




</br></br>
# Patient Care Management System Android App

Patients and doctors of the healthcare organization using our Patient Care Management System can interact with each other via a mobile Android app. This mobile app enables patients and doctors to easily see their most recent health data. It also facilitates direct 1-to-1 chat.


https://user-images.githubusercontent.com/82246325/167280007-faf2e859-b2ab-4997-9804-fc75e4d6bbe1.mp4

## App Start Up

![Image of Patient Care Management System Android App Startup Screen](https://user-images.githubusercontent.com/30096097/167276701-55f32f2e-2eb6-4e93-9c9b-ee88388c56b3.png)



## Login

![Image of Patient Care Management System Android App Login Screen](https://user-images.githubusercontent.com/30096097/167276741-7c56b873-69b1-484c-b04e-eb593e344230.png)


## Assignments 

- On this screen a patient sees all of the doctors assigned to them. If a doctor is using the app, then they will see all of the patients assigned to them.

![Image of Patient Care Management System Android App Assignments Screen](https://user-images.githubusercontent.com/30096097/167276975-69f8b3b0-0f5b-4d55-b217-e363e9788940.png)


## Patient Record

- Clicking on a name on the assignments screen brings the user to the patient's record screen.
- On this screen there is a summary of the patient and a listing of the most recent measurements.
- The most recent measurements section is scrollable.

![Image of Patient Care Management System Android App Patient Record Screen 1](https://user-images.githubusercontent.com/30096097/167277432-7fcbe5e3-967f-49ce-9081-09f38b934cd2.png)


![Image of Patient Care Management System Android App Patient Record Screen 2](https://user-images.githubusercontent.com/30096097/167277451-182bfce9-c94f-45ba-80e6-f08e3f0b0d8f.png)


## Chat 

Patient Sending Chat Message to Doctor


![Image of Patient Care Management System Android App Patient Sending Chat Message to Doctor Screen](https://user-images.githubusercontent.com/30096097/167277644-f6ce7a3c-0d56-4f50-9677-af105f207a98.png)

Doctor Sending Chat Message to Patient


![Image of Patient Care Management System Android App Doctor Sending Chat Message to Patient Screen](https://user-images.githubusercontent.com/30096097/167277652-444896c9-5f2b-4faa-98a5-8e7717567fed.png)





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
