@bdd
Feature: Authentication
  As a user
  I want to authenticate and stay signed in when remember me is enabled
  So that I do not need to log in again on refresh

  @ui @e2e @smoke
  Scenario: Remember me persists after reload
    Given I open the app
    When I log in as "adminA@example.com" with password "Password123!" and remember me true
    Then the remember me cookie max age is about 604800 seconds
    And I should still be logged in after reload
