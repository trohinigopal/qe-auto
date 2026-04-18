@api @smoke

Feature: Account API



  Scenario: Get account details

    Given api user has valid token

    When user calls account details endpoint

    Then api response should be 200

