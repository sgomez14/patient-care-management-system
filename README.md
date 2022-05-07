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

> - Login Authentication
> - User Full Name
> - Doctor/Patient Assignments
> - Patient Summary
> - Patient Recent Measurements

## User API Endpoints
### GET /users/authenticate-login/{login_json}
- This is basic plaintext authentication. Production version will utilize proper encryption methods.
- Login json has the following format: {"user_id":20544,"password":"ec544"}


Successful Response


![Image of Login Successful Response JSON](https://user-images.githubusercontent.com/30096097/167271854-6b2bfbc6-79bf-4d60-9c75-82b30f2d1e8a.png)

