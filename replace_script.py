import re

with open('craft-match.html', 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#1a1a1a">
    <title>Craft Match</title>
    <link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet">
    <style>
        :root {
            --pixel-border: 4px;
            --color-dirt: #5c3a21;
            --color-dirt-light: #7a4f2e;
            --color-stone: #7d7d7d;
            --color-stone-light: #9e9e9e;
            --color-stone-dark: #5c5c5c;
            --color-grass: #4caf50;
            --color-grass-dark: #388e3c;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: 'VT323', monospace;
            background: #222;
            background-image: 
                linear-gradient(45deg, #1a1a1a 25%, transparent 25%, transparent 75%, #1a1a1a 75%, #1a1a1a),
                linear-gradient(45deg, #1a1a1a 25%, transparent 25%, transparent 75%, #1a1a1a 75%, #1a1a1a);
            background-size: 32px 32px;
            background-position: 0 0, 16px 16px;
            color: white;
            overflow: hidden;
            height: 100vh;
            display: flex;
            flex-direction: column;
            text-transform: uppercase;
        }

        /* Pixel borders helper */
        .pixel-box {
            background: var(--color-stone);
            border: var(--pixel-border) solid black;
            box-shadow: 
                inset calc(var(--pixel-border) * -1) calc(var(--pixel-border) * -1) 0px rgba(0,0,0,0.5),
                inset var(--pixel-border) var(--pixel-border) 0px rgba(255,255,255,0.4);
        }

        /* Top header */
        .game-header {
            padding: 1.5rem 1rem 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 20;
        }

        .title {
            font-size: 2.5rem;
            color: #ffd700;
            text-shadow: 3px 3px 0 #000;
            margin: 0;
        }

        .icon-btn {
            background: var(--color-stone);
            border: 3px solid black;
            box-shadow: 
                inset -3px -3px 0px rgba(0,0,0,0.5),
                inset 3px 3px 0px rgba(255,255,255,0.4);
            width: 48px; height: 48px;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: transform 0.1s;
        }
        .icon-btn:active { 
            transform: scale(0.95);
            box-shadow: 
                inset 3px 3px 0px rgba(0,0,0,0.5),
                inset -3px -3px 0px rgba(255,255,255,0.2);
        }

        .game-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 500px;
            margin: 0 auto;
            width: 100%;
            position: relative;
            z-index: 10;
        }

        .stats-board {
            display: flex;
            justify-content: space-around;
            padding: 1rem;
            margin: 0.5rem 1rem;
            align-items: center;
            image-rendering: pixelated;
        }
        
        .goal-box {
            flex: 2;
            align-items: flex-start;
            padding-right: 1rem;
        }
        .stat-box {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .stat-label { 
            font-size: 1.2rem; 
            color: #ddd; 
            text-shadow: 2px 2px 0 #000;
        }
        .stat-value { 
            font-size: 2rem; 
            color: white; 
            text-shadow: 2px 2px 0 #000;
        }
        
        .goal-text {
            font-size: 1.4rem;
            margin: 4px 0 8px;
            text-shadow: 2px 2px 0 #000;
        }

        .progress-bar {
            width: 100%;
            height: 16px;
            background: #000;
            border: 3px solid #5c5c5c;
            position: relative;
        }
        .progress-fill {
            height: 100%;
            width: 0%;
            background: var(--color-grass);
            box-shadow: inset 0 4px 0 var(--color-grass-dark);
            transition: width 0.3s ease;
        }

        .board-wrapper {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 1rem;
        }

        .game-board {
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            grid-template-rows: repeat(8, 1fr);
            gap: 2px;
            background: var(--color-dirt);
            border: 6px solid #3d2412;
            padding: 4px;
            box-shadow: 
                inset 6px 6px 0px rgba(0,0,0,0.6),
                inset -6px -6px 0px rgba(255,255,255,0.1),
                0 10px 20px rgba(0,0,0,0.8);
            width: 100%;
            max-width: 420px;
            aspect-ratio: 1;
            position: relative;
            touch-action: none;
        }

        .cell {
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.2);
            border: 1px solid rgba(0,0,0,0.3);
            border-bottom-color: rgba(255,255,255,0.1);
            border-right-color: rgba(255,255,255,0.1);
        }

        .piece {
            position: absolute;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: clamp(26px, 9vw, 40px);
            user-select: none;
            transition: transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1), top 0.25s cubic-bezier(0.2, 0.8, 0.2, 1), left 0.25s cubic-bezier(0.2, 0.8, 0.2, 1), opacity 0.2s ease;
            z-index: 10;
            cursor: pointer;
            filter: drop-shadow(2px 4px 0px rgba(0,0,0,0.6));
        }
        
        .piece.selected {
            transform: scale(1.15) translateY(-4px);
            filter: drop-shadow(0 0 8px rgba(255,255,255,0.8));
            z-index: 20;
        }
        .piece.combo {
            animation: pulseCombo 0.25s ease;
        }
        @keyframes pulseCombo {
            0% { transform: scale(1); }
            50% { transform: scale(1.4); opacity: 0.8; filter: brightness(1.5); }
            100% { transform: scale(0); opacity: 0; }
        }

        /* Specials */
        .special-badge {
            position: absolute;
            bottom: -5px;
            right: -5px;
            font-size: 18px;
            background: rgba(0,0,0,0.8);
            padding: 2px;
            border: 2px solid white;
            z-index: 20;
            line-height: 1;
            image-rendering: pixelated;
        }
        
        .piece[data-special="crafting_table"] { filter: drop-shadow(0 0 8px #ffd700); }
        .piece[data-special="pickaxe_row"] { filter: drop-shadow(0 0 8px #00ffaa); }
        .piece[data-special="pickaxe_col"] { filter: drop-shadow(0 0 8px #00ffaa); }
        .piece[data-special="enchanting_table"] { filter: drop-shadow(0 0 10px #9c27b0); }
        
        .piece[data-special="tnt"] {
            filter: drop-shadow(0 0 15px #ff5252);
            font-size: clamp(30px, 10vw, 44px);
            animation: tntPulse 1s infinite alternate;
        }
        @keyframes tntPulse {
            0% { filter: drop-shadow(0 0 10px #ff5252) brightness(1); }
            100% { filter: drop-shadow(0 0 20px #ff0000) brightness(1.5); transform: scale(1.05); }
        }

        .explosion {
            position: absolute;
            width: 80px;
            height: 80px;
            background: radial-gradient(circle, #fff 10%, #ffeb3b 30%, #ff5252 60%, transparent 80%);
            border-radius: 20%;
            transform: translate(-50%, -50%) scale(0);
            animation: explodeAnim 0.3s ease-out forwards;
            pointer-events: none;
            z-index: 50;
            mix-blend-mode: screen;
            image-rendering: pixelated;
        }
        @keyframes explodeAnim {
            0% { transform: translate(-50%, -50%) scale(0.5); opacity: 1; }
            50% { opacity: 1; }
            100% { transform: translate(-50%, -50%) scale(2.5); opacity: 0; }
        }

        .shake {
            animation: shakeAnim 0.3s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
        }
        @keyframes shakeAnim {
            10%, 90% { transform: translate3d(-4px, 0, 0); }
            20%, 80% { transform: translate3d(5px, 0, 0); }
            30%, 50%, 70% { transform: translate3d(-8px, 0, 0); }
            40%, 60% { transform: translate3d(8px, 0, 0); }
        }

        /* Modal */
        .modal {
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.85);
            z-index: 100;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease;
        }
        .modal.visible {
            opacity: 1;
            pointer-events: auto;
        }
        .modal-content {
            background: var(--color-stone);
            border: 6px solid black;
            box-shadow: 
                inset -6px -6px 0px rgba(0,0,0,0.5),
                inset 6px 6px 0px rgba(255,255,255,0.4),
                0 10px 40px rgba(0,0,0,1);
            padding: 2.5rem 2rem;
            text-align: center;
            max-width: 90%;
            width: 360px;
            transform: scale(0.9) translateY(20px);
            transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        .modal.visible .modal-content {
            transform: scale(1) translateY(0);
        }
        .modal-content h2 {
            font-size: 3rem;
            margin-bottom: 1rem;
            color: #ffd700;
            text-shadow: 3px 3px 0 #000;
        }
        .modal-content p {
            font-size: 1.5rem;
            margin-bottom: 2rem;
            color: white;
            text-shadow: 2px 2px 0 #000;
        }

        .primary-btn {
            background: var(--color-grass);
            color: white;
            font-family: 'VT323', monospace;
            font-size: 1.8rem;
            padding: 0.8rem 2rem;
            border: 4px solid black;
            box-shadow: 
                inset -4px -4px 0px rgba(0,0,0,0.5),
                inset 4px 4px 0px rgba(255,255,255,0.4);
            cursor: pointer;
            text-transform: uppercase;
            width: 100%;
        }
        .primary-btn:active { 
            background: var(--color-grass-dark);
            box-shadow: 
                inset 4px 4px 0px rgba(0,0,0,0.5),
                inset -4px -4px 0px rgba(255,255,255,0.2);
        }

        .secondary-btn {
            background: var(--color-dirt);
            color: white;
            font-family: 'VT323', monospace;
            font-size: 1.5rem;
            padding: 0.8rem 2rem;
            border: 4px solid black;
            box-shadow: 
                inset -4px -4px 0px rgba(0,0,0,0.5),
                inset 4px 4px 0px rgba(255,255,255,0.4);
            cursor: pointer;
            text-transform: uppercase;
            width: 100%;
            margin-top: 1rem;
        }
        .secondary-btn:active { 
            background: var(--color-dirt-light);
            box-shadow: 
                inset 4px 4px 0px rgba(0,0,0,0.5),
                inset -4px -4px 0px rgba(255,255,255,0.2);
        }

        @keyframes floatUp { 
            0% { top: 40%; opacity: 1; transform: translate(-50%, 0) scale(0.8); } 
            50% { transform: translate(-50%, -20px) scale(1.2); }
            100% { top: 20%; opacity: 0; transform: translate(-50%, -40px) scale(1); } 
        }
    </style>
</head>
<body>
    <div class="game-container">
        <header class="game-header">
            <button class="icon-btn" onclick="goBack()">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none"><path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="4" stroke-linecap="square" stroke-linejoin="miter"/></svg>
            </button>
            <div class="header-center text-center">
                <h1 class="title" id="level-title">Nível 1</h1>
            </div>
            <div style="width:48px"></div>
        </header>
        
        <div class="stats-board pixel-box">
            <div class="stat-box goal-box">
                <span class="stat-label">Meta</span>
                <span class="stat-value goal-text" id="goal-desc">Colete 10 🪵 e 10 🪨</span>
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill"></div>
                </div>
            </div>
            <div class="stat-box">
                <span class="stat-label">Movs</span>
                <span class="stat-value" id="moves">18</span>
            </div>
        </div>

        <div class="board-wrapper">
            <div id="board" class="game-board"></div>
        </div>
    </div>
    
    <div id="modal" class="modal">
        <div class="modal-content">
            <h2 id="modal-title">Vitória!</h2>
            <p id="modal-desc">Você completou o desafio.</p>
            <button class="primary-btn mt-4" id="modal-btn" onclick="initGame()">Jogar Novamente</button>
            <button class="secondary-btn mt-3" onclick="goBack()">Voltar ao Portal</button>
        </div>
    </div>

    <script>
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const SoundFX = {
            init() {
                if(audioCtx.state === 'suspended') {
                    // Ignore promise warning
                    audioCtx.resume().catch(()=>{});
                }
            },
            playTone(freq, type, duration, vol=0.1) {
                try {
                    this.init();
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    osc.type = type;
                    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                    gain.gain.setValueAtTime(vol, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    osc.start();
                    osc.stop(audioCtx.currentTime + duration);
                } catch(e){}
            },
            playNoise(duration, vol=0.2) {
                try {
                    this.init();
                    const bufferSize = audioCtx.sampleRate * duration;
                    const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
                    const data = buffer.getChannelData(0);
                    for(let i=0; i<bufferSize; i++) data[i] = Math.random() * 2 - 1;
                    const noise = audioCtx.createBufferSource();
                    noise.buffer = buffer;
                    const gain = audioCtx.createGain();
                    gain.gain.setValueAtTime(vol, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
                    
                    const filter = audioCtx.createBiquadFilter();
                    filter.type = 'lowpass';
                    filter.frequency.value = 1000;
                    noise.connect(filter);
                    filter.connect(gain);
                    gain.connect(audioCtx.destination);
                    noise.start();
                } catch(e){}
            },
            swap() { this.playTone(400, 'triangle', 0.1, 0.2); },
            match() { 
                this.playTone(600, 'square', 0.1, 0.1); 
                setTimeout(()=>this.playTone(800, 'square', 0.15, 0.1), 100); 
            },
            combo(level) { this.playTone(600 + level*100, 'square', 0.2, 0.15); },
            explosion() { this.playNoise(0.4, 0.4); this.playTone(150, 'sawtooth', 0.4, 0.2); },
            tnt() { this.playNoise(0.8, 0.6); this.playTone(100, 'sawtooth', 0.8, 0.4); },
            win() {
                this.playTone(400, 'square', 0.2, 0.1);
                setTimeout(()=>this.playTone(500, 'square', 0.2, 0.1), 200);
                setTimeout(()=>this.playTone(600, 'square', 0.4, 0.1), 400);
            }
        };

        const ROWS = 8;
        const COLS = 8;
        // 0: Madeira, 1: Pedra, 2: Ferro, 3: Ouro, 4: Diamante, 5: Esmeralda
        const ICONS = ['🪵', '🪨', '⚙️', '🪙', '💎', '🟢'];

        const LEVELS = [
            {
                level: 1,
                moves: 18,
                targets: { 0: 10, 1: 10 }, 
                desc: 'Colete 10 🪵 e 10 🪨'
            },
            {
                level: 2,
                moves: 20,
                targets: { 2: 15, 3: 10 },
                desc: 'Colete 15 ⚙️ e 10 🪙'
            },
            {
                level: 3,
                moves: 18,
                targets: { 4: 10, 5: 10 },
                desc: 'Colete 10 💎 e 10 🟢'
            }
        ];
        
        let currentLevel = 0;
        let collected = {};
        
        let board = []; 
        let score = 0;
        let moves = 20;
        let selected = null;
        let isAnimating = false;
        let pieceIdCounter = 0;

        const boardElem = document.getElementById('board');
        const movesElem = document.getElementById('moves');

        function goBack() {
            window.location.href = '/'; 
        }

        function triggerShake() {
            boardElem.classList.remove('shake');
            void boardElem.offsetWidth;
            boardElem.classList.add('shake');
        }

        function createExplosion(r, c) {
            const pad = 4;
            const gap = 2;
            let width = boardElem.getBoundingClientRect().width;
            let cW = (width - pad*2 - gap*7)/8;
            
            const x = c * cW + c*gap + pad + cW/2;
            const y = r * cW + r*gap + pad + cW/2;
            
            const particle = document.createElement('div');
            particle.className = 'explosion';
            particle.style.left = `${x}px`;
            particle.style.top = `${y}px`;
            boardElem.appendChild(particle);
            
            setTimeout(() => particle.remove(), 300);
        }

        function initGame() {
            let levelData = LEVELS[currentLevel];
            score = 0;
            moves = levelData.moves;
            collected = {};
            
            updateUI();
            document.getElementById('modal').classList.remove('visible');
            boardElem.innerHTML = '';
            
            board = [];
            for(let r=0; r<ROWS; r++){
                board[r] = [];
                for(let c=0; c<COLS; c++){
                    let type;
                    do {
                        type = Math.floor(Math.random() * ICONS.length);
                    } while (
                        (r >= 2 && board[r-1][c] && board[r-2][c] && board[r-1][c].type === type && board[r-2][c].type === type) ||
                        (c >= 2 && board[r][c-1] && board[r][c-2] && board[r][c-1].type === type && board[r][c-2].type === type)
                    );
                    
                    const cell = document.createElement('div');
                    cell.className = 'cell';
                    boardElem.appendChild(cell);
                    
                    board[r][c] = {
                        type: type,
                        special: 'none',
                        id: pieceIdCounter++,
                        r: r, c: c
                    };
                }
            }
            drawBoard();
        }

        function getPieceElem(id) {
            return document.getElementById(`piece-${id}`);
        }

        function drawBoard() {
            boardElem.querySelectorAll('.piece').forEach(p => p.remove());
            for(let r=0; r<ROWS; r++){
                for(let c=0; c<COLS; c++){
                    if(board[r][c]) createPieceElement(board[r][c]);
                }
            }
        }

        function createPieceElement(pieceData) {
            const p = document.createElement('div');
            p.className = 'piece';
            p.id = `piece-${pieceData.id}`;
            
            let html = pieceData.special === 'tnt' ? '🧨' : ICONS[pieceData.type];
            if (pieceData.special === 'crafting_table') html += `<div class="special-badge" style="border-color:#ffd700">🛠️</div>`;
            else if (pieceData.special === 'pickaxe_row' || pieceData.special === 'pickaxe_col') html += `<div class="special-badge" style="border-color:#00ffaa">⛏️</div>`;
            else if (pieceData.special === 'enchanting_table') html += `<div class="special-badge" style="border-color:#9c27b0">🔮</div>`;
            p.innerHTML = html;
            
            if (pieceData.special !== 'none') p.dataset.special = pieceData.special;
            
            updatePiecePos(p, pieceData.r, pieceData.c);
            
            boardElem.appendChild(p);
        }

        function updatePiecePos(elem, r, c) {
            if(!elem) return;
            const pad = 4;
            const gap = 2;
            elem.style.width = `calc((100% - ${gap * (COLS-1)}px) / ${COLS})`;
            elem.style.height = `calc((100% - ${gap * (ROWS-1)}px) / ${ROWS})`;
            elem.style.top = `calc(${r} * ((100% - ${gap * (ROWS-1)}px) / ${ROWS}) + ${r * gap}px + ${pad}px)`;
            elem.style.left = `calc(${c} * ((100% - ${gap * (COLS-1)}px) / ${COLS}) + ${c * gap}px + ${pad}px)`;
        }

        let touchStartX = 0;
        let touchStartY = 0;
        let touchStartPiece = null;

        boardElem.addEventListener('touchstart', (e) => {
            if(isAnimating) return;
            SoundFX.init();
            const touch = e.touches[0];
            touchStartX = touch.clientX;
            touchStartY = touch.clientY;
            
            const rect = boardElem.getBoundingClientRect();
            const pad = 4;
            const x = touchStartX - rect.left - pad;
            const y = touchStartY - rect.top - pad;
            const cWidth = (rect.width - pad*2) / COLS;
            const cHeight = (rect.height - pad*2) / ROWS;
            const c = Math.floor(x / cWidth);
            const r = Math.floor(y / cHeight);
            
            if(r >= 0 && r < ROWS && c >= 0 && c < COLS) {
                touchStartPiece = {r, c};
            }
        }, {passive: false});

        boardElem.addEventListener('touchmove', (e) => {
            e.preventDefault();
            if(isAnimating || !touchStartPiece) return;
            
            const touch = e.touches[0];
            const dx = touch.clientX - touchStartX;
            const dy = touch.clientY - touchStartY;
            
            if (Math.abs(dx) > 30 || Math.abs(dy) > 30) {
                let tr = touchStartPiece.r, tc = touchStartPiece.c;
                if (Math.abs(dx) > Math.abs(dy)) {
                    if (dx > 0) tc++; else tc--;
                } else {
                    if (dy > 0) tr++; else tr--;
                }
                
                if (tr>=0 && tr<ROWS && tc>=0 && tc<COLS) {
                    let sp = touchStartPiece;
                    touchStartPiece = null;
                    if(selected) {
                        let selEl = getPieceElem(board[selected.r][selected.c].id);
                        if(selEl) selEl.classList.remove('selected');
                        selected = null;
                    }
                    trySwap(sp.r, sp.c, tr, tc);
                } else {
                    touchStartPiece = null;
                }
            }
        }, {passive: false});

        boardElem.addEventListener('touchend', (e) => {
            if(isAnimating || !touchStartPiece) return;
            handleInteract(touchStartPiece.r, touchStartPiece.c);
            touchStartPiece = null;
        });
        
        boardElem.addEventListener('mousedown', (e) => {
            if(isAnimating) return;
            SoundFX.init();
            const rect = boardElem.getBoundingClientRect();
            const pad = 4;
            const x = e.clientX - rect.left - pad;
            const y = e.clientY - rect.top - pad;
            const cWidth = (rect.width - pad*2) / COLS;
            const cHeight = (rect.height - pad*2) / ROWS;
            const c = Math.floor(x / cWidth);
            const r = Math.floor(y / cHeight);
            if(r >= 0 && r < ROWS && c >= 0 && c < COLS) {
                handleInteract(r, c);
            }
        });

        async function handleInteract(r, c) {
            if (isAnimating) return;
            if (!selected) {
                selected = {r, c};
                let el = getPieceElem(board[r][c].id);
                if(el) {
                    el.classList.add('selected');
                    SoundFX.playTone(300, 'triangle', 0.05, 0.1);
                }
            } else {
                const sr = selected.r, sc = selected.c;
                let selEl = getPieceElem(board[sr][sc].id);
                if(selEl) selEl.classList.remove('selected');
                
                const isAdj = Math.abs(sr - r) + Math.abs(sc - c) === 1;
                if (sr === r && sc === c) {
                    selected = null;
                } else if (isAdj) {
                    selected = null;
                    await trySwap(sr, sc, r, c);
                } else {
                    selected = {r, c};
                    let el = getPieceElem(board[r][c].id);
                    if(el) {
                        el.classList.add('selected');
                        SoundFX.playTone(300, 'triangle', 0.05, 0.1);
                    }
                }
            }
        }

        async function trySwap(r1, c1, r2, c2) {
            isAnimating = true;
            SoundFX.swap();
            
            let p1 = board[r1][c1];
            let p2 = board[r2][c2];
            
            board[r1][c1] = p2;
            board[r2][c2] = p1;
            p1.r = r2; p1.c = c2;
            p2.r = r1; p2.c = c1;
            
            updatePiecePos(getPieceElem(p1.id), p1.r, p1.c);
            updatePiecePos(getPieceElem(p2.id), p2.r, p2.c);
            
            await sleep(250);
            
            let isColorBomb = p1.special === 'tnt' || p2.special === 'tnt';
            let matchData = findMatches();
            
            if (matchData.hMatches.length > 0 || matchData.vMatches.length > 0 || matchData.squares.length > 0 || isColorBomb) {
                moves--;
                updateUI();
                
                if(isColorBomb) {
                    let bomb = p1.special === 'tnt' ? p1 : p2;
                    let target = p1.special === 'tnt' ? p2 : p1;
                    
                    if (p1.special === 'tnt' && p2.special === 'tnt') {
                        let all = [];
                        for(let r=0; r<ROWS; r++) for(let c=0; c<COLS; c++) all.push({r,c});
                        await processDestruction(all);
                    } else {
                        let toDestroy = [{r: bomb.r, c: bomb.c}];
                        let tType = target.type >= 0 ? target.type : Math.floor(Math.random()*ICONS.length);
                        for(let r=0; r<ROWS; r++){
                            for(let c=0; c<COLS; c++){
                                if(board[r][c] && board[r][c].type === tType) toDestroy.push({r, c});
                            }
                        }
                        toDestroy.push({r: target.r, c: target.c});
                        await processDestruction(toDestroy);
                    }
                    
                    await applyGravity();
                    await processMatchesSeq(null, 2);
                } else {
                    await processMatchesSeq([{r: r1, c: c1}, {r: r2, c: c2}], 1);
                }
            } else {
                // Revert
                board[r1][c1] = p1;
                board[r2][c2] = p2;
                p1.r = r1; p1.c = c1;
                p2.r = r2; p2.c = c2;
                updatePiecePos(getPieceElem(p1.id), p1.r, p1.c);
                updatePiecePos(getPieceElem(p2.id), p2.r, p2.c);
                await sleep(250);
            }
            
            isAnimating = false;
            checkWinLose();
        }

        function findMatches() {
            let matchCells = new Set();
            let squares = [];
            let hMatches = [];
            let vMatches = [];

            // Horizontal
            for (let r = 0; r < ROWS; r++) {
                for (let c = 0; c < COLS - 2; c++) {
                    if (board[r][c] && board[r][c].type !== -1) {
                        let matchLen = 1;
                        while (c + matchLen < COLS && board[r][c + matchLen] && board[r][c + matchLen].type === board[r][c].type) matchLen++;
                        if (matchLen >= 3) {
                            let group = [];
                            for (let i = 0; i < matchLen; i++) group.push({ r, c: c + i });
                            hMatches.push(group);
                            group.forEach(p => matchCells.add(`${p.r},${p.c}`));
                            c += matchLen - 1;
                        }
                    }
                }
            }

            // Vertical
            for (let c = 0; c < COLS; c++) {
                for (let r = 0; r < ROWS - 2; r++) {
                    if (board[r][c] && board[r][c].type !== -1) {
                        let matchLen = 1;
                        while (r + matchLen < ROWS && board[r + matchLen][c] && board[r + matchLen][c].type === board[r][c].type) matchLen++;
                        if (matchLen >= 3) {
                            let group = [];
                            for (let i = 0; i < matchLen; i++) group.push({ r: r + i, c });
                            vMatches.push(group);
                            group.forEach(p => matchCells.add(`${p.r},${p.c}`));
                            r += matchLen - 1;
                        }
                    }
                }
            }

            // 2x2 Squares
            for (let r = 0; r < ROWS - 1; r++) {
                for (let c = 0; c < COLS - 1; c++) {
                    let p1 = board[r][c];
                    if (p1 && p1.type !== -1) {
                        if (
                            board[r][c+1] && board[r][c+1].type === p1.type &&
                            board[r+1][c] && board[r+1][c].type === p1.type &&
                            board[r+1][c+1] && board[r+1][c+1].type === p1.type
                        ) {
                            let group = [{r,c}, {r,c:c+1}, {r:r+1,c}, {r:r+1,c:c+1}];
                            squares.push(group);
                            group.forEach(p => matchCells.add(`${p.r},${p.c}`));
                        }
                    }
                }
            }

            return { hMatches, vMatches, squares, matchCells };
        }

        async function processDestruction(initialList) {
            let toDestroy = new Set();
            let queue = [...initialList];
            let cellsDestroyed = 0;
            let hadSpecial = false;
            let hadTNT = false;
            
            while(queue.length > 0) {
                let p = queue.shift();
                let key = `${p.r},${p.c}`;
                if (!toDestroy.has(key)) {
                    let piece = board[p.r][p.c];
                    if (piece) {
                        toDestroy.add(key);
                        if (piece.special === 'pickaxe_row') {
                            for(let c=0; c<COLS; c++) queue.push({r: p.r, c: c});
                            hadSpecial = true;
                        } else if (piece.special === 'pickaxe_col') {
                            for(let r=0; r<ROWS; r++) queue.push({r: r, c: p.c});
                            hadSpecial = true;
                        } else if (piece.special === 'enchanting_table') {
                            for(let r=p.r-1; r<=p.r+1; r++) {
                                for(let c=p.c-1; c<=p.c+1; c++) {
                                    if (r>=0 && r<ROWS && c>=0 && c<COLS) queue.push({r, c});
                                }
                            }
                            hadSpecial = true;
                        } else if (piece.special === 'crafting_table') {
                            if (p.r-1 >= 0) queue.push({r: p.r-1, c: p.c});
                            if (p.r+1 < ROWS) queue.push({r: p.r+1, c: p.c});
                            if (p.c-1 >= 0) queue.push({r: p.r, c: p.c-1});
                            if (p.c+1 < COLS) queue.push({r: p.r, c: p.c+1});
                            hadSpecial = true;
                        } else if (piece.special === 'tnt') {
                            let types = [0,1,2,3,4,5];
                            let rType = types[Math.floor(Math.random() * types.length)];
                            for(let r=0; r<ROWS; r++) {
                                for(let c=0; c<COLS; c++) {
                                    if(board[r][c] && board[r][c].type === rType) queue.push({r, c});
                                }
                            }
                            hadSpecial = true;
                            hadTNT = true;
                        }
                    }
                }
            }
            
            let destroyArr = Array.from(toDestroy).map(s => {
                let [r,c] = s.split(',').map(Number);
                return {r,c};
            });
            
            destroyArr.forEach(p => {
                let piece = board[p.r][p.c];
                if (piece && piece.type >= 0) {
                    collected[piece.type] = (collected[piece.type] || 0) + 1;
                }
            });

            cellsDestroyed = destroyArr.length;
            score += cellsDestroyed * 10;
            
            if (hadTNT) SoundFX.tnt();
            else if (hadSpecial || cellsDestroyed > 5) SoundFX.explosion();
            else if (cellsDestroyed > 0) SoundFX.match();
            
            if (cellsDestroyed > 6) triggerShake();
            
            await destroyPiecesView(destroyArr);
            return cellsDestroyed;
        }

        async function destroyPiecesView(list) {
            list.forEach(p => {
                let piece = board[p.r][p.c];
                if (piece) {
                    let elem = getPieceElem(piece.id);
                    if(elem) {
                        elem.classList.add('combo');
                        createExplosion(p.r, p.c);
                        setTimeout(() => elem.remove(), 250);
                    }
                    board[p.r][p.c] = null;
                }
            });
            if(list.length > 0) await sleep(250);
        }

        async function processMatchesSeq(swapTarget, combo) {
            let { matchCells, squares } = findMatches();
            if (matchCells.size === 0) return;
            
            if(combo > 1) SoundFX.combo(combo);
            
            let cellsByCluster = [];
            let visited = new Set();
            let cellToType = {};
            let allCells = Array.from(matchCells).map(str => {
                let [r,c] = str.split(',').map(Number);
                cellToType[str] = board[r][c].type;
                return {r, c, str};
            });

            allCells.forEach(cell => {
                if (!visited.has(cell.str)) {
                    let cluster = [];
                    let q = [cell];
                    visited.add(cell.str);
                    while(q.length > 0) {
                        let curr = q.shift();
                        cluster.push(curr);
                        allCells.forEach(n => {
                            if (!visited.has(n.str) && cellToType[n.str] === cellToType[curr.str]) {
                                if (Math.abs(n.r - curr.r) + Math.abs(n.c - curr.c) === 1) {
                                    visited.add(n.str);
                                    q.push(n);
                                }
                            }
                        });
                    }
                    cellsByCluster.push(cluster);
                }
            });

            let specialToCreate = [];
            cellsByCluster.forEach(cluster => {
                let rows = new Set(cluster.map(c => c.r));
                let cols = new Set(cluster.map(c => c.c));
                let maxInRow = 0, maxInCol = 0;
                rows.forEach(r => {
                    let cnt = cluster.filter(c => c.r === r).length;
                    if (cnt > maxInRow) maxInRow = cnt;
                });
                cols.forEach(c => {
                    let cnt = cluster.filter(c => c.c === c).length;
                    if (cnt > maxInCol) maxInCol = cnt;
                });
                
                let has2x2 = squares.some(sq => sq.every(p => cluster.some(c => c.r === p.r && c.c === p.c)));
                
                let specialType = 'none';
                if (maxInRow >= 5 || maxInCol >= 5) specialType = 'tnt';
                else if (maxInRow >= 3 && maxInCol >= 3) specialType = 'enchanting_table';
                else if (maxInRow === 4) specialType = 'pickaxe_row';
                else if (maxInCol === 4) specialType = 'pickaxe_col';
                else if (has2x2) specialType = 'crafting_table';
                
                if (specialType !== 'none') {
                    let bestCell = cluster[0];
                    if (swapTarget) {
                        let found = cluster.find(c => swapTarget.some(st => st.r === c.r && st.c === c.c));
                        if (found) bestCell = found;
                    }
                    if ((specialType === 'enchanting_table' || specialType === 'crafting_table') && (!swapTarget || !swapTarget.some(st => st.r === bestCell.r && st.c === bestCell.c))) {
                        let intersect = cluster.find(c => cluster.filter(x => x.r === c.r).length >= 3 && cluster.filter(x => x.c === c.c).length >= 3);
                        if (intersect) bestCell = intersect;
                        else if (has2x2) {
                             let sq = squares.find(s => s.every(p => cluster.some(cl => cl.r===p.r && cl.c===p.c)));
                             if (sq) bestCell = sq[0];
                        }
                    }
                    specialToCreate.push({r: bestCell.r, c: bestCell.c, type: cellToType[bestCell.str], special: specialType});
                }
            });

            let destroyList = allCells.map(c => ({r: c.r, c: c.c}));
            specialToCreate.forEach(sp => {
                destroyList = destroyList.filter(d => !(d.r === sp.r && d.c === sp.c));
            });

            let destroyedCount = await processDestruction(destroyList);
            
            if (combo > 1 && destroyedCount > 0) {
                let texts = ["Combo!", "Mágico!", "Crafting!", "Boom!"];
                showFloatingText(texts[Math.floor(Math.random() * texts.length)]);
            }

            specialToCreate.forEach(sp => {
                if(board[sp.r][sp.c]) {
                    let el = getPieceElem(board[sp.r][sp.c].id);
                    if(el) el.remove();
                }
                let pType = sp.special === 'tnt' ? -1 : sp.type;
                let p = {
                    type: pType,
                    special: sp.special,
                    id: pieceIdCounter++,
                    r: sp.r, c: sp.c
                };
                board[sp.r][sp.c] = p;
                createPieceElement(p);
            });

            updateUI();
            await applyGravity();
            
            let { matchCells: mc2 } = findMatches();
            if (mc2.size > 0) {
                await processMatchesSeq(null, combo + 1);
            }
        }

        async function applyGravity() {
            let moved = false;
            for(let c=0; c<COLS; c++){
                for(let r=ROWS-1; r>=0; r--){
                    if (board[r][c] === null) {
                        for(let k=r-1; k>=0; k--){
                            if (board[k][c] !== null) {
                                board[r][c] = board[k][c];
                                board[k][c] = null;
                                board[r][c].r = r;
                                let elem = getPieceElem(board[r][c].id);
                                if(elem) updatePiecePos(elem, r, c);
                                moved = true;
                                break;
                            }
                        }
                    }
                }
            }
            for(let c=0; c<COLS; c++){
                for(let r=0; r<ROWS; r++){
                    if (board[r][c] === null) {
                        let p = {
                            type: Math.floor(Math.random() * ICONS.length),
                            special: 'none',
                            id: pieceIdCounter++,
                            r: r, c: c
                        };
                        board[r][c] = p;
                        
                        createPieceElement(p);
                        let elem = getPieceElem(p.id);
                        
                        const pad = 4;
                        const gap = 2;
                        elem.style.top = `calc(${(r - ROWS)} * ((100% - ${gap * (ROWS-1)}px) / ${ROWS}) - 50px)`;
                        
                        elem.getBoundingClientRect(); // reflow
                        updatePiecePos(elem, r, c);
                        moved = true;
                    }
                }
            }
            if (moved) await sleep(300);
        }

        function showFloatingText(text) {
            const el = document.createElement('div');
            el.innerText = text;
            el.style.position = 'absolute';
            el.style.left = '50%';
            el.style.top = '40%';
            el.style.transform = 'translate(-50%, -50%)';
            el.style.color = '#ffd700';
            el.style.fontSize = '2.5rem';
            el.style.textShadow = '3px 3px 0 #000, 0 4px 6px rgba(0,0,0,0.8)';
            el.style.zIndex = '100';
            el.style.pointerEvents = 'none';
            el.style.animation = 'floatUp 1s cubic-bezier(0.34, 1.56, 0.64, 1) forwards';
            boardElem.appendChild(el);
            setTimeout(() => el.remove(), 1000);
        }

        function updateUI() {
            let levelData = LEVELS[currentLevel];
            if (!levelData) return;
            
            document.getElementById('level-title').innerText = `Nível ${levelData.level}`;
            movesElem.innerText = moves;
            
            let desc = '';
            let pTotal = 0;
            let cTotal = 0;
            for (let t in levelData.targets) {
                let req = levelData.targets[t];
                let col = Math.min(req, collected[t] || 0);
                desc += `${col}/${req} ${ICONS[t]} `;
                pTotal += req;
                cTotal += col;
            }
            document.getElementById('goal-desc').innerText = desc;
            let p = Math.min(100, (cTotal / pTotal) * 100);
            
            document.getElementById('progress-fill').style.width = `${p}%`;
        }

        function checkWinLose() {
            let levelData = LEVELS[currentLevel];
            let won = true;
            
            for(let t in levelData.targets) {
                if ((collected[t] || 0) < levelData.targets[t]) won = false;
            }
            
            if (won) {
                SoundFX.win();
                if (currentLevel < LEVELS.length - 1) {
                    showModal(`Nível ${levelData.level} Concluído!`, 'Trabalho bem feito, minerador!', 'Próximo Nível', () => {
                        currentLevel++;
                        initGame();
                    });
                } else {
                    showModal(`Mestre da Mineração!`, 'Você completou todos os desafios.', 'Jogar Novamente', () => {
                        currentLevel = 0;
                        initGame();
                    });
                }
            } else if (moves <= 0) {
                showModal('Sem Picaretas!', 'Você ficou sem movimentos. Tente novamente!', 'Tentar Novamente', () => {
                    initGame();
                });
            }
        }

        function showModal(title, desc, btnText, callback) {
            document.getElementById('modal-title').innerText = title;
            document.getElementById('modal-desc').innerText = desc;
            let btn = document.getElementById('modal-btn');
            btn.innerText = btnText;
            btn.onclick = callback;
            document.getElementById('modal').classList.add('visible');
        }

        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }

        window.onload = initGame;
    </script>
</body>
</html>
''')

