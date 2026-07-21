import re

with open('potion-mix.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace HTML controls
old_html_controls = """<div class="controls-wrapper">
            <div class="d-pad">
                <div style="grid-column: 2; grid-row: 1;" class="control-btn" id="btn-up">▲</div>
                <div style="grid-column: 1; grid-row: 2;" class="control-btn" id="btn-left">◀</div>
                <div style="grid-column: 2; grid-row: 2;" class="control-btn" id="btn-down">▼</div>
                <div style="grid-column: 3; grid-row: 2;" class="control-btn" id="btn-right">▶</div>
            </div>
            <div class="action-pad">
                <div class="control-btn" id="btn-rotate" style="width: 90px; height: 90px; border-radius: 50%; background: #4caf50; font-size: 3rem; margin-top: 10px;">↻</div>
            </div>
        </div>"""

new_html_controls = """<div class="controls-wrapper" style="justify-content: flex-end;">
            <div class="action-pad">
                <div class="control-btn" id="btn-rotate" style="width: 90px; height: 90px; border-radius: 50%; background: #4caf50; font-size: 3rem; margin-top: 10px;">↻</div>
            </div>
        </div>"""

content = content.replace(old_html_controls, new_html_controls)

# Replace old touch logic
old_touch_start = "let touchStartX = 0;"
old_touch_end = "attachButton('btn-rotate', btnActions['btn-rotate'], false);"

# We need to use regex to replace from touchStartX to the end of button attaching
regex_pattern = r'let touchStartX = 0;[\s\S]*attachButton\(\'btn-rotate\', btnActions\[\'btn-rotate\'\], false\);'

new_touch_logic = """let dragStartX = 0;
        let dragStartY = 0;
        let lastDragX = 0;
        let lastDragY = 0;
        const DRAG_THRESHOLD_X = 25;
        const DRAG_THRESHOLD_Y = 25;

        canvas.addEventListener('touchstart', e => {
            if (isGameOver) return;
            dragStartX = e.touches[0].clientX;
            dragStartY = e.touches[0].clientY;
            lastDragX = dragStartX;
            lastDragY = dragStartY;
        }, {passive: false});

        canvas.addEventListener('touchmove', e => {
            if (isGameOver) return;
            e.preventDefault();
            const currentX = e.touches[0].clientX;
            const currentY = e.touches[0].clientY;

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
        }, {passive: false});
        
        // Desktop drag support
        let isMouseDown = false;
        canvas.addEventListener('mousedown', e => {
            if (isGameOver) return;
            isMouseDown = true;
            dragStartX = e.clientX;
            dragStartY = e.clientY;
            lastDragX = dragStartX;
            lastDragY = dragStartY;
        });
        
        window.addEventListener('mouseup', () => {
            isMouseDown = false;
        });
        
        canvas.addEventListener('mousemove', e => {
            if (isGameOver || !isMouseDown) return;
            
            const currentX = e.clientX;
            const currentY = e.clientY;

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

        const btnRotate = document.getElementById('btn-rotate');
        if (btnRotate) {
            btnRotate.addEventListener('touchstart', (e) => {
                if (e.cancelable) e.preventDefault();
                btnRotate.classList.add('active-btn');
                if(!isGameOver) playerRotate(1);
            }, {passive: false});
            const stopRotate = (e) => {
                if (e.cancelable) e.preventDefault();
                btnRotate.classList.remove('active-btn');
            };
            btnRotate.addEventListener('touchend', stopRotate, {passive: false});
            btnRotate.addEventListener('touchcancel', stopRotate, {passive: false});
            
            btnRotate.addEventListener('mousedown', (e) => {
                btnRotate.classList.add('active-btn');
                if(!isGameOver) playerRotate(1);
            });
            btnRotate.addEventListener('mouseup', () => btnRotate.classList.remove('active-btn'));
            btnRotate.addEventListener('mouseleave', () => btnRotate.classList.remove('active-btn'));
        }"""

content = re.sub(regex_pattern, new_touch_logic, content)

with open('potion-mix.html', 'w', encoding='utf-8') as f:
    f.write(content)
