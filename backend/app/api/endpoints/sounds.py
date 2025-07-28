from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from app.utils.auth import get_current_user
from app.utils.relaxation_sounds import RelaxationSounds
from app.utils.usage_limits import can_use_feature, increment_usage
from app.database.supabase_db import SupabaseDB

router = APIRouter(tags=["sounds"])

# リラックスサウンドシステムの初期化
relaxation_sounds = RelaxationSounds()

@router.get("/")
def get_all_sounds(
    category: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """サウンド一覧を取得"""
    try:
        if category:
            sounds = relaxation_sounds.get_sounds_by_category(category)
        else:
            sounds = relaxation_sounds.get_all_sounds()
        
        return {
            "sounds": sounds,
            "total_count": len(sounds)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"サウンド取得エラー: {str(e)}")

@router.get("/{sound_id}")
def get_sound(
    sound_id: str,
    current_user: dict = Depends(get_current_user)
):
    """特定のサウンド詳細を取得"""
    try:
        sound = relaxation_sounds.get_sound_by_id(sound_id)
        if not sound:
            raise HTTPException(status_code=404, detail="サウンドが見つかりません")
        
        return {"sound": sound}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"サウンド取得エラー: {str(e)}")

@router.get("/categories")
def get_sound_categories():
    """サウンドカテゴリ一覧を取得"""
    try:
        categories = {
            "nature": {
                "name": "自然音",
                "description": "雨、波、森などの自然の音",
                "sounds": relaxation_sounds.get_sounds_by_category("nature")
            },
            "ambient": {
                "name": "環境音",
                "description": "ホワイトノイズ、ピンクノイズなどの環境音",
                "sounds": relaxation_sounds.get_sounds_by_category("ambient")
            },
            "instruments": {
                "name": "楽器音",
                "description": "ピアノ、フルートなどの楽器の音",
                "sounds": relaxation_sounds.get_sounds_by_category("instruments")
            }
        }
        
        return {"categories": categories}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"カテゴリ取得エラー: {str(e)}")

@router.get("/presets")
def get_presets():
    """プリセットサウンドスケープ一覧を取得"""
    try:
        presets = relaxation_sounds.get_presets()
        return {"presets": presets}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"プリセット取得エラー: {str(e)}")

@router.get("/presets/{preset_id}")
def get_preset(
    preset_id: str,
    current_user: dict = Depends(get_current_user)
):
    """特定のプリセット詳細を取得"""
    try:
        preset = relaxation_sounds.get_preset_by_id(preset_id)
        if not preset:
            raise HTTPException(status_code=404, detail="プリセットが見つかりません")
        
        return {"preset": preset}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"プリセット取得エラー: {str(e)}")

@router.post("/create-soundscape")
def create_custom_soundscape(
    sound_ids: List[str],
    volumes: Optional[List[float]] = None,
    current_user: dict = Depends(get_current_user)
):
    """カスタムサウンドスケープを作成"""
    try:
        soundscape = relaxation_sounds.create_custom_soundscape(sound_ids, volumes)
        return {"soundscape": soundscape}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"サウンドスケープ作成エラー: {str(e)}")

@router.get("/recommendations")
def get_recommended_sounds(
    context: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """推奨サウンドを取得"""
    try:
        # ユーザーの最新の気分を取得
        moods = SupabaseDB.get_user_moods(current_user['id'])
        mood_score = moods[0].get("mood", 3) if moods else 3
        
        recommendations = relaxation_sounds.get_recommended_sounds(context, mood_score)
        
        return {
            "recommendations": recommendations,
            "context": context,
            "mood_score": mood_score
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推奨取得エラー: {str(e)}")

@router.post("/favorites")
def save_favorite_soundscape(
    soundscape: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """お気に入りサウンドスケープを保存"""
    try:
        success = relaxation_sounds.save_user_favorite(current_user['id'], soundscape)
        
        if success:
            return {"message": "お気に入りに保存しました", "soundscape": soundscape}
        else:
            raise HTTPException(status_code=500, detail="保存に失敗しました")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存エラー: {str(e)}")

@router.get("/favorites")
def get_user_favorites(current_user: dict = Depends(get_current_user)):
    """ユーザーのお気に入りサウンドスケープを取得"""
    try:
        favorites = relaxation_sounds.get_user_favorites(current_user['id'])
        
        return {
            "favorites": favorites,
            "total_count": len(favorites)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"お気に入り取得エラー: {str(e)}")

@router.post("/play")
def play_sound(
    sound_id: str,
    volume: Optional[float] = 0.5,
    current_user: dict = Depends(get_current_user)
):
    """サウンドを再生"""
    # 使用制限チェック
    if not can_use_feature(current_user['id'], 'sound_play'):
        raise HTTPException(
            status_code=429,
            detail="サウンド再生の使用回数上限に達しました。プレミアムプランへのアップグレードをご検討ください。"
        )
    
    try:
        sound = relaxation_sounds.get_sound_by_id(sound_id)
        if not sound:
            raise HTTPException(status_code=404, detail="サウンドが見つかりません")
        
        # 使用回数を増加
        increment_usage(current_user['id'], 'sound_play')
        
        return {
            "message": "サウンドを再生しました",
            "sound": sound,
            "volume": volume
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"再生エラー: {str(e)}") 