import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

imports = "import { useState, useEffect } from 'react';\n" + content.replace("import { Settings", "import { Settings")

# Find default export
main_func = """
export default function App() {
  const [unlockedLevel, setUnlockedLevel] = useState(1);

  useEffect(() => {
    const level = parseInt(localStorage.getItem('craftMatchMaxLevel') || '1');
    setUnlockedLevel(level);
  }, []);

  const potionUnlocked = unlockedLevel >= 5;

"""

content = re.sub(
    r'export default function App\(\) \{\s*return \(',
    main_func + '  return (',
    imports
)

potion_locked_html = """{/* Locked Game: Poção Mix */}
        <div className="bg-[#7d7d7d] pixel-border p-5 flex items-center gap-5 opacity-80 grayscale-[50%] relative">
           <div className="w-14 h-14 bg-[#5c5c5c] pixel-border-sm flex items-center justify-center relative shrink-0">
              <Lock className="absolute top-1 right-1 text-black" size={12} />
              <FlaskConical size={28} className="text-[#a8e6cf]" />
           </div>
           <div className="flex-1">
             <h3 className="text-2xl font-bold text-white drop-shadow-[2px_2px_0_#000]">Poção Mix</h3>
             <p className="text-[#ff9a9e] text-lg drop-shadow-[2px_2px_0_#000] mt-1">Nível 5 req.</p>
           </div>
        </div>"""

potion_dynamic_html = """{/* Poção Mix */}
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
        </div>"""

content = content.replace(potion_locked_html, potion_dynamic_html)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
