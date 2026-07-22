import re

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
    subtitle: 'A Magia das Pedras',
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

  const handleScroll = () => {
    if (!scrollRef.current) return;
    const container = scrollRef.current;
    const center = container.scrollLeft + container.clientWidth / 2;
    
    let minDiff = Infinity;
    let closestIndex = selectedIndex;
    
    const children = Array.from(container.children);
    children.forEach((child) => {
      const idxStr = child.getAttribute('data-index');
      if (idxStr !== null) {
        const idx = parseInt(idxStr, 10);
        const childEl = child as HTMLElement;
        const childCenter = childEl.offsetLeft + childEl.offsetWidth / 2;
        const diff = Math.abs(center - childCenter);
        if (diff < minDiff) {
          minDiff = diff;
          closestIndex = idx;
        }
      }
    });

    if (closestIndex !== selectedIndex) {
      setSelectedIndex(closestIndex);
    }
  };

  const scrollTo = (idx: number) => {
    if (!scrollRef.current) return;
    const container = scrollRef.current;
    const children = Array.from(container.children);
    const target = children.find(c => c.getAttribute('data-index') === idx.toString()) as HTMLElement;
    if (target) {
      const scrollPos = target.offsetLeft - container.clientWidth / 2 + target.offsetWidth / 2;
      container.scrollTo({ left: scrollPos, behavior: 'smooth' });
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
        <div className="flex gap-2 text-2xl font-black tracking-wide items-center">
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400 drop-shadow-sm">Portal</span>
          <span className="text-white drop-shadow-md">Arcano</span>
        </div>
        <div className="flex gap-4 items-center text-gray-300">
          <Search size={22} className="drop-shadow-md" />
          <Settings size={22} className="drop-shadow-md" />
          <div onClick={handleSecretUnlock} className="w-9 h-9 rounded-full bg-gray-700/80 backdrop-blur-md flex items-center justify-center cursor-pointer border border-gray-500 shadow-md active:scale-95 transition-transform">
            <User size={18} className="text-white" />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col justify-start z-10 pt-8">
        {/* Horizontal Game Carousel */}
        <div className="w-full relative py-8">
          <div 
            ref={scrollRef}
            onScroll={handleScroll}
            className="flex gap-6 overflow-x-auto scrollbar-hide snap-x snap-mandatory px-[calc(50vw-4rem)] items-center"
          >
            {GAMES.map((game, idx) => {
              const isSelected = selectedIndex === idx;
              const isGameUnlocked = unlockedLevel >= game.req;
              return (
                <div 
                  key={game.id}
                  data-index={idx}
                  onClick={() => scrollTo(idx)}
                  className={`relative shrink-0 transition-all duration-300 cursor-pointer rounded-3xl overflow-hidden shadow-2xl snap-center flex items-center justify-center
                    ${isSelected ? 'w-32 h-32 border-2 border-white/80' : 'w-20 h-20 border border-transparent opacity-60 scale-90'}`}
                  style={{ backgroundColor: game.color }}
                >
                  <game.icon size={isSelected ? 54 : 32} className={isGameUnlocked ? 'text-white' : 'text-gray-400'} />
                  {!isGameUnlocked && (
                    <div className="absolute inset-0 bg-black/60 flex items-center justify-center backdrop-blur-[2px]">
                      <Lock size={isSelected ? 24 : 16} className="text-white" />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected Game Details */}
        <div className="px-8 mt-6 flex-1 flex flex-col justify-start items-center text-center pb-12">
          <AnimatePresence mode="wait">
            <motion.div
              key={selectedGame.id}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -15 }}
              transition={{ duration: 0.25 }}
              className="flex flex-col items-center w-full max-w-md"
            >
              <h1 className="text-4xl sm:text-5xl font-black mb-2 tracking-tight drop-shadow-lg text-white">
                {selectedGame.title}
              </h1>
              <p className="text-lg sm:text-xl text-gray-300 mb-10 font-medium drop-shadow-md">
                {selectedGame.subtitle}
              </p>

              {isUnlocked ? (
                <div className="flex flex-col gap-4 w-full px-2">
                  <button 
                    onClick={() => selectedGame.url && (window.location.href = selectedGame.url)}
                    className="w-full bg-white text-black py-4 rounded-full font-bold text-xl flex items-center justify-center gap-3 shadow-[0_0_20px_rgba(255,255,255,0.4)] hover:scale-105 active:scale-95 transition-transform"
                  >
                    <Gamepad2 size={26} />
                    {selectedGame.id === 'runa-master' ? 'Em Breve' : 'Jogar'}
                  </button>
                  <button className="w-full py-4 rounded-full bg-gray-800/60 text-white font-semibold flex items-center justify-center gap-2 hover:bg-gray-700/80 active:scale-95 transition-all shadow-lg border border-gray-500/50 backdrop-blur-md">
                    <Info size={20} />
                    Detalhes
                  </button>
                </div>
              ) : (
                <div className="flex flex-col gap-3 w-full px-2">
                  <div className="bg-gray-900/60 backdrop-blur-md border border-gray-700/50 rounded-3xl p-8 flex flex-col items-center shadow-xl">
                    <Lock size={36} className="text-gray-400 mb-4" />
                    <span className="text-lg font-semibold text-gray-200 mb-5">Desbloqueia no Nível {selectedGame.req}</span>
                    <div className="h-2 bg-gray-800 w-full rounded-full overflow-hidden shadow-inner">
                      <div className="h-full bg-gradient-to-r from-blue-400 to-purple-500 rounded-full transition-all duration-500" style={{ width: `${Math.min(100, (unlockedLevel / selectedGame.req) * 100)}%` }}></div>
                    </div>
                    <span className="text-sm text-gray-400 mt-4 font-medium">{unlockedLevel} / {selectedGame.req} Níveis Concluídos</span>
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

