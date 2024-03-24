# Registration User Stories
### 1. User Story
#### Registration Happy Flow
As a User, 
I should be able to register to the system
so that I can login to the system.

#### Acceptance Criteria
- Given that user provides all the inputs correctly then the system should display registration successful message with a link to login page.

### 2. User Story:
#### Registration Exception Flow: Validation Error
As a user,
I should be notified when provided firstname, lastname, mobile number, email, password has validation error
so that I can provide different value for specific field and try to register again.

#### Acceptance Criteria
- Given that user has provided firstname, lastname, mobile number, email, password which have validation issues
then the system should display an validation error for the first field that has one.

### 3. User Story:
#### Registration Exception Flow: Email Already Exists
As a user,
I should be notified when provided email already exists in the database
So that I can either provide different email or try login with the existing email.

#### Acceptance Criteria
- Given that user has provided email that is already present in database
then the system should display an "Email Already Exists" error message.

### 4. User Story:
#### Registration Exception Flow: Mobile Number Already Exists
As a user,
I should be notified when provided mobile number already exists in the database
So that I can either provide different mobile number or try login with the existing mobile number.

#### Acceptance Criteria
- Given that user has provided mobile number that is already present in database
then the system should display an "mobile number Already Exists" error message.