from fastapi import APIRouter
from .endpoints import users, profiles, journals, moods, auth, usage, analysis, cbt, meditation, sounds, pomodoro

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(journals.router, prefix="/journals", tags=["journals"])
api_router.include_router(moods.router, prefix="/moods", tags=["moods"])
api_router.include_router(usage.router, prefix="/usage", tags=["usage"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(cbt.router, prefix="/cbt", tags=["cbt"])
api_router.include_router(meditation.router, prefix="/meditation", tags=["meditation"])
api_router.include_router(sounds.router, prefix="/sounds", tags=["sounds"])
api_router.include_router(pomodoro.router, prefix="/pomodoro", tags=["pomodoro"]) 