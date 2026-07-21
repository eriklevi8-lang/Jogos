import re

with open('potion-mix.html', 'r', encoding='utf-8') as f:
    content = f.read()

guard_code = """
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        // Guard against direct access
        const unlocked = parseInt(localStorage.getItem('craftMatchMaxLevel') || '1');
        if (unlocked < 5) {
            window.location.href = '/';
        }
"""

content = content.replace("const audioCtx = new (window.AudioContext || window.webkitAudioContext)();", guard_code)

with open('potion-mix.html', 'w', encoding='utf-8') as f:
    f.write(content)
