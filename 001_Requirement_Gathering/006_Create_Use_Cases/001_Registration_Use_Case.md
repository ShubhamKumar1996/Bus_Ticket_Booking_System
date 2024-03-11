# User Registration Use Case

## 1. Brief Description
The purpose of this use case is to register user to the Bus Ticket Booking System.

This use case starts when the user selects to register to the system and ends when system presents a registration successful confirmation.

## 2. Actors
- User
- Bus Operator

## 3. Pre-condition
- None

## 4. Basic Flow
1. User select to register to system.
2. The system presents a registration form.
3. The user provides necessary information such as firstname, lastname, mobile number, email, password.
4. The user submits the registration form.
5. The system validates all fields.
6. The system displays registration successful message and link for login page.

## 5. Alternate/Exception Flows
1. Validation Error:
    - The system detects issue while validating fields
    - The system displays an error.
    - Use case end.
2. Email exists in DB.
    - The system displays email already exists.
    - Use case end.
3. Mobile number exists in DB.
    - The system displays mobile number already exists.
    - Use case end.

## 6. Postcondition
The user will get registered in the application and now can move to the login.
