@bdd
Feature: Cards
  As a user
  I want to create and move cards between columns
  So that I can track progress

  @ui @e2e @regression
  Scenario: Create a card and move it to another column
    Given I open the app
    And I log in as "adminA@example.com" with password "Password123!" and remember me false
    And I have a board named "Card Board"
    When I open the board
    And I create a card titled "Card One" in column "Todo"
    And I drag the card to column "Doing"
    Then the card should be in column "Doing"
    And the card should remain in column "Doing" after refresh

  @ui @e2e @regression
  Scenario: Card title length validation
    Given I open the app
    And I log in as "adminA@example.com" with password "Password123!" and remember me false
    And I have a board named "Validation Board"
    When I open the board
    And I attempt to create a card with a title over 120 characters
    Then a card title validation error is shown
    And no new card is created in column "Todo"
