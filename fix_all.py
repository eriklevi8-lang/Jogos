import re

# 1. Fix CSS
with open('src/index.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

if '.scrollbar-hide' not in css_content:
    css_content += """
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
"""
    with open('src/index.css', 'w', encoding='utf-8') as f:
        f.write(css_content)

# 2. Rewrite App.tsx
app_tsx = """import { useState, useEffect, useRef } from 'react';
import { Settings, FlaskConical, Gem, Lock, Search, User, Pickaxe, Gamepad2, Info } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

const GAMES = [
  {
    id: 'craft-match',
    title: 'Craft Match',
    subtitle: 'Mineração Pixelada',
    icon: Pickaxe,
    color: '#5c3a21',
    url: '/craft-match.html',
    req: 1,
    bgImage: 'linear-gradient(to bottom, rgba(92, 58, 33, 0.8), rgba(0,0,0,1))'
  },
  {
    id: 'potion-mix',
    title: 'Poção Mix',
    subtitle: 'Tetris Alquímico',
    icon: FlaskConical,
    color: '#3b3b3b',
    url: '/potion-mix.html',
    req: 5,
    bgImage: 'linear-gradient(to bottom, rgba(59, 59, 59, 0.8), rgba(0,0,0,1))'
  },
  {
    id: 'runa-master',
    title: 'Runa Master',
    subtitle: 'Em breve...',
    icon: Gem,
    color: '#4a148c',
    url: '',
    req: 10,
    bgImage: 'linear-gradient(to bottom, rgba(74, 20, 140, 0.8), rgba(0,0,0,1))'
  }
];

export default function App() {
  const [unlockedLevel, setUnlockedLevel] = useState(1);
  const [clickCount, setClickCount] = useState(0);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const level = parseInt(localStorage.getItem('craftMatchMaxLevel') || '1');
    setUnlockedLevel(level);
  }, []);

  const handleSecretUnlock = () => {
    const newCount = clickCount + 1;
    setClickCount(newCount);
    if (newCount === 5) {
      localStorage.setItem('craftMatchMaxLevel', '10');
      setUnlockedLevel(10);
      alert("Master mode ativado! Todos os jogos foram liberados.");
    }
  };

  const selectedGame = GAMES[selectedIndex];
  const isUnlocked = unlockedLevel >= selectedGame.req;

  return (
    <div className="relative min-h-screen flex flex-col font-sans text-white overflow-hidden bg-black">
      {/* Dynamic Background */}
      <div 
        className="absolute inset-0 z-0 transition-all duration-700 ease-in-out"
        style={{ background: selectedGame.bgImage }}
      />
      
      {/* Header */}
      <header className="px-6 pt-12 pb-4 flex justify-between items-center z-20">
        <div className="flex gap-6 text-lg font-semibold tracking-wide">
          <span className="text-white drop-shadow-md">Jogos</span>
          <span className="text-gray-400 drop-shadow-md">Mídia</span>
        </div>
        <div className="flex gap-4 items-center text-gray-300">
          <Search size={22} className="drop-shadow-md" />
          <Settings size={22} className="drop-shadow-md" />
          <div onClick={handleSecretUnlock} className="w-9 h-9 rounded-full bg-gray-700 flex items-center justify-center cursor-pointer border border-gray-500 shadow-md active:scale-95 transition-transform">
            <User size={18} className="text-white" />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col justify-start z-10 pt-4">
        {/* Horizontal Game Carousel */}
        <div className="pl-6 py-4">
          <div 
            ref={scrollRef}
            className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide items-end"
            style={{ scrollSnapType: 'x mandatory' }}
          >
            {GAMES.map((game, idx) => {
              const isSelected = selectedIndex === idx;
              const isGameUnlocked = unlockedLevel >= game.req;
              return (
                <div 
                  key={game.id}
                  onClick={() => {
                    setSelectedIndex(idx);
                    if (scrollRef.current) {
                        const child = scrollRef.current.children[idx] as HTMLElement;
                        scrollRef.current.scrollTo({ left: child.offsetLeft - 24, behavior: 'smooth' });
                    }
                  }}
                  className={`relative shrink-0 transition-all duration-300 cursor-pointer rounded-2xl overflow-hidden shadow-2xl ${isSelected ? 'w-24 h-24 border-2 border-white translate-y-0' : 'w-16 h-16 border border-transparent opacity-60 translate-y-2'} flex items-center justify-center`}
                  style={{ backgroundColor: game.color, scrollSnapAlign: 'start' }}
                >
                  <game.icon size={isSelected ? 40 : 24} className={isGameUnlocked ? 'text-white' : 'text-gray-400'} />
                  {!isGameUnlocked && (
                    <div className="absolute inset-0 bg-black/60 flex items-center justify-center backdrop-blur-[2px]">
                      <Lock size={isSelected ? 20 : 14} className="text-white" />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected Game Details */}
        <div className="px-6 mt-8 flex-1 flex flex-col justify-end pb-24">
          <AnimatePresence mode="wait">
            <motion.div
              key={selectedGame.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <h1 className="text-5xl font-black mb-1 tracking-tight drop-shadow-lg">{selectedGame.title}</h1>
              <p className="text-xl text-gray-200 mb-8 font-medium drop-shadow-md">{selectedGame.subtitle}</p>

              {isUnlocked ? (
                <div className="flex gap-4 items-center">
                  <button 
                    onClick={() => selectedGame.url && (window.location.href = selectedGame.url)}
                    className="bg-white text-black px-8 py-4 rounded-full font-bold text-lg flex items-center gap-3 shadow-[0_0_20px_rgba(255,255,255,0.3)] hover:scale-105 active:scale-95 transition-transform"
                  >
                    <Gamepad2 size={24} />
                    {selectedGame.id === 'runa-master' ? 'Em Breve' : 'Jogar'}
                  </button>
                  <button className="w-14 h-14 rounded-full bg-gray-800/80 backdrop-blur-md flex items-center justify-center hover:bg-gray-700 active:scale-95 transition-all shadow-lg border border-gray-600">
                    <Info size={24} className="text-white" />
                  </button>
                </div>
              ) : (
                <div className="flex flex-col gap-3">
                  <div className="text-gray-300 flex items-center gap-2 drop-shadow-md">
                    <Lock size={20} />
                    <span className="text-lg font-semibold">Desbloqueia no Nível {selectedGame.req}</span>
                  </div>
                  <div className="h-1.5 bg-gray-800 w-64 rounded-full overflow-hidden mt-2 shadow-inner">
                    <div className="h-full bg-gray-400" style={{ width: `${Math.min(100, (unlockedLevel / selectedGame.req) * 100)}%` }}></div>
                  </div>
                </div>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
"""
with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(app_tsx)

# 3. Fix Potion Mix logic for rotation double tap
with open('potion-mix.html', 'r', encoding='utf-8') as f:
    potion = f.read()

potion_old = """        canvas.addEventListener('touchend', e => {
            if (isGameOver) return;
            if (!hasDragged) {
                playerRotate(1);
            }
        }, {passive: false});"""

potion_new = """        let lastTapTime = 0;
        canvas.addEventListener('touchend', e => {
            if (isGameOver) return;
            e.preventDefault(); // Prevent double triggering via simulated mouse events
            
            const now = performance.now();
            if (!hasDragged) {
                // simple debounce
                if (now - lastTapTime > 150) {
                    playerRotate(1);
                    lastTapTime = now;
                }
            }
        }, {passive: false});"""

if potion_old in potion:
    potion = potion.replace(potion_old, potion_new)
    with open('potion-mix.html', 'w', encoding='utf-8') as f:
        f.write(potion)

