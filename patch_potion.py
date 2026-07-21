import re

with open('potion-mix.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove controls-wrapper HTML
controls_html = """<div class="controls-wrapper" style="justify-content: flex-end;">
            <div class="action-pad">
                <div class="control-btn" id="btn-rotate" style="width: 90px; height: 90px; border-radius: 50%; background: #4caf50; font-size: 3rem; margin-top: 10px;">↻</div>
            </div>
        </div>"""
content = content.replace(controls_html, "")

# 2. Add grid drawing in JS
draw_old = """        function draw() {
            ctx.fillStyle = '#2b2b2b';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            drawMatrix(arena, {x: 0, y: 0});
            drawMatrix(player.matrix, player.pos);
        }"""

draw_new = """        function draw() {
            ctx.fillStyle = '#2b2b2b';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw grid
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.lineWidth = 0.05;
            for (let i = 0; i <= arena[0].length; i++) {
                ctx.beginPath();
                ctx.moveTo(i, 0);
                ctx.lineTo(i, arena.length);
                ctx.stroke();
            }
            for (let i = 0; i <= arena.length; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i);
                ctx.lineTo(arena[0].length, i);
                ctx.stroke();
            }

            drawMatrix(arena, {x: 0, y: 0});
            drawMatrix(player.matrix, player.pos);
        }"""
content = content.replace(draw_old, draw_new)

# 3. Update playerRotate to use a robust wall kick
rotate_old = """        function playerRotate(dir) {
            const pos = player.pos.x;
            let offset = 1;
            rotate(player.matrix, dir);
            while (collide(arena, player)) {
                player.pos.x += offset;
                offset = -(offset + (offset > 0 ? 1 : -1));
                if (offset > player.matrix[0].length) {
                    rotate(player.matrix, -dir);
                    player.pos.x = pos;
                    return;
                }
            }
            SoundFX.rotate();
        }"""

rotate_new = """        function playerRotate(dir) {
            const pos = player.pos.x;
            rotate(player.matrix, dir);
            
            const kicks = [1, -1, 2, -2, 3, -3];
            let i = 0;
            while (collide(arena, player)) {
                if (i >= kicks.length) {
                    rotate(player.matrix, -dir);
                    player.pos.x = pos;
                    return;
                }
                player.pos.x = pos + kicks[i];
                i++;
            }
            SoundFX.rotate();
        }"""
content = content.replace(rotate_old, rotate_new)

# 4. Remove btn-rotate event listeners
rotate_btn_js = r'const btnRotate = document\.getElementById.*?mouseleave\', \(\) => btnRotate\.classList\.remove\(\'active-btn\'\)\);\s*\}'
content = re.sub(rotate_btn_js, "", content, flags=re.DOTALL)

with open('potion-mix.html', 'w', encoding='utf-8') as f:
    f.write(content)
