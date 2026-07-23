import { useState, useEffect, useRef } from 'react';
import { Settings, FlaskConical, Gem, Lock, Search, User, Pickaxe, Gamepad2, Swords } from 'lucide-react';

import { motion, AnimatePresence } from 'motion/react';
import { ParticlesBackground } from './components/ParticlesBackground';

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
    url: '/runa-master.html',
    req: 10,
    bgImage: 'linear-gradient(to bottom, rgba(74, 20, 140, 0.8), rgba(0,0,0,1))'
  },
  {
    id: 'aether-royale',
    title: 'Aether Royale',
    subtitle: 'Batalha Arcana',
    icon: Swords,
    color: '#1d4ed8',
    url: '/aether-royale.html',
    req: 15,
    bgImage: 'linear-gradient(to bottom, rgba(29, 78, 216, 0.8), rgba(0,0,0,1))'
  }
];

export default function App() {
  const [unlockedLevel, setUnlockedLevel] = useState(1);
  const [clickCount, setClickCount] = useState(0);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const scrollRef = useRef<HTMLDivElement>(null);
  const scrollVelocityRef = useRef(0);
  const lastScrollLeft = useRef(0);
  const touchStartRef = useRef<number | null>(null);
  const [isReady, setIsReady] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const level = parseInt(localStorage.getItem('craftMatchMaxLevel') || '1');
    setUnlockedLevel(level);
    setIsReady(true);
    
    // Initial loading screen
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1800);
    return () => clearTimeout(timer);
  }, []);

  // Request devicemotion on first interaction
  useEffect(() => {
    const handleFirstClick = () => {
      if (typeof (DeviceMotionEvent as any).requestPermission === 'function') {
        (DeviceMotionEvent as any).requestPermission().catch(() => {});
      }
      document.removeEventListener('click', handleFirstClick);
      document.removeEventListener('touchstart', handleFirstClick);
    };
    document.addEventListener('click', handleFirstClick);
    document.addEventListener('touchstart', handleFirstClick);
    return () => {
      document.removeEventListener('click', handleFirstClick);
      document.removeEventListener('touchstart', handleFirstClick);
    };
  }, []);

  useEffect(() => {
    let lastShake = 0;
    const handleMotion = (e: DeviceMotionEvent) => {
      if (!e.acceleration) return;
      const { x, y, z } = e.acceleration;
      const acceleration = Math.sqrt((x || 0) ** 2 + (y || 0) ** 2 + (z || 0) ** 2);
      
      if (acceleration > 15) {
        const now = Date.now();
        if (now - lastShake > 1000) {
          lastShake = now;
          setSelectedIndex((prev) => {
             const next = (prev + 1) % GAMES.length;
             scrollTo(next);
             return next;
          });
        }
      }
    };
    window.addEventListener('devicemotion', handleMotion);
    return () => window.removeEventListener('devicemotion', handleMotion);
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
    const currentScrollLeft = container.scrollLeft;
    scrollVelocityRef.current = currentScrollLeft - lastScrollLeft.current;
    lastScrollLeft.current = currentScrollLeft;

    const center = currentScrollLeft + container.clientWidth / 2;
    
    let minDiff = Infinity;
    let closestIndex = selectedIndex;
    
    const children = Array.from(container.children) as HTMLElement[];
    children.forEach((child) => {
      const idxStr = child.getAttribute('data-index');
      if (idxStr !== null) {
        const idx = parseInt(idxStr, 10);
        const childCenter = child.offsetLeft + child.offsetWidth / 2;
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
    const children = Array.from(container.children) as HTMLElement[];
    const target = children.find(c => c.getAttribute('data-index') === idx.toString());
    if (target) {
      const scrollPos = target.offsetLeft - container.clientWidth / 2 + target.offsetWidth / 2;
      container.scrollTo({ left: scrollPos, behavior: 'smooth' });
    }
  };

  const handleTouchStart = (e: any) => {
    const target = e.target as HTMLElement;
    if (target.closest('.scrollbar-hide')) return; // Let carousel handle its own swipe
    touchStartRef.current = e.touches[0].clientX;
  };

  const handleTouchEnd = (e: any) => {
    if (touchStartRef.current === null) return;
    const touchEndX = e.changedTouches[0].clientX;
    const diff = touchStartRef.current - touchEndX;
    
    if (Math.abs(diff) > 50) {
      if (diff > 0 && selectedIndex < GAMES.length - 1) {
        const next = selectedIndex + 1;
        setSelectedIndex(next);
        scrollTo(next);
      } else if (diff < 0 && selectedIndex > 0) {
        const prev = selectedIndex - 1;
        setSelectedIndex(prev);
        scrollTo(prev);
      }
    }
    touchStartRef.current = null;
  };

  const handlePlay = (url: string) => {
    if (!url) return;
    setIsLoading(true);
    setTimeout(() => {
      window.location.href = url;
    }, 1500);
  };

  const selectedGame = GAMES[selectedIndex];
  const isUnlocked = true; // Always unlocked

  if (!isReady) return null;

  return (
    <div 
      className="relative min-h-screen flex flex-col font-sans text-white overflow-hidden bg-black"
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
    >
      <AnimatePresence>
        {isLoading && (
          <motion.div
            initial={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
            className="absolute inset-0 z-[100] flex flex-col items-center justify-center bg-black/80 backdrop-blur-xl"
          >
            <motion.div 
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="flex flex-col items-center gap-6"
            >
              <div className="relative flex items-center justify-center w-24 h-24 rounded-3xl bg-gradient-to-br from-blue-500/20 to-purple-600/20 border border-white/10 shadow-[0_0_30px_rgba(139,92,246,0.3)] backdrop-blur-md">
                <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-blue-400 to-purple-500 opacity-20 animate-pulse"></div>
                <Gamepad2 size={56} className="text-purple-300 drop-shadow-[0_0_12px_rgba(168,85,247,0.8)]" />
              </div>
              <div className="flex flex-col items-center text-center">
                <span className="text-5xl font-black tracking-wider leading-none">
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 via-blue-400 to-purple-500 drop-shadow-lg">PORTAL</span>
                </span>
                <span className="text-lg font-bold tracking-[0.4em] text-gray-300 uppercase pl-1 drop-shadow-md mt-1 opacity-90">
                  Arcano
                </span>
              </div>
              <div className="mt-8 flex items-center gap-3 text-purple-300">
                <div className="w-5 h-5 border-2 border-purple-400 border-t-transparent rounded-full animate-spin"></div>
                <span className="text-sm font-semibold tracking-widest uppercase">Carregando</span>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Dynamic Background */}
      <div 
        className="absolute inset-0 z-0 transition-all duration-700 ease-in-out"
        style={{ background: selectedGame.bgImage }}
      />
      
      <ParticlesBackground scrollVelocityRef={scrollVelocityRef} />

      {/* Header */}
      <header className="px-6 pt-12 pb-4 flex justify-between items-center z-20">
        <div className="flex items-center gap-3">
          {/* Logo Icon */}
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500/20 to-purple-600/20 border border-white/10 shadow-[0_0_15px_rgba(139,92,246,0.3)] backdrop-blur-md">
            <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-blue-400 to-purple-500 opacity-20 animate-pulse"></div>
            <Gamepad2 size={24} className="text-purple-300 drop-shadow-[0_0_8px_rgba(168,85,247,0.8)]" />
          </div>
          {/* Logo Text */}
          <div className="flex flex-col">
            <span className="text-2xl font-black tracking-wider leading-none">
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 via-blue-400 to-purple-500 drop-shadow-lg">PORTAL</span>
            </span>
            <span className="text-[0.8rem] font-bold tracking-[0.3em] text-gray-300 uppercase pl-1 drop-shadow-md -mt-1 opacity-90">
              Arcano
            </span>
          </div>
        </div>
        <div className="flex gap-4 items-center text-gray-300">
          <Search size={22} className="drop-shadow-md cursor-pointer hover:text-white transition-colors" />
          <Settings size={22} className="drop-shadow-md cursor-pointer hover:text-white transition-colors" />
          <div onClick={handleSecretUnlock} className="w-9 h-9 rounded-full bg-gray-800/80 backdrop-blur-md flex items-center justify-center cursor-pointer border border-white/10 shadow-[0_0_10px_rgba(0,0,0,0.5)] hover:bg-gray-700/80 active:scale-95 transition-all">
            <User size={18} className="text-purple-200" />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col justify-start z-10 pt-8">
        {/* Horizontal Game Carousel */}
        <div className="w-full relative">
          <div 
            ref={scrollRef}
            onScroll={handleScroll}
            className="flex gap-6 overflow-x-auto scrollbar-hide snap-x snap-mandatory px-[calc(50vw-4rem)] items-center py-10"
          >
            {GAMES.map((game, idx) => {
              const isSelected = selectedIndex === idx;
              const isGameUnlocked = true; // Always unlocked
              return (
                <div 
                  key={game.id}
                  data-index={idx}
                  onClick={() => scrollTo(idx)}
                  className={`relative shrink-0 transition-all duration-500 cursor-pointer rounded-3xl snap-center flex items-center justify-center backdrop-blur-md
                    ${isSelected 
                      ? 'w-32 h-32 border-2 border-white/80 scale-110 shadow-[0_0_20px_rgba(255,255,255,0.4)] z-10' 
                      : 'w-24 h-24 border border-white/10 opacity-70 scale-90 blur-[2px] brightness-50 z-0'}`}
                  style={{ backgroundColor: `${game.color}cc` }}
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
                    onClick={() => handlePlay(selectedGame.url)}
                    className="w-full bg-white text-black py-4 rounded-full font-bold text-xl flex items-center justify-center gap-3 shadow-[0_0_20px_rgba(255,255,255,0.4)] hover:scale-105 active:scale-95 transition-transform"
                  >
                    <Gamepad2 size={26} />
                    Jogar
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
