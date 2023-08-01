*** Keywords ***

Set Result Text
    [Arguments]  ${text}
    Input Text  text  ${text}

Set Result Cutoff
    [Arguments]  ${value}
    Input Text  cutoff  ${value}

Save Result
    Click Button  xpath: //*[contains(text(), "Save changes")]
    Sleep  2s

Expand Result Card
    [Arguments]  ${result_index}
    Wait Until Page Contains Element    id:expandable-result-${result_index}
    Click Element  id:expandable-result-${result_index}

Edit Result
    [Arguments]  ${result}  ${cutoff}  ${id}
    Input Text  result-${id}  ${result}  clear=True
    Input Text  cutoff-${id}  ${cutoff}  clear=True
    Save Result
    