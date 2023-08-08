*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***
Home Page Should Be Open
    Title Should Be  Super Admin 3000

User Logged In With Correct Credentials
    Go To Backdoor Login Page
    Login With Correct Credentials
    Wait Until Page Contains  Logged in
    Wait Until Page Contains  rudolf

Logged In User Can See Surveys On Home Page
    Go To Home Page
    Wait Until Page Contains Element  xpath://div[@id="survey-1"]
    Wait Until Page Contains  How well are you doing Agile?

Logged Out User Should Be On Login Page
    Logout
    Go To Home Page
    Wait Until Page Contains  Please login with your Google account:

Logged Out User Trying To Create Surveys Is Redirected To Login And Displayed Notification
    Go To Create New Survey Page
    Wait Until Page Contains  Please login with your Google account:
    Notification Is Displayed

