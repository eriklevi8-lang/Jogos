import { useState, useEffect } from 'react';
import { Settings, FlaskConical, Gem, Lock, Home, Trophy, Pickaxe } from 'lucide-react';


export default function App() {
  const [unlockedLevel, setUnlockedLevel] = useState(1);
  const [clickCount, setClickCount] = useState(0);

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

  const potionUnlocked = unlockedLevel >= 5;
  const runaUnlocked = unlockedLevel >= 10;

  return (
    <div className="relative min-h-screen flex flex-col z-10 font-pixel text-white">
      {/* Header */}
      <header className="px-6 pt-12 pb-4 flex justify-between items-center z-20 sticky top-0 bg-[#5c3a21] pixel-border border-b-0 shadow-lg">
        <div className="flex items-center gap-3">
          <div onClick={handleSecretUnlock} className="relative flex items-center justify-center w-12 h-12 bg-[#7d7d7d] pixel-border cursor-pointer active:scale-95 transition-transform">
            <Pickaxe className="text-white" size={24} />
          </div>
          <h1 className="text-3xl font-black text-[#ffd700] drop-shadow-[3px_3px_0_#000] tracking-widest">
            PORTAL
          </h1>
        </div>
        <button className="p-2 bg-[#7d7d7d] pixel-border hover:bg-[#9e9e9e] active:scale-95 transition-all text-white">
          <Settings size={26} />
        </button>
      </header>

      {/* Main Content */}
      <main className="flex-1 px-6 py-6 flex flex-col gap-6 z-10 overflow-y-auto pb-32 max-w-lg mx-auto w-full">
        {/* Active Game Card: Craft Match */}
        <div 
          className="relative cursor-pointer active:scale-95 transition-transform w-full bg-[#5c3a21] pixel-border p-6 flex flex-col items-center gap-4"
          onClick={() => window.location.href = '/craft-match.html'}
        >
          <div className="text-6xl drop-shadow-[3px_3px_0_rgba(0,0,0,1)] hover:scale-110 transition-transform duration-300">
            ⛏️
          </div>
          
          <div className="text-center">
            <h3 className="text-3xl font-bold text-white tracking-wide mb-1 drop-shadow-[3px_3px_0_#000]">
              Craft Match
            </h3>
            <p className="text-[#a8e6cf] text-lg drop-shadow-[2px_2px_0_#000]">Mineração Pixelada</p>
          </div>
          
          <div className="w-full h-4 bg-black border-2 border-[#5c5c5c] mt-2 relative">
            <div className="h-full bg-[#4caf50] w-1/3 shadow-[inset_0_-2px_0_#388e3c]"></div>
          </div>
          
          <span className="text-lg text-[#ffd700] uppercase font-bold drop-shadow-[2px_2px_0_#000] animate-pulse">
            Tocar para Jogar
          </span>
        </div>

        <div className="h-2"></div>

        {/* Poção Mix */}
        <div 
          className={`relative p-5 flex items-center gap-5 pixel-border ${potionUnlocked ? 'bg-[#5c3a21] cursor-pointer active:scale-95 transition-transform' : 'bg-[#7d7d7d] opacity-80 grayscale-[50%]'}`}
          onClick={() => potionUnlocked && (window.location.href = '/potion-mix.html')}
        >
           <div className={`w-14 h-14 flex items-center justify-center relative shrink-0 pixel-border-sm ${potionUnlocked ? 'bg-[#8c5d38]' : 'bg-[#5c5c5c]'}`}>
              {!potionUnlocked && <Lock className="absolute top-1 right-1 text-black" size={12} />}
              <FlaskConical size={28} className={potionUnlocked ? "text-[#00ffaa]" : "text-[#a8e6cf]"} />
           </div>
           <div className="flex-1">
             <h3 className="text-2xl font-bold text-white drop-shadow-[2px_2px_0_#000]">Poção Mix</h3>
             <p className={potionUnlocked ? "text-[#ffd700] text-lg drop-shadow-[2px_2px_0_#000] mt-1 animate-pulse" : "text-[#ff9a9e] text-lg drop-shadow-[2px_2px_0_#000] mt-1"}>
                {potionUnlocked ? 'Tocar para Jogar' : 'Nível 5 req.'}
             </p>
           </div>
        </div>

        {/* Runa Master */}
        <div 
          className={`relative p-5 flex items-center gap-5 pixel-border ${runaUnlocked ? 'bg-[#5c3a21] cursor-pointer active:scale-95 transition-transform' : 'bg-[#7d7d7d] opacity-80 grayscale-[50%]'}`}
          onClick={() => runaUnlocked && alert('Em breve!')}
        >
           <div className={`w-14 h-14 flex items-center justify-center relative shrink-0 pixel-border-sm ${runaUnlocked ? 'bg-[#8c5d38]' : 'bg-[#5c5c5c]'}`}>
              {!runaUnlocked && <Lock className="absolute top-1 right-1 text-black" size={12} />}
              <Gem size={28} className={runaUnlocked ? "text-[#00ffff]" : "text-[#ffd700]"} />
           </div>
           <div className="flex-1">
             <h3 className="text-2xl font-bold text-white drop-shadow-[2px_2px_0_#000]">Runa Master</h3>
             <p className={runaUnlocked ? "text-[#ffd700] text-lg drop-shadow-[2px_2px_0_#000] mt-1 animate-pulse" : "text-[#a8e6cf] text-lg drop-shadow-[2px_2px_0_#000] mt-1"}>
                {runaUnlocked ? 'Em breve!' : 'Nível 10 req.'}
             </p>
           </div>
        </div>
      </main>

      {/* Footer Navigation */}
      <footer className="fixed bottom-0 left-0 right-0 p-4 z-20">
        <div className="max-w-md mx-auto bg-[#5c3a21] pixel-border px-8 py-3 flex justify-around items-center shadow-[0_-10px_20px_rgba(0,0,0,0.5)]">
          <button className="flex flex-col items-center gap-1 text-[#ffd700] drop-shadow-[2px_2px_0_#000] active:scale-95 transition-transform">
            <Home size={26} strokeWidth={2.5} />
            <span className="text-xl uppercase font-bold">Início</span>
          </button>
          
          <div className="w-1 h-8 bg-[#3d2412]"></div>
          
          <button className="flex flex-col items-center gap-1 text-[#9e9e9e] hover:text-white drop-shadow-[2px_2px_0_#000] active:scale-95 transition-all">
            <Trophy size={26} strokeWidth={2.5} />
            <span className="text-xl uppercase font-bold">Recordes</span>
          </button>
        </div>
      </footer>
    </div>
  );
}
