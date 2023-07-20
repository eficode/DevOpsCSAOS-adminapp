*** Settings ***

Resource  resource.robot
Resource  resource_login.robot
Resource  resource_create_survey.robot
Resource  resource_delete_question.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Delete An Existing Question
    Go To Backdoor Login Page
    Login With Correct Credentials
    Go To Home Page
    Go To Survey  1
    Click Delete Question  9
    Go To Survey  1
    Wait Until Page Does Not Contain  Game of Thrones