import re

with open("aether-royale.html", "r") as f:
    content = f.read()

# 1. Add ThreeJS script
content = content.replace("</head>", '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n</head>')

# 2. Add canvas and CSS
content = content.replace('<canvas id="gameCanvas"></canvas>', '<canvas id="gameCanvas"></canvas>\n        <canvas id="threeCanvas"></canvas>')
css_three = """        #threeCanvas {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            pointer-events: none;
            z-index: 2;
        }"""
content = content.replace("</style>", css_three + "\n</style>")

# 3. Add Pathfinding (A*)
astar_code = """
function isWalkable(x, y, isAir) {
    if (isAir) return true;
    if (x < 0 || x >= COLS || y < 0 || y >= ROWS) return false;
    if (y === 15 || y === 16) {
        if ((x >= 2 && x <= 5) || (x >= 12 && x <= 15)) return true;
        return false;
    }
    return true;
}

function aStar(start, goal, isAir) {
    let openSet = [start];
    let cameFrom = new Map();
    let gScore = new Map();
    let fScore = new Map();
    
    let hash = (p) => `${p.x},${p.y}`;
    gScore.set(hash(start), 0);
    fScore.set(hash(start), dist(start, goal));
    
    let iters = 0;
    while(openSet.length > 0 && iters < 500) {
        iters++;
        openSet.sort((a,b) => (fScore.get(hash(a))||Infinity) - (fScore.get(hash(b))||Infinity));
        let curr = openSet.shift();
        
        if (curr.x === goal.x && curr.y === goal.y) {
            let path = [curr];
            while(cameFrom.has(hash(curr))) {
                curr = cameFrom.get(hash(curr));
                path.push(curr);
            }
            return path.reverse();
        }
        
        let dirs = [[0,1], [1,0], [0,-1], [-1,0], [1,1], [-1,1], [1,-1], [-1,-1]];
        for(let d of dirs) {
            let nx = curr.x + d[0];
            let ny = curr.y + d[1];
            if (!isWalkable(nx, ny, isAir)) continue;
            
            let neighbor = {x: nx, y: ny};
            let tentativeG = (gScore.get(hash(curr))||Infinity) + Math.hypot(d[0], d[1]);
            
            if (tentativeG < (gScore.get(hash(neighbor))||Infinity)) {
                cameFrom.set(hash(neighbor), curr);
                gScore.set(hash(neighbor), tentativeG);
                fScore.set(hash(neighbor), tentativeG + dist(neighbor, goal));
                if (!openSet.find(p => p.x === nx && p.y === ny)) {
                    openSet.push(neighbor);
                }
            }
        }
    }
    return null;
}
"""
content = content.replace("// --- Game State ---", astar_code + "\n// --- Game State ---")

move_target_old = """    moveTowardsTarget(dt) {
        let tx = this.target.x;
        let ty = this.target.y;

        // Pathfinding around river for ground troops
        if (!this.isAir) {
            let mySide = this.y > 15.5;
            let tSide = ty > 15.5;
            let onBridgeX = (this.x >= 2.5 && this.x <= 5.5) || (this.x >= 12.5 && this.x <= 15.5);
            
            if (mySide !== tSide && !onBridgeX) {
                // Must cross bridge
                let leftBridgeCenter = {x: 4, y: 15.5};
                let rightBridgeCenter = {x: 14, y: 15.5};
                
                let distL = dist(this, leftBridgeCenter) + dist(leftBridgeCenter, this.target);
                let distR = dist(this, rightBridgeCenter) + dist(rightBridgeCenter, this.target);
                
                let bridge = distL < distR ? leftBridgeCenter : rightBridgeCenter;
                
                tx = bridge.x;
                ty = bridge.y;
            }
        }

        this.moveTowards(tx, ty, dt);
    }"""
move_target_new = """    moveTowardsTarget(dt) {
        let tx = this.target.x;
        let ty = this.target.y;

        if (!this.isAir) {
            let mySide = this.y > 15.5;
            let tSide = this.target.y > 15.5;
            if (mySide !== tSide) {
                if (!this.pathTimer || this.pathTimer <= 0) {
                    let sx = Math.floor(this.x);
                    let sy = Math.floor(this.y);
                    let gx = Math.floor(this.target.x);
                    let gy = Math.floor(this.target.y);
                    this.path = aStar({x: sx, y: sy}, {x: gx, y: gy}, false);
                    this.pathTimer = 0.5; // Recompute every 0.5s
                } else {
                    this.pathTimer -= dt;
                }
                
                if (this.path && this.path.length > 1) {
                    let next = this.path[1];
                    if (dist(this, {x: next.x+0.5, y: next.y+0.5}) < 0.5 && this.path.length > 2) {
                        next = this.path[2];
                    }
                    tx = next.x + 0.5;
                    ty = next.y + 0.5;
                }
            } else {
                this.path = null;
            }
        }

        this.moveTowards(tx, ty, dt);
    }"""
content = content.replace(move_target_old, move_target_new)

# 4. Audio Refinements
music_code = """
let musicPlaying = false;
let musicInterval = null;

function playMusic() {
    if (musicPlaying || !soundEnabled || audioCtx.state === 'suspended') return;
    musicPlaying = true;
    
    musicInterval = setInterval(() => {
        if (!soundEnabled || audioCtx.state === 'suspended') return;
        let now = audioCtx.currentTime;
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        let notes = [110, 130, 110, 146, 164, 110, 130, 110];
        let note = notes[Math.floor(Date.now() / 500) % notes.length];
        
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(note, now);
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.03, now + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
        
        osc.start(now);
        osc.stop(now + 0.4);
    }, 500);
}
"""
content = content.replace("// --- Game State ---", music_code + "\n// --- Game State ---")

# Replace tower hit sound
thud_old = """    } else if (type === 'tower_hit') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(80, now);
        osc.frequency.exponentialRampToValueAtTime(20, now + 0.2);
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.3, now + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
        osc.start(now);
        osc.stop(now + 0.2);
    }"""
thud_new = """    } else if (type === 'tower_hit') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(120, now);
        osc.frequency.exponentialRampToValueAtTime(40, now + 0.3);
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.4, now + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
        
        let noiseSize = audioCtx.sampleRate * 0.2;
        let noiseBuf = audioCtx.createBuffer(1, noiseSize, audioCtx.sampleRate);
        let output = noiseBuf.getChannelData(0);
        for (let i = 0; i < noiseSize; i++) output[i] = Math.random() * 2 - 1;
        
        let whiteNoise = audioCtx.createBufferSource();
        whiteNoise.buffer = noiseBuf;
        let noiseFilter = audioCtx.createBiquadFilter();
        noiseFilter.type = 'lowpass';
        noiseFilter.frequency.value = 600;
        let noiseGain = audioCtx.createGain();
        whiteNoise.connect(noiseFilter);
        noiseFilter.connect(noiseGain);
        noiseGain.connect(audioCtx.destination);
        
        noiseGain.gain.setValueAtTime(0, now);
        noiseGain.gain.linearRampToValueAtTime(0.15, now + 0.02);
        noiseGain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
        
        whiteNoise.start(now);
        whiteNoise.stop(now + 0.2);
        
        osc.start(now);
        osc.stop(now + 0.3);
    } else if (type === 'spell_launch') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(400, now);
        osc.frequency.exponentialRampToValueAtTime(800, now + 0.3);
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.1, now + 0.1);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
        osc.start(now);
        osc.stop(now + 0.4);
    }"""
content = content.replace(thud_old, thud_new)

with open("aether-royale.html", "w") as f:
    f.write(content)
