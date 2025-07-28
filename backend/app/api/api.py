from fastapi import APIRouter
from .endpoints import users, profiles, journals, moods, auth, usage, analysis, cbt, meditation, sounds, pomodoro, admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(users.router, prefix="/users")
api_router.include_router(profiles.router, prefix="/profiles")
api_router.include_router(journals.router, prefix="/journals")
api_router.include_router(moods.router, prefix="/moods")
api_router.include_router(usage.router, prefix="/usage")
api_router.include_router(analysis.router, prefix="/analysis")
api_router.include_router(cbt.router, prefix="/cbt")
api_router.include_router(meditation.router, prefix="/meditation")
api_router.include_router(sounds.router, prefix="/sounds")
api_router.include_router(pomodoro.router, prefix="/pomodoro")
api_router.include_router(admin.router, prefix="/admin") 