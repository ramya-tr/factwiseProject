from board import router as board_router
from teams import router as team_router
from users import router as user_router


def add_routes(app):
    """
    add app routes
    """
    app.include_router(user_router.router)
    app.include_router(team_router.router)
    app.include_router(board_router.router)
