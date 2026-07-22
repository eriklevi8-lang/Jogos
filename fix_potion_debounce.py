import re

with open('potion-mix.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix touchend
old_touchend = """        let lastTapTime = 0;
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

new_touchend = """        let lastTapTime = 0;
        canvas.addEventListener('touchend', e => {
            if (isGameOver) return;
            e.preventDefault(); // Prevent double triggering via simulated mouse events
            
            const now = performance.now();
            if (!hasDragged) {
                // simple debounce
                if (now - lastTapTime > 250) {
                    playerRotate(1);
                    lastTapTime = now;
                }
            }
        }, {passive: false});"""

content = content.replace(old_touchend, new_touchend)

# Fix mouseup
old_mouseup = """        window.addEventListener('mouseup', (e) => {
            if (isGameOver) return;
            if (isMouseDown && !hasDragged && e.target === canvas) {
                playerRotate(1);
            }
            isMouseDown = false;
        });"""

new_mouseup = """        window.addEventListener('mouseup', (e) => {
            if (isGameOver) return;
            const now = performance.now();
            if (isMouseDown && !hasDragged && e.target === canvas) {
                if (now - lastTapTime > 250) {
                    playerRotate(1);
                    lastTapTime = now;
                }
            }
            isMouseDown = false;
        });"""

content = content.replace(old_mouseup, new_mouseup)

with open('potion-mix.html', 'w', encoding='utf-8') as f:
    f.write(content)
