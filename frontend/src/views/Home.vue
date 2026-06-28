<template>
  <div class="home-container">
    <AnimeBackground />
    
    <!-- 浮动粒子装饰 -->
    <div class="floating-particles">
      <div class="particle" v-for="i in 20" :key="i" :style="{ '--i': i }"></div>
    </div>
    
    <!-- 流星动画 -->
    <div class="shooting-stars">
      <div class="shooting-star" v-for="i in 5" :key="'star'+i" :style="{ '--i': i }"></div>
    </div>

    <header class="header">
      <div class="logo-wrapper">
        <div class="logo-icon-container">
          <span class="logo-icon">🎮</span>
          <div class="icon-glow"></div>
        </div>
        <h1 class="logo-text">游戏星球</h1>
        <p class="slogan">✨ 释放你的游戏天赋 ✨</p>
      </div>
      <div class="header-decoration">
        <div class="deco-star" v-for="i in 12" :key="i" :style="{ '--i': i }">⭐</div>
      </div>
    </header>

    <main class="main-content">
      <!-- 开场横幅 -->
      <section class="hero-banner">
        <div class="hero-content">
          <div class="hero-icon">🎯</div>
          <h2>今日热门推荐</h2>
          <p>挑战你的极限，创造新纪录!</p>
        </div>
        <div class="hero-decoration">
          <div class="floating-emoji">🔥</div>
          <div class="floating-emoji">⚡</div>
          <div class="floating-emoji">💪</div>
        </div>
      </section>

      <section class="games-section">
        <h2 class="section-title">
          <span class="title-icon">🎮</span>
          <span class="title-text">热门游戏</span>
          <span class="title-decoration"></span>
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
            <div class="card-border"></div>
            <div class="game-icon-wrapper">
              <span class="game-icon">{{ game.icon }}</span>
              <div class="icon-shine"></div>
            </div>
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
            <div class="card-hover-border"></div>
          </div>
        </div>
      </section>

      <section class="leaderboard-section">
        <h2 class="section-title">
          <span class="title-icon">🏆</span>
          <span class="title-text">排行榜</span>
          <span class="title-badge">TOP 10</span>
          <span class="title-decoration"></span>
        </h2>
        <div class="leaderboard">
          <div class="leaderboard-header">
            <div class="header-glow"></div>
            <span class="header-title">🏅 最强玩家榜单</span>
          </div>
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
              <span class="player-avatar" :style="{ '--avatar-bg': getAvatarBg(index) }">{{ getAvatar(item.player_name) }}</span>
              <div class="player-detail">
                <span class="player-name">{{ item.player_name }}</span>
                <span class="player-title">{{ getPlayerTitle(index) }}</span>
              </div>
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
          <span class="title-text">为什么选择我们</span>
          <span class="title-decoration"></span>
        </h2>
        <div class="features-grid">
          <div class="feature-card" v-for="feature in features" :key="feature.icon">
            <div class="feature-icon-wrapper">
              <span class="feature-icon">{{ feature.icon }}</span>
              <div class="feature-glow"></div>
            </div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.desc }}</p>
            <div class="feature-border"></div>
          </div>
        </div>
      </section>
      
      <!-- 活动横幅 -->
      <section class="event-banner">
        <div class="event-content">
          <span class="event-icon">🎉</span>
          <div class="event-text">
            <h3>限时活动</h3>
            <p>2048挑战大赛火热进行中!</p>
          </div>
          <button class="event-btn" @click="navigateToGame(1)">立即参与</button>
        </div>
        <div class="event-particles">
          <span v-for="i in 8" :key="i" class="event-particle" :style="{ '--i': i }">✨</span>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="footer-content">
        <div class="footer-logo">🎮 游戏星球</div>
        <p>让快乐触手可及</p>
        <p class="copyright">© 2026 GameStar | 快乐游戏，健康生活 🎮</p>
      </div>
      <div class="footer-stars">
        <span v-for="i in 20" :key="i" class="footer-star" :style="{ '--i': i }">⭐</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api.js'
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

const getAvatarBg = (index) => {
  const colors = ['rgba(255, 215, 0, 0.2)', 'rgba(192, 192, 192, 0.2)', 'rgba(205, 127, 50, 0.2)', 'rgba(255, 107, 157, 0.1)']
  return colors[Math.min(index, 3)]
}

const getPlayerTitle = (index) => {
  const titles = ['传奇大师', '荣耀王者', '黄金战神', '钻石高手', '铂金玩家', '白银挑战者', '青铜新手']
  return titles[Math.min(index, titles.length - 1)]
}

const formatNumber = (num) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num.toLocaleString()
}

onMounted(async () => {
  try {
    const gamesRes = await api.get('/api/games')
    games.value = gamesRes.data
    
    const leaderboardRes = await api.get('/api/leaderboard?limit=10')
    leaderboard.value = leaderboardRes.data
    
    if (leaderboard.value.length === 0) {
      leaderboard.value = getDefaultLeaderboard()
    }
  } catch (error) {
    console.error('Failed to load data:', error)
    games.value = [
      { id: 1, name: '2048', description: '经典数字合成游戏，使用方向键移动方块，合成出2048', icon: '🔢', play_count: 12580, rating: 49 }
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

/* 浮动粒子 */
.floating-particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.particle {
  position: absolute;
  width: 8px;
  height: 8px;
  background: radial-gradient(circle, #FFD700 0%, #FF6B9D 50%, transparent 100%);
  border-radius: 50%;
  left: calc(var(--i) * 5%);
  animation: particle-float 15s ease-in-out infinite;
  animation-delay: calc(var(--i) * 0.5s);
}

@keyframes particle-float {
  0%, 100% { transform: translateY(0) translateX(0); opacity: 0; }
  10% { opacity: 0.8; }
  50% { transform: translateY(-50vh) translateX(20px); opacity: 0.6; }
  90% { opacity: 0.8; }
  100% { transform: translateY(-100vh) translateX(-20px); }
}

/* 流星 */
.shooting-stars {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.shooting-star {
  position: absolute;
  top: -50px;
  width: 100px;
  height: 2px;
  background: linear-gradient(to right, #fff, transparent);
  left: calc(var(--i) * 20%);
  animation: shooting 8s ease-in-out infinite;
  animation-delay: calc(var(--i) * 1.5s);
  opacity: 0;
}

@keyframes shooting {
  0% { opacity: 0; transform: rotate(-45deg) translateX(-100px); }
  10% { opacity: 1; }
  20% { opacity: 0; transform: rotate(-45deg) translateX(500px) translateY(300px); }
  100% { opacity: 0; }
}

/* Header */
.header {
  text-align: center;
  margin-bottom: 60px;
  position: relative;
  z-index: 1;
  padding: 40px 20px;
}

.logo-wrapper {
  position: relative;
  display: inline-block;
}

.logo-icon-container {
  position: relative;
  display: inline-block;
  margin-bottom: 15px;
}

.logo-icon {
  font-size: 6rem;
  display: block;
  animation: bounce-icon 3s ease-in-out infinite;
  position: relative;
  z-index: 2;
}

.icon-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 120px;
  background: radial-gradient(circle, rgba(255, 107, 157, 0.4) 0%, rgba(168, 85, 247, 0.2) 50%, transparent 70%);
  border-radius: 50%;
  animation: glow-pulse 2s ease-in-out infinite;
}

@keyframes bounce-icon {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-20px) scale(1.1); }
}

@keyframes glow-pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.6; }
  50% { transform: translate(-50%, -50%) scale(1.3); opacity: 1; }
}

.logo-text {
  font-size: 4.5rem;
  background: linear-gradient(135deg, #fff 0%, #FF6B9D 30%, #C44BE9 60%, #fff 100%);
  background-size: 400% 400%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 40px rgba(255, 255, 255, 0.5);
  animation: text-gradient 3s ease infinite;
  margin-bottom: 15px;
}

@keyframes text-gradient {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.slogan {
  font-size: 1.6rem;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 600;
  letter-spacing: 3px;
  animation: slogan-fade 2s ease-out;
}

@keyframes slogan-fade {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.header-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.deco-star {
  position: absolute;
  font-size: 1.5rem;
  animation: star-twinkle 2s ease-in-out infinite;
  animation-delay: calc(var(--i) * 0.15s);
}

.deco-star:nth-child(1) { top: 10%; left: 10%; }
.deco-star:nth-child(2) { top: 15%; right: 15%; }
.deco-star:nth-child(3) { top: 30%; left: 5%; }
.deco-star:nth-child(4) { top: 40%; right: 8%; }
.deco-star:nth-child(5) { top: 20%; left: 20%; }
.deco-star:nth-child(6) { top: 25%; right: 25%; }
.deco-star:nth-child(7) { top: 50%; left: 3%; }
.deco-star:nth-child(8) { top: 55%; right: 5%; }
.deco-star:nth-child(9) { bottom: 20%; left: 12%; }
.deco-star:nth-child(10) { bottom: 15%; right: 18%; }
.deco-star:nth-child(11) { bottom: 30%; left: 8%; }
.deco-star:nth-child(12) { bottom: 35%; right: 10%; }

@keyframes star-twinkle {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.3; transform: scale(0.7); }
}

/* 开场横幅 */
.hero-banner {
  background: linear-gradient(135deg, rgba(255, 107, 157, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%);
  border-radius: 30px;
  padding: 30px;
  margin-bottom: 50px;
  position: relative;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.hero-content {
  text-align: center;
  position: relative;
  z-index: 2;
}

.hero-icon {
  font-size: 4rem;
  animation: hero-bounce 2s ease-in-out infinite;
}

@keyframes hero-bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.15); }
}

.hero-content h2 {
  font-size: 2.5rem;
  color: #fff;
  margin: 15px 0;
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
}

.hero-content p {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
}

.hero-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.floating-emoji {
  position: absolute;
  font-size: 2.5rem;
  animation: emoji-float 4s ease-in-out infinite;
}

.floating-emoji:nth-child(1) { top: 20%; left: 10%; animation-delay: 0s; }
.floating-emoji:nth-child(2) { top: 30%; right: 15%; animation-delay: 1.5s; }
.floating-emoji:nth-child(3) { bottom: 25%; left: 20%; animation-delay: 3s; }

@keyframes emoji-float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(10deg); }
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
  font-size: 2.2rem;
  margin-bottom: 35px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  position: relative;
}

.title-icon {
  font-size: 2.8rem;
  animation: icon-wiggle 2s ease-in-out infinite;
}

@keyframes icon-wiggle {
  0%, 100% { transform: rotate(-8deg); }
  50% { transform: rotate(8deg); }
}

.title-text {
  background: linear-gradient(135deg, #fff, #FFE66D);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.title-decoration {
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 4px;
  background: linear-gradient(90deg, transparent, #FF6B9D, transparent);
  border-radius: 2px;
}

.title-badge {
  background: linear-gradient(135deg, #FFE66D, #FF6B6B);
  padding: 6px 18px;
  border-radius: 25px;
  font-size: 0.9rem;
  font-weight: normal;
  color: #333;
  animation: badge-pulse 2s ease-in-out infinite;
}

@keyframes badge-pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Game Cards */
.game-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 35px;
  margin-bottom: 70px;
}

.game-card {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(255, 255, 255, 0.9));
  border-radius: 30px;
  padding: 40px 35px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.4);
}

.game-card:hover {
  transform: translateY(-20px) scale(1.03);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3),
              0 0 60px var(--card-color);
}

.card-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, var(--card-color) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.game-card:hover .card-glow {
  opacity: 0.12;
}

.card-border {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 30px;
  padding: 2px;
  background: linear-gradient(135deg, var(--card-color), transparent, var(--card-color));
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.game-card:hover .card-border {
  opacity: 0.5;
}

.card-hover-border {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 32px;
  border: 3px solid var(--card-color);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.game-card:hover .card-hover-border {
  opacity: 0.6;
}

.game-icon-wrapper {
  position: relative;
  margin-bottom: 25px;
}

.game-icon {
  font-size: 6rem;
  display: block;
  filter: drop-shadow(0 8px 20px rgba(0, 0, 0, 0.2));
  transition: transform 0.3s ease;
}

.game-card:hover .game-icon {
  transform: scale(1.1) rotate(5deg);
}

.icon-shine {
  position: absolute;
  top: 10%;
  right: 10%;
  width: 30%;
  height: 30%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.8) 0%, transparent 70%);
  border-radius: 50%;
}

.game-title {
  font-size: 2rem;
  color: #333;
  margin-bottom: 15px;
  font-weight: 800;
  transition: color 0.3s ease;
}

.game-card:hover .game-title {
  color: var(--card-color);
}

.game-desc {
  color: #666;
  margin-bottom: 25px;
  font-size: 1rem;
  line-height: 1.7;
}

.game-meta {
  display: flex;
  justify-content: space-between;
  padding-top: 20px;
  border-top: 2px dashed rgba(0, 0, 0, 0.1);
}

.play-count, .rating {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #888;
  font-size: 1rem;
  font-weight: 600;
}

.meta-icon {
  font-size: 1.4rem;
}

.card-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
  transition: left 0.6s ease;
}

.game-card:hover .card-shine {
  left: 100%;
}

/* Leaderboard */
.leaderboard-section {
  margin-bottom: 70px;
}

.leaderboard {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(255, 255, 255, 0.92));
  border-radius: 30px;
  padding: 35px;
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.4);
  position: relative;
  overflow: hidden;
}

.leaderboard-header {
  text-align: center;
  padding-bottom: 25px;
  margin-bottom: 25px;
  border-bottom: 2px dashed rgba(0, 0, 0, 0.1);
  position: relative;
}

.header-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 50px;
  background: radial-gradient(ellipse, rgba(255, 215, 0, 0.3) 0%, transparent 70%);
}

.header-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  position: relative;
  z-index: 2;
}

.leaderboard-item {
  display: flex;
  align-items: center;
  padding: 20px 25px;
  margin-bottom: 15px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  transition: all 0.35s ease;
  position: relative;
  overflow: hidden;
  border: 2px solid transparent;
}

.leaderboard-item:hover {
  transform: translateX(15px);
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.leaderboard-item.top-three {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(255, 255, 255, 0.95));
  border: 2px solid rgba(255, 107, 157, 0.3);
}

.leaderboard-item:nth-child(2) {
  background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
  border-color: #FFD54F;
}

.leaderboard-item:nth-child(3) {
  background: linear-gradient(135deg, #F5F5F5, #E0E0E0);
  border-color: #BDBDBD;
}

.leaderboard-item:nth-child(4) {
  background: linear-gradient(135deg, #FFF8E1, #FFECB3);
  border-color: #FFB74D;
}

.rank-badge {
  width: 55px;
  height: 55px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: bold;
  margin-right: 22px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.5);
  transition: transform 0.3s ease;
}

.leaderboard-item:hover .rank-badge {
  transform: scale(1.1);
}

.rank-badge.rank-1 {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  box-shadow: 0 5px 20px rgba(255, 215, 0, 0.7);
  font-size: 2.5rem;
}

.rank-badge.rank-2 {
  background: linear-gradient(135deg, #C0C0C0, #A0A0A0);
  box-shadow: 0 5px 20px rgba(192, 192, 192, 0.7);
  font-size: 2.5rem;
}

.rank-badge.rank-3 {
  background: linear-gradient(135deg, #CD7F32, #B8860B);
  box-shadow: 0 5px 20px rgba(205, 127, 50, 0.7);
  font-size: 2.5rem;
}

.rank-num {
  font-size: 1.5rem;
}

.medal {
  font-size: 2.5rem;
}

.player-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 15px;
}

.player-avatar {
  font-size: 2.2rem;
  width: 55px;
  height: 55px;
  background: var(--avatar-bg);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(255, 107, 157, 0.3);
}

.player-detail {
  display: flex;
  flex-direction: column;
}

.player-name {
  font-weight: 800;
  color: #333;
  font-size: 1.2rem;
}

.player-title {
  font-size: 0.85rem;
  color: #999;
  margin-top: 3px;
}

.score-info {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.score-value {
  font-size: 2rem;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.score-label {
  color: #888;
  font-size: 1rem;
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
  margin-bottom: 70px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 25px;
}

.feature-card {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
  border-radius: 25px;
  padding: 35px 25px;
  text-align: center;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 2px solid rgba(255, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.feature-card:hover {
  transform: translateY(-15px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
}

.feature-icon-wrapper {
  position: relative;
  margin-bottom: 20px;
}

.feature-icon {
  font-size: 4rem;
  display: block;
  position: relative;
  z-index: 2;
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.15);
}

.feature-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: radial-gradient(circle, rgba(255, 107, 157, 0.3) 0%, transparent 70%);
  animation: feature-glow-pulse 2s ease-in-out infinite;
}

@keyframes feature-glow-pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
  50% { transform: translate(-50%, -50%) scale(1.3); opacity: 0.8; }
}

.feature-card h3 {
  color: #333;
  margin-bottom: 12px;
  font-size: 1.3rem;
  font-weight: 700;
}

.feature-card p {
  color: #666;
  font-size: 1rem;
  line-height: 1.6;
}

.feature-border {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 4px;
  background: linear-gradient(90deg, transparent, #FF6B9D, transparent);
  border-radius: 2px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feature-card:hover .feature-border {
  opacity: 1;
}

/* 活动横幅 */
.event-banner {
  background: linear-gradient(135deg, rgba(255, 107, 157, 0.3) 0%, rgba(168, 85, 247, 0.3) 50%, rgba(255, 230, 109, 0.3) 100%);
  border-radius: 30px;
  padding: 35px;
  margin-bottom: 50px;
  position: relative;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.event-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  position: relative;
  z-index: 2;
}

.event-icon {
  font-size: 4rem;
  animation: event-bounce 2s ease-in-out infinite;
}

@keyframes event-bounce {
  0%, 100% { transform: scale(1) rotate(0deg); }
  50% { transform: scale(1.1) rotate(10deg); }
}

.event-text {
  flex: 1;
}

.event-text h3 {
  font-size: 1.8rem;
  color: #fff;
  margin-bottom: 8px;
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
}

.event-text p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.9);
}

.event-btn {
  background: linear-gradient(135deg, #FFE66D, #FF6B6B);
  border: none;
  border-radius: 25px;
  padding: 15px 35px;
  font-size: 1.1rem;
  font-weight: bold;
  color: #333;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.event-btn:hover {
  transform: scale(1.08);
  box-shadow: 0 10px 30px rgba(255, 230, 109, 0.4);
}

.event-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.event-particle {
  position: absolute;
  font-size: 1.5rem;
  animation: event-particle-float 3s ease-in-out infinite;
  animation-delay: calc(var(--i) * 0.3s);
}

.event-particle:nth-child(1) { top: 10%; left: 10%; }
.event-particle:nth-child(2) { top: 20%; right: 20%; }
.event-particle:nth-child(3) { top: 60%; left: 15%; }
.event-particle:nth-child(4) { top: 70%; right: 10%; }
.event-particle:nth-child(5) { bottom: 20%; left: 30%; }
.event-particle:nth-child(6) { bottom: 30%; right: 25%; }
.event-particle:nth-child(7) { top: 40%; left: 5%; }
.event-particle:nth-child(8) { top: 50%; right: 5%; }

@keyframes event-particle-float {
  0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.6; }
  50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
}

/* Footer */
.footer {
  text-align: center;
  padding: 50px 20px;
  position: relative;
  z-index: 1;
}

.footer-content {
  position: relative;
  z-index: 2;
}

.footer-logo {
  font-size: 1.8rem;
  font-weight: bold;
  color: #fff;
  margin-bottom: 15px;
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
}

.footer-content p {
  color: rgba(255, 255, 255, 0.95);
  font-size: 1.3rem;
  margin-bottom: 12px;
}

.copyright {
  font-size: 1rem !important;
  opacity: 0.8;
}

.footer-stars {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.footer-star {
  position: absolute;
  font-size: 1.2rem;
  animation: footer-star-twinkle 3s ease-in-out infinite;
  animation-delay: calc(var(--i) * 0.15s);
  opacity: 0.5;
}

.footer-star:nth-child(odd) { top: calc(var(--i) * 5%); left: calc(var(--i) * 3%); }
.footer-star:nth-child(even) { bottom: calc(var(--i) * 4%); right: calc(var(--i) * 3%); }

@keyframes footer-star-twinkle {
  0%, 100% { opacity: 0.3; transform: scale(0.8); }
  50% { opacity: 0.8; transform: scale(1.2); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .logo-text {
    font-size: 3rem;
  }
  
  .logo-icon {
    font-size: 4.5rem;
  }
  
  .section-title {
    font-size: 1.6rem;
  }
  
  .game-grid {
    grid-template-columns: 1fr;
  }
  
  .leaderboard-item {
    padding: 15px 20px;
  }
  
  .player-name {
    font-size: 1rem;
  }
  
  .score-value {
    font-size: 1.5rem;
  }
  
  .event-content {
    flex-direction: column;
    text-align: center;
  }
  
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .hero-content h2 {
    font-size: 1.8rem;
  }
}
</style>