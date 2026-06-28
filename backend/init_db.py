from app.main import SessionLocal, GameDB

def init_games():
    db = SessionLocal()
    
    existing_game = db.query(GameDB).filter(GameDB.id == 1).first()
    if not existing_game:
        game_2048 = GameDB(
            id=1,
            name="2048",
            description="经典数字合成游戏，使用方向键移动方块，合成出2048!",
            icon="🔢",
            play_count=12580,
            rating=49
        )
        db.add(game_2048)
        db.commit()
        print("✅ 2048游戏数据已初始化")
    else:
        print("ℹ️ 游戏数据已存在")
    
    db.close()

if __name__ == "__main__":
    init_games()