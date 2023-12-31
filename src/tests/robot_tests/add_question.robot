*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_add_question.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Logged In User Can Add a New Question
    Go To Backdoor Login Page
    Login With Correct Credentials
    Go To Survey  1
    Page Should Contain  Add question
    Click Link  Add question
    Page Should Contain  Category weights
    Add New Question  kysymys1  1
    Go To Survey    1
    Page Should Contain  kysymys1

Back Button Opens Correct Survey Page
    Go To Survey  1
    Click Link  Add question
    Click Link  partial link:Back to survey
    Page Should Contain  Devops assessment
    Page Should Contain  Are you doing DevOps right?
    Page Should Contain  DevOps practices and capabilities.

Invalid Category Weights Default to Zeros
    Go To Survey  1
    Click Link  Add question
    Add New Question  kysymys2  abc
    Go To Home Page
    Go To Survey  1
    Page Should Contain  kysymys2
    Edit Question By Table Row  14
    Textfield Should Contain  cat1  0

Empty Category Weights Are Interpreted As Zeros
    Click Element  id:survey-1
    Click Link  Add question
    Add Question With No Weights  kysymys3
    Wait Until Page Contains Element  xpath: //*[contains(text(), "kysymys3")]
