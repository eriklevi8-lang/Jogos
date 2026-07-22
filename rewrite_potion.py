import re

html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Poção Mix</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0d0f1a;
            --panel-bg: rgba(255, 255, 255, 0.05);
            --border-color: rgba(255, 255, 255, 0.1);
            --accent: #ff007f;
            --text-main: #f0f0f0;
            --text-muted: #a0a0b0;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            touch-action: none;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: var(--bg-color);
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(76, 29, 149, 0.4), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(15, 118, 110, 0.4), transparent 25%);
            color: var(--text-main);
            overflow: hidden;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .game-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 500px;
            margin: 0 auto;
            width: 100%;
            padding: 1rem;
            gap: 1rem;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .back-btn {
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            backdrop-filter: blur(10px);
            border-radius: 50%;
            width: 44px; height: 44px;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: background 0.2s;
        }
        .back-btn:active { background: rgba(255,255,255,0.15); transform: scale(0.95); }

        .title {
            font-size: 1.8rem;
            font-weight: 800;
            background: linear-gradient(to right, #00f2fe 0%, #4facfe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .stats-panel {
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 1rem;
            backdrop-filter: blur(10px);
            display: flex;
            flex-direction: column;
            gap: 0.8rem;
        }

        .stats-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .stat-group {
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
        }

        .stat-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 1px;
        }

        .stat-value {
            font-size: 1.5rem;
            font-weight: 800;
        }

        .goal-container {
            width: 100%;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            height: 12px;
            position: relative;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }

        .goal-fill {
            position: absolute;
            top: 0; left: 0; height: 100%;
            background: linear-gradient(90deg, #ff0844 0%, #ffb199 100%);
            width: 0%;
            transition: width 0.3s ease;
            border-radius: 10px;
        }

        .goal-text {
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 600;
        }

        .board-wrapper {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        .game-board {
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            max-height: 100%;
            max-width: 100%;
            object-fit: contain;
        }

        /* Modal */
        .modal {
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(5px);
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
            z-index: 100;
        }
        .modal.visible { opacity: 1; pointer-events: auto; }
        
        .modal-content {
            background: var(--bg-color);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 2rem;
            text-align: center;
            max-width: 90%;
            width: 320px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }

        .modal h2 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(to right, #f83600 0%, #f9d423 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .modal p { color: var(--text-muted); margin-bottom: 1.5rem; }

        .primary-btn {
            background: white;
            color: black;
            border: none;
            padding: 1rem 2rem;
            font-size: 1.1rem;
            font-weight: 700;
            border-radius: 30px;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s;
        }
        .primary-btn:active { transform: scale(0.95); }
    </style>
</head>
<body>
    <div class="game-container">
        <header class="header">
            <button class="back-btn" onclick="goBack()">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
            <h1 class="title">Poção Mix</h1>
            <div style="width:44px"></div>
        </header>
        
        <div class="stats-panel">
            <div class="stats-row">
                <div class="stat-group">
                    <span class="stat-label">Nível</span>
                    <span class="stat-value" id="level">1</span>
                </div>
                <div class="stat-group" style="border-left: 1px solid var(--border-color); border-right: 1px solid var(--border-color);">
                    <span class="stat-label">Pontos</span>
                    <span class="stat-value" id="score">0</span>
                </div>
                <div class="stat-group">
                    <span class="stat-label">Linhas</span>
                    <span class="stat-value" id="lines">0</span>
                </div>
            </div>
            <div class="goal-text">
                <span>Progresso do Nível</span>
                <span id="goal-text">0 / 10</span>
            </div>
            <div class="goal-container">
                <div class="goal-fill" id="goal-fill"></div>
            </div>
        </div>

        <div class="board-wrapper">
            <canvas id="tetris" width="240" height="480" class="game-board"></canvas>
        </div>
    </div>

    <div id="modal" class="modal">
        <div class="modal-content">
            <h2 id="modal-title">Fim de Jogo</h2>
            <p id="modal-desc">Você fez 0 pontos.</p>
            <button class="primary-btn" onclick="initGame()">Jogar Novamente</button>
        </div>
    </div>

    <script>
        function goBack() {
            window.location.href = '/';
        }

        const SoundFX = {
            playTone: (freq, type, duration, vol=0.1) => {
                try {
                    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    osc.type = type;
                    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(freq/2, audioCtx.currentTime + duration);
                    
                    gain.gain.setValueAtTime(vol, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
                    
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    osc.start();
                    osc.stop(audioCtx.currentTime + duration);
                } catch(e) {}
            },
            move: () => SoundFX.playTone(400, 'sine', 0.1, 0.05),
            rotate: () => SoundFX.playTone(600, 'triangle', 0.1, 0.05),
            drop: () => SoundFX.playTone(200, 'square', 0.15, 0.1),
            clear: () => SoundFX.playTone(800, 'sine', 0.3, 0.2),
            levelUp: () => SoundFX.playTone(1200, 'triangle', 0.5, 0.2),
            gameover: () => SoundFX.playTone(150, 'sawtooth', 1.0, 0.3),
        };

        const canvas = document.getElementById('tetris');
        const ctx = canvas.getContext('2d');
        
        // Logical grid size: 10 cols, 20 rows
        const COLS = 10;
        const ROWS = 20;
        const BLOCK_SIZE = canvas.width / COLS;
        ctx.scale(BLOCK_SIZE, BLOCK_SIZE);

        function createMatrix(w, h) {
            const matrix = [];
            while (h--) {
                matrix.push(new Array(w).fill(0));
            }
            return matrix;
        }

        const arena = createMatrix(COLS, ROWS);

        function drawMatrix(matrix, offset, isGhost = false) {
            matrix.forEach((row, y) => {
                row.forEach((value, x) => {
                    if (value !== 0) {
                        ctx.fillStyle = colors[value];
                        if (isGhost) {
                            ctx.globalAlpha = 0.2;
                        }
                        
                        // Draw block with modern glowing/rounded style
                        const drawX = x + offset.x;
                        const drawY = y + offset.y;
                        
                        ctx.beginPath();
                        ctx.roundRect(drawX + 0.05, drawY + 0.05, 0.9, 0.9, 0.2);
                        ctx.fill();
                        
                        // Inner highlight
                        if (!isGhost) {
                            ctx.fillStyle = 'rgba(255,255,255,0.3)';
                            ctx.beginPath();
                            ctx.roundRect(drawX + 0.1, drawY + 0.1, 0.8, 0.3, 0.15);
                            ctx.fill();
                        }
                        
                        ctx.globalAlpha = 1.0;
                    }
                });
            });
        }

        function drawGrid() {
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.lineWidth = 0.02;
            for (let i = 0; i <= COLS; i++) {
                ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, ROWS); ctx.stroke();
            }
            for (let i = 0; i <= ROWS; i++) {
                ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(COLS, i); ctx.stroke();
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawGrid();
            drawMatrix(arena, {x: 0, y: 0});
            
            // Draw ghost piece
            const ghost = { matrix: player.matrix, pos: { x: player.pos.x, y: player.pos.y } };
            while (!collide(arena, ghost)) {
                ghost.pos.y++;
            }
            ghost.pos.y--;
            drawMatrix(ghost.matrix, ghost.pos, true);
            
            drawMatrix(player.matrix, player.pos);
        }

        function merge(arena, player) {
            player.matrix.forEach((row, y) => {
                row.forEach((value, x) => {
                    if (value !== 0) {
                        arena[y + player.pos.y][x + player.pos.x] = value;
                    }
                });
            });
        }

        function collide(arena, player) {
            const m = player.matrix;
            const o = player.pos;
            for (let y = 0; y < m.length; ++y) {
                for (let x = 0; x < m[y].length; ++x) {
                    if (m[y][x] !== 0 &&
                       (arena[y + o.y] && arena[y + o.y][x + o.x]) !== 0) {
                        return true;
                    }
                }
            }
            return false;
        }

        function rotate(matrix, dir) {
            for (let y = 0; y < matrix.length; ++y) {
                for (let x = 0; x < y; ++x) {
                    [matrix[x][y], matrix[y][x]] = [matrix[y][x], matrix[x][y]];
                }
            }
            if (dir > 0) {
                matrix.forEach(row => row.reverse());
            } else {
                matrix.reverse();
            }
        }

        function playerDrop() {
            player.pos.y++;
            if (collide(arena, player)) {
                player.pos.y--;
                merge(arena, player);
                playerReset();
                arenaSweep();
                updateScore();
                SoundFX.drop();
            }
            dropCounter = 0;
        }

        function playerMove(offset) {
            player.pos.x += offset;
            if (collide(arena, player)) {
                player.pos.x -= offset;
            } else {
                SoundFX.move();
            }
        }

        function playerRotate(dir) {
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
        }

        function createPiece(type) {
            if (type === 'T') return [[0,0,0],[1,1,1],[0,1,0]];
            if (type === 'O') return [[2,2],[2,2]];
            if (type === 'L') return [[0,3,0],[0,3,0],[0,3,3]];
            if (type === 'J') return [[0,4,0],[0,4,0],[4,4,0]];
            if (type === 'I') return [[0,5,0,0],[0,5,0,0],[0,5,0,0],[0,5,0,0]];
            if (type === 'S') return [[0,6,6],[6,6,0],[0,0,0]];
            if (type === 'Z') return [[7,7,0],[0,7,7],[0,0,0]];
        }

        const colors = [
            null,
            '#a855f7', // T - purple
            '#eab308', // O - yellow
            '#f97316', // L - orange
            '#3b82f6', // J - blue
            '#06b6d4', // I - cyan
            '#22c55e', // S - green
            '#ef4444'  // Z - red
        ];

        function playerReset() {
            const pieces = 'ILJOTSZ';
            player.matrix = createPiece(pieces[pieces.length * Math.random() | 0]);
            player.pos.y = 0;
            player.pos.x = (arena[0].length / 2 | 0) - (player.matrix[0].length / 2 | 0);
            
            if (collide(arena, player)) {
                SoundFX.gameover();
                document.getElementById('modal-desc').innerText = `Você fez ${player.score} pontos.`;
                document.getElementById('modal').classList.add('visible');
                isGameOver = true;
            }
        }

        function calculateLinesForNextLevel() {
            // Level 1: 10 lines
            // Level 2: +12 lines (22 total)
            // Starts increasing gradually
            return 10 + (player.level - 1) * 2;
        }

        function updateSpeed() {
            // Gradual speed increase
            // Base speed 1000ms, decreases by 10% each level, minimum 150ms
            dropInterval = Math.max(150, 1000 * Math.pow(0.9, player.level - 1));
        }

        function arenaSweep() {
            let rowCount = 1;
            let cleared = 0;
            outer: for (let y = arena.length - 1; y >= 0; --y) {
                for (let x = 0; x < arena[y].length; ++x) {
                    if (arena[y][x] === 0) continue outer;
                }
                const row = arena.splice(y, 1)[0].fill(0);
                arena.unshift(row);
                ++y;
                player.score += rowCount * 10;
                player.lines += 1;
                rowCount *= 2;
                cleared++;
            }
            if (cleared > 0) {
                const linesRequired = calculateLinesForNextLevel();
                player.levelLines += cleared;
                
                if (player.levelLines >= linesRequired) {
                    player.level++;
                    player.levelLines -= linesRequired;
                    SoundFX.levelUp();
                    updateSpeed();
                } else {
                    SoundFX.clear();
                }
            }
        }

        let dropCounter = 0;
        let dropInterval = 1000;
        let lastTime = 0;
        let isGameOver = false;

        function update(time = 0) {
            if (isGameOver) return;
            const deltaTime = time - lastTime;
            lastTime = time;
            dropCounter += deltaTime;
            if (dropCounter > dropInterval) {
                playerDrop();
            }
            draw();
            requestAnimationFrame(update);
        }

        function updateScore() {
            document.getElementById('score').innerText = player.score;
            document.getElementById('lines').innerText = player.lines;
            document.getElementById('level').innerText = player.level;
            
            const req = calculateLinesForNextLevel();
            document.getElementById('goal-text').innerText = `${player.levelLines} / ${req}`;
            document.getElementById('goal-fill').style.width = `${(player.levelLines / req) * 100}%`;
        }

        const player = {
            pos: {x: 0, y: 0},
            matrix: null,
            score: 0,
            lines: 0,
            level: 1,
            levelLines: 0
        };

        function initGame() {
            arena.forEach(row => row.fill(0));
            player.score = 0;
            player.lines = 0;
            player.level = 1;
            player.levelLines = 0;
            updateSpeed();
            isGameOver = false;
            document.getElementById('modal').classList.remove('visible');
            playerReset();
            updateScore();
            lastTime = performance.now();
            update();
        }

        // Improved Touch Controls
        let dragStartX = 0;
        let dragStartY = 0;
        let lastDragX = 0;
        let lastDragY = 0;
        let hasDragged = false;
        let activeTouchId = null;

        canvas.addEventListener('touchstart', e => {
            if (isGameOver || activeTouchId !== null) return;
            e.preventDefault();
            const touch = e.changedTouches[0];
            activeTouchId = touch.identifier;
            
            dragStartX = touch.clientX;
            dragStartY = touch.clientY;
            lastDragX = dragStartX;
            lastDragY = dragStartY;
            hasDragged = false;
        }, {passive: false});

        canvas.addEventListener('touchmove', e => {
            if (isGameOver || activeTouchId === null) return;
            e.preventDefault();
            
            let touch = null;
            for (let i = 0; i < e.changedTouches.length; i++) {
                if (e.changedTouches[i].identifier === activeTouchId) {
                    touch = e.changedTouches[i];
                    break;
                }
            }
            if (!touch) return;

            const currentX = touch.clientX;
            const currentY = touch.clientY;
            
            // Dynamic threshold based on actual canvas display width
            const rect = canvas.getBoundingClientRect();
            // Block size on screen
            const displayBlockSize = rect.width / COLS;
            
            // Sensitivity modifiers
            const moveThresholdX = displayBlockSize * 0.8; 
            const dropThresholdY = displayBlockSize * 0.8;

            if (Math.abs(currentX - dragStartX) > 10 || Math.abs(currentY - dragStartY) > 10) {
                hasDragged = true;
            }

            const dx = currentX - lastDragX;
            const dy = currentY - lastDragY;

            if (Math.abs(dx) > moveThresholdX) {
                const steps = Math.floor(Math.abs(dx) / moveThresholdX);
                const dir = dx > 0 ? 1 : -1;
                for (let s=0; s<steps; s++) playerMove(dir);
                lastDragX += dir * steps * moveThresholdX;
            }

            if (dy > dropThresholdY) {
                const steps = Math.floor(dy / dropThresholdY);
                for (let s=0; s<steps; s++) playerDrop();
                lastDragY += steps * dropThresholdY;
            }
            
            // Allow fast drop by swiping down hard
            if (dy > dropThresholdY * 3) {
                 while(!collide(arena, player)) {
                     player.pos.y++;
                 }
                 player.pos.y--;
                 playerDrop(); // force lock
                 lastDragY = currentY;
            }

        }, {passive: false});
        
        let lastTapTime = 0;
        canvas.addEventListener('touchend', e => {
            if (isGameOver) return;
            e.preventDefault();
            
            let touchFound = false;
            for (let i = 0; i < e.changedTouches.length; i++) {
                if (e.changedTouches[i].identifier === activeTouchId) {
                    touchFound = true;
                    break;
                }
            }
            if (!touchFound) return;
            activeTouchId = null;

            const now = performance.now();
            if (!hasDragged) {
                if (now - lastTapTime > 100) { // faster debounce for taps
                    playerRotate(1);
                    lastTapTime = now;
                }
            }
        }, {passive: false});

        canvas.addEventListener('touchcancel', e => {
            for (let i = 0; i < e.changedTouches.length; i++) {
                if (e.changedTouches[i].identifier === activeTouchId) {
                    activeTouchId = null;
                    break;
                }
            }
        }, {passive: false});

        // Desktop controls
        let isMouseDown = false;
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
            const now = performance.now();
            if (isMouseDown && !hasDragged && e.target === canvas) {
                if (now - lastTapTime > 100) {
                    playerRotate(1);
                    lastTapTime = now;
                }
            }
            isMouseDown = false;
        });
        
        canvas.addEventListener('mousemove', e => {
            if (isGameOver || !isMouseDown) return;
            
            const currentX = e.clientX;
            const currentY = e.clientY;
            
            const rect = canvas.getBoundingClientRect();
            const displayBlockSize = rect.width / COLS;
            const moveThresholdX = displayBlockSize * 0.8; 
            const dropThresholdY = displayBlockSize * 0.8;

            if (Math.abs(currentX - dragStartX) > 10 || Math.abs(currentY - dragStartY) > 10) {
                hasDragged = true;
            }

            const dx = currentX - lastDragX;
            const dy = currentY - lastDragY;

            if (Math.abs(dx) > moveThresholdX) {
                const steps = Math.floor(Math.abs(dx) / moveThresholdX);
                const dir = dx > 0 ? 1 : -1;
                for(let s=0; s<steps; s++) playerMove(dir);
                lastDragX += dir * steps * moveThresholdX;
            }

            if (dy > dropThresholdY) {
                const steps = Math.floor(dy / dropThresholdY);
                for(let s=0; s<steps; s++) playerDrop();
                lastDragY += steps * dropThresholdY;
            }
        });

        document.addEventListener('keydown', event => {
            if (isGameOver) return;
            if (event.keyCode === 37) playerMove(-1);
            else if (event.keyCode === 39) playerMove(1);
            else if (event.keyCode === 40) playerDrop();
            else if (event.keyCode === 38 || event.keyCode === 32) playerRotate(1);
        });

        initGame();
    </script>
</body>
</html>
