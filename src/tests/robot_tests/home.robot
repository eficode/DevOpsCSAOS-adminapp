*** Settings ***
Resource  resource.robot
Resource  login_resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***
Home Page Should Be Open
    Title Should Be  Super Admin 3000

User Logged In With Correct Credentials
    Go To Backdoor Login Page
    Login With Correct Credentials
    Page Should Contain  Hello rudolf!

Logged In User Can Edit Questionnaires
    Click Link  Edit existing questionnaire
    Page Should Contain  Here you can eventually edit or delete existing questionnaires

Logged In User Can Create Questionnaires
    Go To Home Page
    Click Link  Create a new questionnaire
    Page Should Contain  Here you can eventually create new questionnaires

Logged Out User Cannot Access Questionnaires
    Logout
    Page Should Not Contain  You are logged in as

Logged Out User Cannot Edit Questionnaires
    Go To Edit Questionnaires Page
    Page Should Contain  Please login 

Logged Out User Cannot Create Questionnaires
    Go To Create New Questionnaire Page
    Page Should Contain  Please login 

*** Keywords ***
Login With Correct Credentials
    Set Username  rudolf
    Set Password  secret
    Submit Credentials