import re

with open('craft-match.html', 'r', encoding='utf-8') as f:
    content = f.read()

levels_replacement = """        const LEVELS = [
            { level: 1, moves: 18, targets: { 0: 10, 1: 10 }, desc: 'Colete 10 🪵 e 10 🪨' },
            { level: 2, moves: 20, targets: { 2: 15, 3: 10 }, desc: 'Colete 15 ⚙️ e 10 🪙' },
            { level: 3, moves: 18, targets: { 4: 10, 5: 10 }, desc: 'Colete 10 💎 e 10 🟢' },
            { level: 4, moves: 22, targets: { 2: 20, 4: 15 }, desc: 'Colete 20 ⚙️ e 15 💎' },
            { level: 5, moves: 25, targets: { 3: 20, 5: 20 }, desc: 'Colete 20 🪙 e 20 🟢' }
        ];"""

content = re.sub(
    r'const LEVELS = \[\s*\{[\s\S]*?\}\s*\];',
    levels_replacement,
    content
)

# Update checkWinLose to save level
win_logic_old = "if (won) {\n                SoundFX.win();\n                if (currentLevel < LEVELS.length - 1) {"
win_logic_new = "if (won) {\n                SoundFX.win();\n                let unlocked = parseInt(localStorage.getItem('craftMatchMaxLevel') || '1');\n                if (currentLevel + 2 > unlocked) localStorage.setItem('craftMatchMaxLevel', currentLevel + 2);\n                if (currentLevel < LEVELS.length - 1) {"
content = content.replace(win_logic_old, win_logic_new)

# In initGame, we don't start at currentLevel = 0 necessarily. Wait, for now the player can select level? No, they just go level by level. Let's start at the unlocked level!
init_logic_old = "let currentLevel = 0;"
init_logic_new = "let currentLevel = Math.min(4, parseInt(localStorage.getItem('craftMatchMaxLevel') || '1') - 1);"
content = content.replace(init_logic_old, init_logic_new)

with open('craft-match.html', 'w', encoding='utf-8') as f:
    f.write(content)
