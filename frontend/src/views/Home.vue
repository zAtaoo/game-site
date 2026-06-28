<template>
  <div class="home-container">
    <AnimeBackground />

    <header class="header">
      <div class="logo-wrapper">
        <h1 class="logo">
          <span class="logo-icon">🎮</span>
          <span class="logo-text">游戏星球</span>
        </h1>
        <p class="slogan">✨ 释放你的游戏天赋 ✨</p>
      </div>
      <div class="header-stars">
        <span class="star" v-for="i in 5" :key="i">⭐</span>
      </div>
    </header>

    <main class="main-content">
      <section class="games-section">
        <h2 class="section-title">
          <span class="title-icon">🎯</span>
          热门游戏
        </h2>
        <div class="game-grid">
          <div 
            v-for="game in games" 
            :key="game.id"
            class="game-card"
            :style="{ '--card-color': getGameColor(game.id) }"
            @click="navigateToGame(game.id)"
          >
            <div class="card-glow"></div>
            <div class="game-icon">{{ game.icon }}</div>
            <h3 class="game-title">{{ game.name }}</h3>
            <p class="game-desc">{{ game.description }}</p>
            <div class="game-meta">
              <span class="play-count">
                <span class="meta-icon">👾</span>
                {{ formatNumber(game.play_count) }}人在玩
              </span>
              <span class="rating">
                <span class="meta-icon">⭐</span>
                {{ (game.rating / 10).toFixed(1) }}
              </span>
            </div>
            <div class="card-shine"></div>
          </div>
        </div>
      </section>

      <section class="leaderboard-section">
        <h2 class="section-title">
          <span class="title-icon">🏆</span>
          排行榜
          <span class="title-badge">TOP 10</span>
        </h2>
        <div class="leaderboard">
          <div 
            v-for="(item, index) in leaderboard" 
            :key="index"
            class="leaderboard-item"
            :class="{ 'top-three': index < 3 }"
          >
            <div class="rank-badge" :class="'rank-' + (index + 1)">
              <span v-if="index < 3" class="medal">{{ getMedal(index) }}</span>
              <span v-else class="rank-num">{{ index + 1 }}</span>
            </div>
            <div class="player-info">
              <span class="player-avatar">{{ getAvatar(item.player_name) }}</span>
              <span class="player-name">{{ item.player_name }}</span>
            </div>
            <div class="score-info">
              <span class="score-value">{{ formatNumber(item.score) }}</span>
              <span class="score-label">分</span>
            </div>
            <div class="rank-glow" :class="'glow-' + (index + 1)"></div>
          </div>
        </div>
      </section>

      <section class="features-section">
        <h2 class="section-title">
          <span class="title-icon">💫</span>
          为什么选择我们
        </h2>
        <div class="features-grid">
          <div class="feature-card" v-for="feature in features" :key="feature.icon">
            <span class="feature-icon">{{ feature.icon }}</span>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.desc }}</p>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="footer-content">
        <p>🚀 游戏星球 - 让快乐触手可及</p>
        <p class="copyright">© 2026 GameStar | 快乐游戏，健康生活 🎮</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import AnimeBackground from '../components/AnimeBackground.vue'

const router = useRouter()
const games = ref([])
const leaderboard = ref([])

const features = ref([
  { icon: '⚡', title: '即开即玩', desc: '无需下载，随时开黑' },
  { icon: '🎨', title: '精美画质', desc: '高品质视觉体验' },
  { icon: '🏅', title: '排行榜', desc: '全球玩家实时竞技' },
  { icon: '🎁', title: '每日福利', desc: '签到送礼惊喜不断' }
])

const getGameColor = (id) => {
  const colors = ['#FF6B9D', '#C44BE9', '#4ECDC4', '#FF6B6B', '#FFE66D']
  return colors[(id - 1) % colors.length]
}

const getMedal = (index) => {
  return ['🥇', '🥈', '🥉'][index]
}

const getAvatar = (name) => {
  const avatars = ['😎', '🤖', '🦊', '🐱', '🐶', '🦄', '🐼', '🐨', '🦁', '🐯']
  let hash = 0
  for (let i = 0; i < name.length; i++) {
    hash += name.charCodeAt(i)
  }
  return avatars[hash % avatars.length]
}

const formatNumber = (num) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num.toLocaleString()
}

onMounted(async () => {
  try {
    const gamesRes = await axios.get('/api/games')
    games.value = gamesRes.data
    
    const leaderboardRes = await axios.get('/api/leaderboard?limit=10')
    leaderboard.value = leaderboardRes.data
    
    // 如果排行榜为空，添加虚拟数据
    if (leaderboard.value.length === 0) {
      leaderboard.value = getDefaultLeaderboard()
    }
  } catch (error) {
    console.error('Failed to load data:', error)
    games.value = [
      { id: 1, name: '2048', description: '经典数字合成游戏', icon: '🔢', play_count: 12580, rating: 49 }
    ]
    leaderboard.value = getDefaultLeaderboard()
  }
})

const getDefaultLeaderboard = () => {
  return [
    { id: 1, game_id: 1, player_name: '游戏达人小明', score: 89456, created_at: new Date() },
    { id: 2, game_id: 1, player_name: '手速狂魔', score: 78234, created_at: new Date() },
    { id: 3, game_id: 1, player_name: '脑洞大师', score: 67890, created_at: new Date() },
    { id: 4, game_id: 1, player_name: '无敌小可爱', score: 56789, created_at: new Date() },
    { id: 5, game_id: 1, player_name: '数字天才', score: 45678, created_at: new Date() },
    { id: 6, game_id: 1, player_name: '挑战者001', score: 34567, created_at: new Date() },
    { id: 7, game_id: 1, player_name: '萌新玩家', score: 23456, created_at: new Date() },
    { id: 8, game_id: 1, player_name: '休闲玩家', score: 12345, created_at: new Date() },
    { id: 9, game_id: 1, player_name: '游戏新手', score: 9876, created_at: new Date() },
    { id: 10, game_id: 1, player_name: '初次挑战', score: 5432, created_at: new Date() }
  ]
}

const navigateToGame = (gameId) => {
  router.push(`/game/${gameId}`)
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  padding: 20px;
  position: relative;
  overflow-x: hidden;
}

/* Header */
.header {
  text-align: center;
  margin-bottom: 50px;
  position: relative;
  z-index: 1;
}

.logo-wrapper {
  margin-bottom: 20px;
}

.logo {
  font-size: 4rem;
  color: #fff;
  text-shadow: 0 0 30px rgba(255, 255, 255, 0.5),
               0 0 60px rgba(255, 107, 157, 0.3);
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  animation: glow 3s ease-in-out infinite alternate;
}

.logo-icon {
  font-size: 5rem;
  animation: bounce 2s ease-in-out infinite;
}

.logo-text {
  background: linear-gradient(135deg, #fff, #FF6B9D, #C44BE9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@keyframes glow {
  from { text-shadow: 0 0 30px rgba(255, 255, 255, 0.5), 0 0 60px rgba(255, 107, 157, 0.3); }
  to { text-shadow: 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 107, 157, 0.5); }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

.slogan {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 600;
  letter-spacing: 2px;
}

.header-stars {
  margin-top: 15px;
}

.star {
  font-size: 1.5rem;
  margin: 0 5px;
  animation: twinkle 1.5s ease-in-out infinite;
}

.star:nth-child(1) { animation-delay: 0s; }
.star:nth-child(2) { animation-delay: 0.2s; }
.star:nth-child(3) { animation-delay: 0.4s; }
.star:nth-child(4) { animation-delay: 0.6s; }
.star:nth-child(5) { animation-delay: 0.8s; }

@keyframes twinkle {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.section-title {
  color: #fff;
  font-size: 2rem;
  margin-bottom: 30px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.title-icon {
  font-size: 2.5rem;
  animation: wiggle 2s ease-in-out infinite;
}

@keyframes wiggle {
  0%, 100% { transform: rotate(-5deg); }
  50% { transform: rotate(5deg); }
}

.title-badge {
  background: linear-gradient(135deg, #FFE66D, #FF6B6B);
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: normal;
}

/* Game Cards */
.game-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 60px;
}

.game-card {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
  border-radius: 25px;
  padding: 35px 30px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.game-card:hover {
  transform: translateY(-15px) scale(1.02);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3),
              0 0 40px var(--card-color);
}

.card-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, var(--card-color) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.game-card:hover .card-glow {
  opacity: 0.15;
}

.card-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: left 0.5s ease;
}

.game-card:hover .card-shine {
  left: 100%;
}

.game-icon {
  font-size: 5rem;
  margin-bottom: 20px;
  filter: drop-shadow(0 5px 10px rgba(0, 0, 0, 0.2));
}

.game-title {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 12px;
  font-weight: 700;
}

.game-desc {
  color: #666;
  margin-bottom: 20px;
  font-size: 1rem;
  line-height: 1.6;
}

.game-meta {
  display: flex;
  justify-content: space-between;
  padding-top: 15px;
  border-top: 2px dashed rgba(0, 0, 0, 0.1);
}

.play-count, .rating {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #888;
  font-size: 0.95rem;
  font-weight: 600;
}

.meta-icon {
  font-size: 1.2rem;
}

/* Leaderboard */
.leaderboard-section {
  margin-bottom: 60px;
}

.leaderboard {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
  border-radius: 25px;
  padding: 30px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.leaderboard-item {
  display: flex;
  align-items: center;
  padding: 18px 20px;
  margin-bottom: 12px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 15px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  border: 2px solid transparent;
}

.leaderboard-item:hover {
  transform: translateX(10px);
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.leaderboard-item.top-three {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
  border: 2px solid rgba(255, 107, 157, 0.3);
}

.leaderboard-item:nth-child(1) {
  background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
  border-color: #FFD54F;
}

.leaderboard-item:nth-child(2) {
  background: linear-gradient(135deg, #F5F5F5, #E0E0E0);
  border-color: #BDBDBD;
}

.leaderboard-item:nth-child(3) {
  background: linear-gradient(135deg, #FFF8E1, #FFECB3);
  border-color: #FFB74D;
}

.rank-badge {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin-right: 20px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.rank-badge.rank-1 {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.6);
  font-size: 2rem;
}

.rank-badge.rank-2 {
  background: linear-gradient(135deg, #C0C0C0, #A0A0A0);
  box-shadow: 0 4px 15px rgba(192, 192, 192, 0.6);
  font-size: 2rem;
}

.rank-badge.rank-3 {
  background: linear-gradient(135deg, #CD7F32, #B8860B);
  box-shadow: 0 4px 15px rgba(205, 127, 50, 0.6);
  font-size: 2rem;
}

.rank-num {
  font-size: 1.3rem;
}

.medal {
  font-size: 2rem;
}

.player-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}

.player-avatar {
  font-size: 2rem;
  width: 45px;
  height: 45px;
  background: rgba(255, 107, 157, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.player-name {
  font-weight: 700;
  color: #333;
  font-size: 1.1rem;
}

.score-info {
  display: flex;
  align-items: baseline;
  gap: 5px;
}

.score-value {
  font-size: 1.8rem;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.score-label {
  color: #888;
  font-size: 0.9rem;
}

.rank-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.leaderboard-item:hover .rank-glow {
  opacity: 0.1;
}

/* Features Section */
.features-section {
  margin-bottom: 60px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.feature-card {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
  border-radius: 20px;
  padding: 30px 20px;
  text-align: center;
  transition: all 0.3s ease;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  display: block;
}

.feature-card h3 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1.2rem;
}

.feature-card p {
  color: #666;
  font-size: 0.95rem;
}

/* Footer */
.footer {
  text-align: center;
  padding: 40px 20px;
  position: relative;
  z-index: 1;
}

.footer-content p {
  color: rgba(255, 255, 255, 0.95);
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.copyright {
  font-size: 0.95rem !important;
  opacity: 0.8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .logo {
    font-size: 2.5rem;
    flex-direction: column;
  }
  
  .logo-icon {
    font-size: 3.5rem;
  }
  
  .section-title {
    font-size: 1.5rem;
  }
  
  .game-grid {
    grid-template-columns: 1fr;
  }
  
  .leaderboard-item {
    padding: 12px 15px;
  }
  
  .player-name {
    font-size: 0.95rem;
  }
  
  .score-value {
    font-size: 1.4rem;
  }
}
</style>