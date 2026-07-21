import re

with open('potion-mix.html', 'r', encoding='utf-8') as f:
    content = f.read()

regex_pattern = r'let dragStartX = 0;[\s\S]*// Desktop drag support'

new_touch_logic = """let dragStartX = 0;
        let dragStartY = 0;
        let lastDragX = 0;
        let lastDragY = 0;
        let hasDragged = false;
        const DRAG_THRESHOLD_X = 25;
        const DRAG_THRESHOLD_Y = 25;

        canvas.addEventListener('touchstart', e => {
            if (isGameOver) return;
            dragStartX = e.touches[0].clientX;
            dragStartY = e.touches[0].clientY;
            lastDragX = dragStartX;
            lastDragY = dragStartY;
            hasDragged = false;
        }, {passive: false});

        canvas.addEventListener('touchmove', e => {
            if (isGameOver) return;
            e.preventDefault();
            const currentX = e.touches[0].clientX;
            const currentY = e.touches[0].clientY;

            const dx = currentX - lastDragX;
            const dy = currentY - lastDragY;

            if (Math.abs(currentX - dragStartX) > 10 || Math.abs(currentY - dragStartY) > 10) {
                hasDragged = true;
            }

            if (Math.abs(dx) > DRAG_THRESHOLD_X) {
                playerMove(dx > 0 ? 1 : -1);
                lastDragX = currentX;
            }

            if (dy > DRAG_THRESHOLD_Y) {
                playerDrop();
                lastDragY = currentY;
            }
        }, {passive: false});
        
        canvas.addEventListener('touchend', e => {
            if (isGameOver) return;
            if (!hasDragged) {
                playerRotate(1);
            }
        }, {passive: false});

        // Desktop drag support"""

content = re.sub(regex_pattern, new_touch_logic, content)

# Do the same for desktop mousedown/up
desktop_regex = r'let isMouseDown = false;[\s\S]*const btnRotate = document\.getElementById'

new_desktop_logic = """let isMouseDown = false;
        canvas.addEventListener('mousedown', e => {
            if (isGameOver) return;
            isMouseDown = true;
            dragStartX = e.clientX;
            dragStartY = e.clientY;
            lastDragX = dragStartX;
            lastDragY = dragStartY;
            hasDragged = false;
        });
        
        window.addEventListener('mouseup', (e) => {
            if (isGameOver) return;
            if (isMouseDown && !hasDragged && e.target === canvas) {
                playerRotate(1);
            }
            isMouseDown = false;
        });
        
        canvas.addEventListener('mousemove', e => {
            if (isGameOver || !isMouseDown) return;
            
            const currentX = e.clientX;
            const currentY = e.clientY;

            if (Math.abs(currentX - dragStartX) > 10 || Math.abs(currentY - dragStartY) > 10) {
                hasDragged = true;
            }

            const dx = currentX - lastDragX;
            const dy = currentY - lastDragY;

            if (Math.abs(dx) > DRAG_THRESHOLD_X) {
                playerMove(dx > 0 ? 1 : -1);
                lastDragX = currentX;
            }

            if (dy > DRAG_THRESHOLD_Y) {
                playerDrop();
                lastDragY = currentY;
            }
        });

        const btnRotate = document.getElementById"""

content = re.sub(desktop_regex, new_desktop_logic, content)

with open('potion-mix.html', 'w', encoding='utf-8') as f:
    f.write(content)
