*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Backdoor Login Page

*** Test Cases ***
Backdoor Login Page Should Be Open
    Title Should Be  Backdoor