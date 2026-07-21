import re

with open('craft-match.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add click method to SoundFX
content = content.replace(
    "swap() { this.playTone(400, 'triangle', 0.1, 0.2); },",
    "click() { this.playTone(800, 'sine', 0.05, 0.1); },\n            swap() { this.playTone(400, 'triangle', 0.1, 0.2); },"
)

# Update goBack to play sound before navigating
content = content.replace(
    "function goBack() {\n            window.location.href = '/'; \n        }",
    "function goBack() {\n            SoundFX.click();\n            setTimeout(() => { window.location.href = '/'; }, 100);\n        }"
)

# Add SoundFX.click() to initGame wrapper for modal button
content = content.replace(
    "btn.onclick = callback;",
    "btn.onclick = () => { SoundFX.click(); callback(); };"
)

# Since the previous modal button (secondary-btn) directly calls goBack(),
# we already covered it by changing goBack(). 

with open('craft-match.html', 'w', encoding='utf-8') as f:
    f.write(content)
