@web @smoke

Feature: Netbanking Login



  Scenario: Successful web login

    Given user logs in with username "demo_user" and password "demo_pass"

    When user lands on account summary

    Then dashboard should be visible

