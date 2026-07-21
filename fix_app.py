import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add click state to App
main_func_old = """export default function App() {
  const [unlockedLevel, setUnlockedLevel] = useState(1);

  useEffect(() => {
    const level = parseInt(localStorage.getItem('craftMatchMaxLevel') || '1');
    setUnlockedLevel(level);
  }, []);

  const potionUnlocked = unlockedLevel >= 5;"""

main_func_new = """export default function App() {
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
  const runaUnlocked = unlockedLevel >= 10;"""

content = content.replace(main_func_old, main_func_new)

# Add onClick to Pickaxe container
header_old = """<div className="relative flex items-center justify-center w-12 h-12 bg-[#7d7d7d] pixel-border">
            <Pickaxe className="text-white" size={24} />
          </div>"""
header_new = """<div onClick={handleSecretUnlock} className="relative flex items-center justify-center w-12 h-12 bg-[#7d7d7d] pixel-border cursor-pointer active:scale-95 transition-transform">
            <Pickaxe className="text-white" size={24} />
          </div>"""

content = content.replace(header_old, header_new)

# Update Runa Master to use runaUnlocked dynamically
runa_old = """{/* Locked Game: Runa Master */}
        <div className="bg-[#7d7d7d] pixel-border p-5 flex items-center gap-5 opacity-80 grayscale-[50%] relative">
           <div className="w-14 h-14 bg-[#5c5c5c] pixel-border-sm flex items-center justify-center relative shrink-0">
              <Lock className="absolute top-1 right-1 text-black" size={12} />
              <Gem size={28} className="text-[#ffd700]" />
           </div>
           <div className="flex-1">
             <h3 className="text-2xl font-bold text-white drop-shadow-[2px_2px_0_#000]">Runa Master</h3>
             <p className="text-[#a8e6cf] text-lg drop-shadow-[2px_2px_0_#000] mt-1">Em breve...</p>
           </div>
        </div>"""

runa_new = """{/* Runa Master */}
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
        </div>"""

content = content.replace(runa_old, runa_new)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
