from pytest_bdd import scenario


@scenario("../../features/auth.feature", "Remember me persists after reload")
def test_remember_me():
    pass


@scenario("../../features/boards.feature", "Create rename and archive a board")
def test_board_lifecycle_ui():
    pass


@scenario("../../features/cards.feature", "Create a card and move it to another column")
def test_card_move_ui():
    pass


@scenario("../../features/cards.feature", "Card title length validation")
def test_card_title_validation_ui():
    pass


@scenario("../../features/rbac.feature", "Viewer controls are disabled in the UI")
def test_viewer_controls_ui():
    pass
