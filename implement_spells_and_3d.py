import re

with open("aether-royale.html", "r") as f:
    content = f.read()

# 1. SpellProjectile class and array
spell_code = """
let spellProjectiles = [];

class SpellProjectile {
    constructor(startX, startY, targetX, targetY, card, team) {
        this.x = startX;
        this.y = startY;
        this.startX = startX;
        this.startY = startY;
        this.targetX = targetX;
        this.targetY = targetY;
        this.card = card;
        this.team = team;
        
        let d = Math.hypot(targetX - startX, targetY - startY);
        this.speed = 15.0; 
        this.duration = d / this.speed;
        this.time = 0;
        
        playSound('spell_launch');
    }
    
    update(dt) {
        this.time += dt;
        let t = this.time / this.duration;
        if (t >= 1.0) {
            this.hit();
            return true;
        }
        
        this.x = this.startX + (this.targetX - this.startX) * t;
        this.y = this.startY + (this.targetY - this.startY) * t;
        
        particles.push(new Particle(this.x * cellSize, this.y * cellSize, this.card.id === 'meteoro' ? '#f97316' : '#d946ef'));
        return false;
    }
    
    hit() {
        effects.push({ x: this.targetX, y: this.targetY, radius: this.card.radius, time: 0.5, type: this.card.id });
        playSound('spell');
        
        entities.forEach(e => {
            if (e.team !== this.team && dist(e, {x: this.targetX, y: this.targetY}) <= this.card.radius) {
                let dmg = e.isBuilding ? this.card.crownDmg : this.card.damage;
                e.damage(dmg);
                if (this.card.stun) e.stunTimer = this.card.stun;
                if (this.card.knockback && !e.isBuilding) {
                    let angle = Math.atan2(e.y - this.targetY, e.x - this.targetX);
                    e.x += Math.cos(angle) * this.card.knockback;
                    e.y += Math.sin(angle) * this.card.knockback;
                }
            }
        });
    }
    
    draw(ctx) {
        let px = this.x * cellSize;
        let py = this.y * cellSize;
        let offsetX = (cw - COLS * cellSize) / 2;
        let offsetY = (ch - ROWS * cellSize) / 2;
        px += offsetX;
        py += offsetY;
        
        let t = this.time / this.duration;
        let h = Math.sin(t * Math.PI) * 4 * cellSize;
        
        ctx.fillStyle = this.card.id === 'meteoro' ? '#f97316' : '#a855f7';
        ctx.beginPath();
        ctx.arc(px, py - h, cellSize*0.6, 0, Math.PI*2);
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();
    }
}
"""
content = content.replace("let effects = [];", spell_code + "\nlet effects = [];")

# Update playCard
play_old = """function playCard(card, x, y, team) {
    if (card.type === 'spell') {
        effects.push({ x, y, radius: card.radius, time: 0.5, type: card.id }); playSound('spell');
        
        entities.forEach(e => {
            if (e.team !== team && dist(e, {x, y}) <= card.radius) {
                let dmg = e.isBuilding ? card.crownDmg : card.damage;
                e.damage(dmg);
                if (card.stun) e.stunTimer = card.stun;
                if (card.knockback && !e.isBuilding) {
                    let angle = Math.atan2(e.y - y, e.x - x);
                    e.x += Math.cos(angle) * card.knockback;
                    e.y += Math.sin(angle) * card.knockback;
                }
            }
        });
    } else if (card.type === 'building') {"""
play_new = """function playCard(card, x, y, team) {
    if (card.type === 'spell') {
        let king = entities.find(e => e.team === team && e.isNexus);
        let startX = king ? king.x : (team === 1 ? COLS/2 : COLS/2);
        let startY = king ? king.y : (team === 1 ? ROWS : 0);
        spellProjectiles.push(new SpellProjectile(startX, startY, x, y, card, team));
    } else if (card.type === 'building') {"""
content = content.replace(play_old, play_new)

# Update spell drawing/updating loop
update_effects_old = """    particles.forEach(p => p.update(dt));
    particles = particles.filter(p => p.life > 0);
    
    effects.forEach(ef => ef.time -= dt);
    effects = effects.filter(ef => ef.time > 0);"""
update_effects_new = """    particles.forEach(p => p.update(dt));
    particles = particles.filter(p => p.life > 0);
    
    for(let i = spellProjectiles.length-1; i>=0; i--) {
        if(spellProjectiles[i].update(dt)) spellProjectiles.splice(i, 1);
    }
    
    effects.forEach(ef => ef.time -= dt);
    effects = effects.filter(ef => ef.time > 0);"""
content = content.replace(update_effects_old, update_effects_new)

# 2. Three.js Initialization and Setup
three_init_code = """
let threeScene, threeCamera, threeRenderer;

function initThree() {
    let canvas3d = document.getElementById('threeCanvas');
    if (!window.THREE) return; // Safeguard if not loaded
    threeRenderer = new THREE.WebGLRenderer({ canvas: canvas3d, alpha: true, antialias: true });
    threeRenderer.setSize(cw, ch);
    
    threeScene = new THREE.Scene();
    threeCamera = new THREE.OrthographicCamera(0, cw, 0, ch, -1000, 1000);
    threeCamera.position.set(0, 0, 100);
    
    let ambLight = new THREE.AmbientLight(0xffffff, 0.7);
    threeScene.add(ambLight);
    
    let dirLight = new THREE.DirectionalLight(0xffffff, 0.6);
    dirLight.position.set(cw/2, ch, 200);
    threeScene.add(dirLight);
}

function create3DTroop(entity) {
    if (!window.THREE) return null;
    const group = new THREE.Group();
    const isBlue = entity.team === 1;
    const bodyColor = isBlue ? 0x2563eb : 0xdc2626;
    
    let r = entity.radius * cellSize * 0.8;
    
    const bodyGeo = new THREE.CylinderGeometry(r*0.4, r*0.8, r*1.5, 12);
    const bodyMat = new THREE.MeshLambertMaterial({ color: bodyColor });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.rotation.x = -Math.PI / 2; 
    body.position.z = -r*0.75;
    group.add(body);
    
    const headGeo = new THREE.SphereGeometry(r*0.6, 12, 12);
    const headMat = new THREE.MeshLambertMaterial({ color: 0xffffff });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.z = -r*1.5 - r*0.2;
    group.add(head);
    
    group.rotation.order = 'ZXY';
    return group;
}

function create3DBuilding(entity) {
    if (!window.THREE) return null;
    const group = new THREE.Group();
    const isBlue = entity.team === 1;
    const bodyColor = isBlue ? 0x1e3a8a : 0x7f1d1d;
    
    let r = entity.radius * cellSize;
    if (entity.isNexus) r *= 1.2;
    
    const baseGeo = new THREE.BoxGeometry(r*1.8, r*1.8, r*2);
    const baseMat = new THREE.MeshLambertMaterial({ color: bodyColor });
    const base = new THREE.Mesh(baseGeo, baseMat);
    base.position.z = -r;
    group.add(base);
    
    const topGeo = new THREE.BoxGeometry(r*2, r*2, r*0.5);
    const topMat = new THREE.MeshLambertMaterial({ color: 0x94a3b8 });
    const top = new THREE.Mesh(topGeo, topMat);
    top.position.z = -r*2 - r*0.25;
    group.add(top);
    
    group.rotation.order = 'ZXY';
    return group;
}
"""
content = content.replace("function initGame() {", three_init_code + "\nfunction initGame() {")

# Modify Entity constructor to create mesh
ent_cons_old = """    constructor(x, y, team, stats) {
        this.x = x;
        this.y = y;
        this.team = team;
        Object.assign(this, stats);
        this.maxHp = this.hp;
        this.isDead = false;
        this.stunTimer = 0;
        this.deployTimer = 1.0; // 1s deploy time
    }"""
ent_cons_new = """    constructor(x, y, team, stats) {
        this.x = x;
        this.y = y;
        this.team = team;
        Object.assign(this, stats);
        this.maxHp = this.hp;
        this.isDead = false;
        this.stunTimer = 0;
        this.deployTimer = 1.0; // 1s deploy time
        
        if (typeof threeScene !== 'undefined' && threeScene) {
            this.mesh = this.isBuilding ? create3DBuilding(this) : create3DTroop(this);
            if (this.mesh) threeScene.add(this.mesh);
        }
    }"""
content = content.replace(ent_cons_old, ent_cons_new)

# Modify Entity die to remove mesh
die_old = """    die() {
        this.isDead = true;
        playSound('death');
        if (this.deathSpawn) {
            spawnUnit(this.spawnCard, this.x, this.y, this.team, this.deathSpawn);
        }
    }"""
die_new = """    die() {
        this.isDead = true;
        playSound('death');
        if (this.deathSpawn) {
            spawnUnit(this.spawnCard, this.x, this.y, this.team, this.deathSpawn);
        }
        if (this.mesh && typeof threeScene !== 'undefined') {
            threeScene.remove(this.mesh);
        }
    }"""
content = content.replace(die_old, die_new)

# Rewrite troop drawing to use 3D
troop_draw_old = """        // Make them larger visually
        let visR = r * 1.2; 
        let jumpY = this.isMoving ? -visR*0.3 : 0;
        
        // Pawn Base Shadow
        ctx.fillStyle = 'rgba(0,0,0,0.3)';
        ctx.beginPath(); ctx.ellipse(0, visR*0.6, visR*0.8, visR*0.4, 0, 0, Math.PI*2); ctx.fill();
        
        // Pawn Base
        ctx.fillStyle = this.team === 1 ? '#1e40af' : '#991b1b';
        ctx.beginPath(); ctx.ellipse(0, visR*0.5 + jumpY, visR*0.9, visR*0.45, 0, 0, Math.PI*2); ctx.fill();
        
        // Pawn Body (cone-like)
        ctx.beginPath();
        ctx.moveTo(-visR*0.9, visR*0.5 + jumpY);
        ctx.lineTo(visR*0.9, visR*0.5 + jumpY);
        ctx.lineTo(visR*0.5, -visR*0.2 + jumpY);
        ctx.lineTo(-visR*0.5, -visR*0.2 + jumpY);
        ctx.fill();
        
        // Pawn Collar
        ctx.fillStyle = this.team === 1 ? '#3b82f6' : '#ef4444';
        ctx.beginPath(); ctx.ellipse(0, -visR*0.2 + jumpY, visR*0.6, visR*0.3, 0, 0, Math.PI*2); ctx.fill();
        
        // Pawn Head (Orb)
        let gradient = ctx.createRadialGradient(-visR*0.2, -visR*0.8 + jumpY, visR*0.1, 0, -visR*0.6 + jumpY, visR*0.7);
        gradient.addColorStop(0, '#ffffff');
        gradient.addColorStop(0.3, this.team === 1 ? '#60a5fa' : '#f87171');
        gradient.addColorStop(1, this.team === 1 ? '#1d4ed8' : '#b91c1c');
        
        ctx.fillStyle = gradient;
        ctx.beginPath(); ctx.arc(0, -visR*0.6 + jumpY, visR*0.7, 0, Math.PI*2); ctx.fill();
        
        // Emoji on face
        ctx.font = `${visR*0.9}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.icon, 0, -visR*0.6 + jumpY);
        
        ctx.restore();
        
        // Draw HP
        if (this.hp < this.maxHp && this.deployTimer <= 0) {
            drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
        }"""
troop_draw_new = """        if (this.mesh) {
            let px = this.x * cellSize + offsetX;
            let py = this.y * cellSize + offsetY;
            this.mesh.position.set(px, py, 0);
            
            let rotZ = 0;
            if (this.target) {
                let angle = Math.atan2(this.target.y - this.y, this.target.x - this.x);
                rotZ = angle - Math.PI/2; 
            } else {
                rotZ = this.team === 1 ? 0 : Math.PI;
            }
            
            this.mesh.rotation.z = rotZ;
            this.mesh.rotation.x = -Math.PI / 6; // Tilt for 3D perspective
            
            if (this.isMoving && !this.isAir) {
                this.mesh.position.y += Math.abs(Math.sin(globalTime * 15)) * (r * -0.3);
                this.mesh.rotation.y = Math.sin(globalTime * 10) * 0.2;
            }
            if (this.isAir) {
                this.mesh.position.y += Math.sin(globalTime * 4) * (r * 0.2);
            }
        }
        
        // Draw emoji overlay in canvas
        ctx.font = `${r*1.2}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.icon, 0, this.isMoving ? -r*0.6 : -r*0.5);
        
        ctx.restore();
        
        if (this.hp < this.maxHp && this.deployTimer <= 0) {
            drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
        }"""
content = content.replace(troop_draw_old, troop_draw_new)

# Rewrite Building drawing to use 3D
build_draw_old = """    draw(ctx) {
        let r = this.radius * cellSize;
        if (this.isNexus) r *= 1.2;
        
        ctx.save();
        ctx.translate(this.x * cellSize, this.y * cellSize);
        
        if (this.deployTimer > 0) {
            ctx.globalAlpha = 0.5;
        }

        ctx.fillStyle = this.team === 1 ? '#1e3a8a' : '#7f1d1d';
        ctx.beginPath(); ctx.ellipse(0, r*0.3, r, r/2, 0, 0, Math.PI*2); ctx.fill();
        ctx.fillRect(-r, -r*0.5, r*2, r*0.8);
        
        ctx.fillStyle = this.team === 1 ? '#3b82f6' : '#ef4444';
        ctx.beginPath(); ctx.ellipse(0, -r*0.5, r, r/2, 0, 0, Math.PI*2); ctx.fill();
        
        ctx.font = `${r}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.icon, 0, -r*0.5);
        
        ctx.restore();
        
        if (this.hp < this.maxHp && this.deployTimer <= 0) {
            drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
        }
    }"""
build_draw_new = """    draw(ctx) {
        let r = this.radius * cellSize;
        if (this.isNexus) r *= 1.2;
        
        let offsetX = (cw - COLS * cellSize) / 2;
        let offsetY = (ch - ROWS * cellSize) / 2;
        
        if (this.mesh) {
            let px = this.x * cellSize + offsetX;
            let py = this.y * cellSize + offsetY;
            this.mesh.position.set(px, py, 0);
            this.mesh.rotation.x = -Math.PI / 6;
        }
        
        ctx.save();
        ctx.translate(this.x * cellSize, this.y * cellSize);
        
        if (this.deployTimer > 0) {
            ctx.globalAlpha = 0.5;
        }
        
        // Only draw emoji
        ctx.font = `${r}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.icon, 0, -r*0.5);
        
        ctx.restore();
        
        if (this.hp < this.maxHp && this.deployTimer <= 0) {
            drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
        }
    }"""
content = content.replace(build_draw_old, build_draw_new)

# Add initThree call and music call to initGame
init_game_old = """function initGame() {
    canvas = document.getElementById('gameCanvas');
    ctx = canvas.getContext('2d');
    
    // Setup Deck"""
init_game_new = """function initGame() {
    canvas = document.getElementById('gameCanvas');
    ctx = canvas.getContext('2d');
    
    initThree();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    playMusic();
    
    // Setup Deck"""
content = content.replace(init_game_old, init_game_new)

# Handle Three.js resize
resize_old = """function resize() {
    let wrapper = document.getElementById('canvas-wrapper') || document.body;
    cw = wrapper.clientWidth;
    ch = wrapper.clientHeight;
    canvas.width = cw;
    canvas.height = ch;
    
    cellSize = Math.min(cw / COLS, ch / ROWS) * 0.95;
}"""
resize_new = """function resize() {
    let wrapper = document.getElementById('canvas-wrapper') || document.body;
    cw = wrapper.clientWidth;
    ch = wrapper.clientHeight;
    canvas.width = cw;
    canvas.height = ch;
    
    cellSize = Math.min(cw / COLS, ch / ROWS) * 0.95;
    
    if (typeof threeRenderer !== 'undefined' && threeRenderer) {
        threeRenderer.setSize(cw, ch);
        threeCamera.left = 0;
        threeCamera.right = cw;
        threeCamera.top = 0;
        threeCamera.bottom = ch;
        threeCamera.updateProjectionMatrix();
    }
}"""
content = content.replace(resize_old, resize_new)

# Draw spells and threejs
draw_end_old = """    effects.forEach(ef => {
        let px = ef.x * cellSize;
        let py = ef.y * cellSize;
        let r = ef.radius * cellSize;
        let p = 1.0 - (ef.time / 0.5); // 0.0 to 1.0
        ctx.fillStyle = ef.type === 'meteoro' ? 'rgba(255, 100, 0, 0.4)' : ef.type === 'relampago' ? 'rgba(255, 255, 0, 0.6)' : 'rgba(217, 70, 239, 0.4)';
        ctx.beginPath(); ctx.arc(px, py, r * (1.0 + p*0.2), 0, Math.PI*2); ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = ef.type === 'meteoro' ? 'rgba(255, 100, 0, 0.8)' : ef.type === 'relampago' ? 'rgba(255, 255, 0, 1.0)' : 'rgba(217, 70, 239, 0.8)';
        ctx.beginPath(); ctx.arc(px, py, r * (1.0 + p*0.5), 0, Math.PI*2); ctx.stroke();
    });
    ctx.restore();
}"""
draw_end_new = """    effects.forEach(ef => {
        let px = ef.x * cellSize;
        let py = ef.y * cellSize;
        let r = ef.radius * cellSize;
        let p = 1.0 - (ef.time / 0.5); // 0.0 to 1.0
        ctx.fillStyle = ef.type === 'meteoro' ? 'rgba(255, 100, 0, 0.4)' : ef.type === 'relampago' ? 'rgba(255, 255, 0, 0.6)' : 'rgba(217, 70, 239, 0.4)';
        ctx.beginPath(); ctx.arc(px, py, r * (1.0 + p*0.2), 0, Math.PI*2); ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = ef.type === 'meteoro' ? 'rgba(255, 100, 0, 0.8)' : ef.type === 'relampago' ? 'rgba(255, 255, 0, 1.0)' : 'rgba(217, 70, 239, 0.8)';
        ctx.beginPath(); ctx.arc(px, py, r * (1.0 + p*0.5), 0, Math.PI*2); ctx.stroke();
    });
    
    ctx.restore();
    
    // Draw spells (they handle their own offset since they calculate absolute px py)
    // Wait, SpellProjectile uses offsetX inside its draw! So we can just call it without ctx.restore
    // Actually we restored, so we are at 0,0. This is perfect for SpellProjectile draw.
    spellProjectiles.forEach(sp => sp.draw(ctx));
    
    if (typeof threeRenderer !== 'undefined' && threeRenderer) {
        threeRenderer.render(threeScene, threeCamera);
    }
}"""
content = content.replace(draw_end_old, draw_end_new)

with open("aether-royale.html", "w") as f:
    f.write(content)
