from app.main import SessionLocal, ScoreDB

def init_leaderboard():
    db = SessionLocal()
    
    # 检查是否已有数据
    existing_scores = db.query(ScoreDB).count()
    if existing_scores > 0:
        print(f"[INFO] 排行榜已有 {existing_scores} 条数据，将清空并重新初始化")
        db.query(ScoreDB).delete()
        db.commit()
    
    # 添加虚拟排行榜数据
    leaderboard_data = [
        {"player_name": "游戏达人小明", "score": 89456},
        {"player_name": "手速狂魔", "score": 78234},
        {"player_name": "脑洞大师", "score": 67890},
        {"player_name": "无敌小可爱", "score": 56789},
        {"player_name": "数字天才", "score": 45678},
        {"player_name": "挑战者001", "score": 34567},
        {"player_name": "萌新玩家", "score": 23456},
        {"player_name": "休闲玩家", "score": 12345},
        {"player_name": "游戏新手", "score": 9876},
        {"player_name": "初次挑战", "score": 5432},
    ]
    
    for data in leaderboard_data:
        score = ScoreDB(
            game_id=1,
            player_name=data["player_name"],
            score=data["score"]
        )
        db.add(score)
    
    db.commit()
    print("[OK] 虚拟排行榜数据已初始化 (10条记录)")
    
    # 显示数据
    scores = db.query(ScoreDB).order_by(ScoreDB.score.desc()).all()
    print("\n当前排行榜数据：")
    for i, s in enumerate(scores, 1):
        print(f"{i}. {s.player_name}: {s.score}分")
    
    db.close()

if __name__ == "__main__":
    init_leaderboard()