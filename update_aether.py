import re

with open('aether-royale.html', 'r') as f:
    content = f.read()

# Add globalTime
content = content.replace("let isGameOver = false;", "let isGameOver = false;\nlet globalTime = 0;")
content = content.replace("gameTime -= dt;", "gameTime -= dt;\nglobalTime += dt;")

# Add animations variables to Entity
entity_old = """    constructor(x, y, team) {
        this.id = Math.random().toString(36).substr(2, 9);
        this.x = x;
        this.y = y;"""
entity_new = """    constructor(x, y, team) {
        this.id = Math.random().toString(36).substr(2, 9);
        this.x = x;
        this.y = y;
        this.animTime = Math.random() * 10;
        this.isMoving = false;
        this.attackAnimTimer = 0;"""
content = content.replace(entity_old, entity_new)

# Update Troop logic
troop_update_old = """    update(dt) {
        if (this.isDead) return;
        if (this.deployTimer > 0) { this.deployTimer -= dt; return; }
        if (this.stunTimer > 0) { this.stunTimer -= dt; return; }

        if (this.attackCooldown > 0) this.attackCooldown -= dt;

        // Retargeting
        if (!this.target || this.target.isDead || dist(this, this.target) > this.sightRange) {"""
troop_update_new = """    update(dt) {
        if (this.isDead) return;
        this.animTime += dt;
        if (this.attackAnimTimer > 0) this.attackAnimTimer -= dt;
        this.isMoving = false;

        if (this.deployTimer > 0) { this.deployTimer -= dt; return; }
        if (this.stunTimer > 0) { this.stunTimer -= dt; return; }

        if (this.attackCooldown > 0) this.attackCooldown -= dt;

        // Retargeting
        if (!this.target || this.target.isDead || dist(this, this.target) > this.sightRange) {"""
content = content.replace(troop_update_old, troop_update_new)

troop_attack_old = """        if (d <= this.attackRange + this.target.radius) {
            // Attack
            if (this.attackCooldown <= 0) {
                if (this.attackRange > 1.5) {
                    projectiles.push(new Projectile(this.x, this.y, this.target, this.damageAmt, this.aoe, this.aoeRadius));
                } else {
                    if (this.aoe) {
                        applyAoE(this.x, this.y, this.aoeRadius, this.damageAmt, this.team, this.targetAir);
                    } else {
                        this.target.damage(this.damageAmt);
                    }
                }
                this.attackCooldown = this.attackSpeed;
            }
        } else {
            // Move towards target
            this.moveTowardsTarget(dt);
        }"""
troop_attack_new = """        if (d <= this.attackRange + this.target.radius) {
            // Attack
            if (this.attackCooldown <= 0) {
                this.attackAnimTimer = 0.2; // 0.2s attack anim
                if (this.attackRange > 1.5) {
                    projectiles.push(new Projectile(this.x, this.y, this.target, this.damageAmt, this.aoe, this.aoeRadius));
                } else {
                    if (this.aoe) {
                        applyAoE(this.x, this.y, this.aoeRadius, this.damageAmt, this.team, this.targetAir);
                    } else {
                        this.target.damage(this.damageAmt);
                    }
                }
                this.attackCooldown = this.attackSpeed;
            }
        } else {
            // Move towards target
            this.moveTowardsTarget(dt);
            this.isMoving = true;
        }"""
content = content.replace(troop_attack_old, troop_attack_new)

# Update Troop draw
troop_draw_old = """    draw(ctx) {
        let px = this.x * cellSize;
        let py = this.y * cellSize;
        let r = this.radius * cellSize;
        
        if (this.deployTimer > 0) ctx.globalAlpha = 0.5;
        
        // Shadow for air
        if (this.isAir) {
            ctx.fillStyle = 'rgba(0,0,0,0.3)';
            ctx.beginPath(); ctx.ellipse(px, py + r*1.5, r, r/2, 0, 0, Math.PI*2); ctx.fill();
            py -= r; // elevate visually
        }

        ctx.fillStyle = this.team === 1 ? 'rgba(59, 130, 246, 0.5)' : 'rgba(239, 68, 68, 0.5)';
        ctx.beginPath(); ctx.arc(px, py, r, 0, Math.PI*2); ctx.fill();

        ctx.font = `${r*1.5}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.icon, px, py);

        ctx.globalAlpha = 1.0;
        if (this.hp < this.maxHp && this.deployTimer <= 0) {
            drawHpBar(ctx, px, py - r - 5, this.hp, this.maxHp);
        }
    }"""
troop_draw_new = """    draw(ctx) {
        let px = this.x * cellSize;
        let py = this.y * cellSize;
        let r = this.radius * cellSize;
        
        if (this.deployTimer > 0) ctx.globalAlpha = 0.5;
        
        // Animations
        let visualY = py;
        let visualX = px;
        let scale = 1;
        let rot = 0;
        
        if (this.isMoving && !this.isAir) {
            visualY += Math.abs(Math.sin(this.animTime * 15)) * (r * -0.3);
            rot = Math.sin(this.animTime * 10) * 0.15;
        } else if (this.isAir) {
            visualY += Math.sin(this.animTime * 4) * (r * 0.2);
        }
        
        if (this.attackAnimTimer > 0) {
            scale = 1 + (this.attackAnimTimer / 0.2) * 0.2;
            if (this.target) {
                let angle = Math.atan2(this.target.y - this.y, this.target.x - this.x);
                visualX += Math.cos(angle) * (r * 0.5) * (this.attackAnimTimer / 0.2);
                visualY += Math.sin(angle) * (r * 0.5) * (this.attackAnimTimer / 0.2);
            }
        }

        // Shadow
        ctx.fillStyle = 'rgba(0,0,0,0.4)';
        if (this.isAir) {
            ctx.beginPath(); ctx.ellipse(px, py + r*1.5, r, r/2, 0, 0, Math.PI*2); ctx.fill();
            visualY -= r*1.5; // elevate visually
        } else {
            ctx.beginPath(); ctx.ellipse(px, py + r*0.5, r, r/2, 0, 0, Math.PI*2); ctx.fill();
        }

        ctx.save();
        ctx.translate(visualX, visualY);
        ctx.rotate(rot);
        ctx.scale(scale, scale);

        ctx.fillStyle = this.team === 1 ? '#3b82f6' : '#ef4444';
        ctx.beginPath(); ctx.arc(0, 0, r, 0, Math.PI*2); ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = this.team === 1 ? '#1d4ed8' : '#b91c1c';
        ctx.stroke();

        ctx.font = `${r*1.3}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.icon, 0, r*0.1);

        ctx.restore();

        ctx.globalAlpha = 1.0;
        if (this.hp < this.maxHp && this.deployTimer <= 0) {
            drawHpBar(ctx, px, py - r - 10, this.hp, this.maxHp);
        }
    }"""
content = content.replace(troop_draw_old, troop_draw_new)

# Update Tower draw
tower_draw_old = """    draw(ctx) {
        let px = this.x * cellSize;
        let py = this.y * cellSize;
        let r = this.radius * cellSize;
        
        // Base
        ctx.fillStyle = '#94a3b8'; // Stone
        ctx.fillRect(px - r, py - r, r*2, r*2);
        // Roof/Accent
        ctx.fillStyle = this.team === 1 ? '#2563eb' : '#dc2626';
        ctx.fillRect(px - r, py - r, r*2, r*0.5);
        ctx.fillRect(px - r*0.8, py - r*1.2, r*1.6, r*0.5); // Top crown
        
        ctx.font = `${r*1.2}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.icon, px, py + r*0.2);

        drawHpBar(ctx, px, py - r - 15, this.hp, this.maxHp, this.isNexus ? 9 : 7);
    }"""
tower_draw_new = """    draw(ctx) {
        let px = this.x * cellSize;
        let py = this.y * cellSize;
        let r = this.radius * cellSize;
        
        // Tower Base (Shadow/Side)
        ctx.fillStyle = '#475569'; // Darker stone
        ctx.fillRect(px - r, py - r + r*0.5, r*2, r*1.5);
        
        // Tower Top Platform
        ctx.fillStyle = '#94a3b8'; // Lighter stone
        ctx.fillRect(px - r, py - r - r*0.5, r*2, r*2);
        
        // Team color banner
        ctx.fillStyle = this.team === 1 ? '#1d4ed8' : '#b91c1c';
        ctx.fillRect(px - r*0.6, py - r + r*0.5, r*1.2, r*1.2);
        // Banner detail
        ctx.fillStyle = '#fde047';
        ctx.fillRect(px - r*0.6, py - r + r*1.4, r*1.2, r*0.3);
        
        // Roof/Crown
        ctx.fillStyle = this.team === 1 ? '#3b82f6' : '#ef4444';
        ctx.fillRect(px - r*1.1, py - r - r*0.8, r*2.2, r*0.6);
        ctx.fillRect(px - r*0.8, py - r - r*1.2, r*1.6, r*0.6); 
        
        // Crown highlights
        ctx.fillStyle = 'rgba(255,255,255,0.2)';
        ctx.fillRect(px - r*1.1, py - r - r*0.8, r*2.2, r*0.2);

        // Icon on top
        // Animation for attack
        let iconScale = 1;
        let iconY = py - r*0.2;
        if (this.attackCooldown > this.attackSpeed - 0.2) {
            iconScale = 1.2;
            iconY -= r*0.2;
        }
        
        ctx.save();
        ctx.translate(px, iconY);
        ctx.scale(iconScale, iconScale);
        ctx.font = `${r*1.4}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.icon, 0, 0);
        ctx.restore();

        // HP
        drawHpBar(ctx, px, py - r - 22, this.hp, this.maxHp, this.isNexus ? 9 : 7);
    }"""
content = content.replace(tower_draw_old, tower_draw_new)


# Update HP Bar function
hp_bar_old = """function drawHpBar(ctx, x, y, hp, maxHp, level=null) {
    let w = 30;
    let h = 6;
    ctx.fillStyle = '#000';
    ctx.fillRect(x - w/2, y, w, h);
    ctx.fillStyle = '#ef4444'; // default red
    if (y > ROWS/2 * cellSize) ctx.fillStyle = '#3b82f6'; // blue for player
    
    let hpW = Math.max(0, w * (hp/maxHp));
    ctx.fillRect(x - w/2 + 1, y + 1, hpW - 2, h - 2);
    
    // Level badge
    if (level !== null) {
        ctx.fillStyle = '#000';
        ctx.beginPath(); ctx.arc(x - w/2 - 4, y + h/2, 6, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = '#eab308';
        ctx.beginPath(); ctx.arc(x - w/2 - 4, y + h/2, 5, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = '#000';
        ctx.font = '8px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(level, x - w/2 - 4, y + h/2 + 0.5);
    }
}"""
hp_bar_new = """function drawHpBar(ctx, x, y, hp, maxHp, level=null) {
    let w = 36;
    let h = 8;
    ctx.fillStyle = '#000';
    ctx.fillRect(x - w/2, y, w, h);
    
    let isPlayer = (y > ROWS/2 * cellSize);
    ctx.fillStyle = isPlayer ? '#3b82f6' : '#ef4444';
    
    let hpRatio = Math.max(0, hp/maxHp);
    ctx.fillRect(x - w/2 + 1, y + 1, (w - 2) * hpRatio, h - 2);
    
    // HP text
    if (level !== null) {
        ctx.font = '900 11px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.lineWidth = 2.5;
        ctx.strokeStyle = 'black';
        ctx.strokeText(Math.floor(hp), x + 6, y - 8);
        ctx.fillStyle = 'white';
        ctx.fillText(Math.floor(hp), x + 6, y - 8);
    }
    
    // Level badge
    if (level !== null) {
        let bx = x - w/2 - 6;
        let by = y + h/2;
        ctx.fillStyle = '#000';
        ctx.beginPath(); ctx.arc(bx, by, 8, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = isPlayer ? '#2563eb' : '#dc2626';
        ctx.beginPath(); ctx.arc(bx, by, 7, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = 'white';
        ctx.font = 'bold 9px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(level, bx, by + 1);
    }
}"""
content = content.replace(hp_bar_old, hp_bar_new)

# Update Map Draw
map_draw_old = """    // Checkerboard Grass Background
    ctx.fillStyle = '#4ade80';
    ctx.fillRect(0, 0, COLS * cellSize, ROWS * cellSize);
    
    ctx.fillStyle = '#22c55e'; // Darker green
    for(let i=0; i<COLS; i++) {
        for(let j=0; j<ROWS; j++) {
            if ((i+j)%2 === 0) {
                ctx.fillRect(i*cellSize, j*cellSize, cellSize, cellSize);
            }
        }
    }

    // Paths (Dirt)
    ctx.fillStyle = '#d97706'; // Dirt color
    let pWidth = 3 * cellSize;
    // Left path
    ctx.fillRect(2.5 * cellSize, 6 * cellSize, pWidth, 20 * cellSize);
    // Right path
    ctx.fillRect(12.5 * cellSize, 6 * cellSize, pWidth, 20 * cellSize);
    // King to Princess
    ctx.fillRect(4 * cellSize, 26 * cellSize, 10 * cellSize, pWidth); // Player
    ctx.fillRect(4 * cellSize, 3 * cellSize, 10 * cellSize, pWidth); // Enemy

    // Draw River
    ctx.fillStyle = '#d946ef'; // Magenta Arcane River
    ctx.fillRect(0, 15*cellSize, COLS*cellSize, 2.5*cellSize);
    
    // River glow/detail
    ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.fillRect(0, 15.2*cellSize, COLS*cellSize, 0.2*cellSize);
    ctx.fillRect(0, 16.8*cellSize, COLS*cellSize, 0.2*cellSize);

    // Draw Bridges
    ctx.fillStyle = '#78350f'; // Wood bridge
    let bw = 2.5 * cellSize;
    let bh = 3.5 * cellSize;
    let by = 14.5 * cellSize;
    // Left
    ctx.fillRect(2.75 * cellSize, by, bw, bh);
    ctx.fillStyle = '#92400e'; // planks
    for(let i=0; i<5; i++) ctx.fillRect(2.75*cellSize, by + i*(bh/5), bw, bh/5 - 2);
    
    // Right
    ctx.fillStyle = '#78350f';
    ctx.fillRect(12.75 * cellSize, by, bw, bh);
    ctx.fillStyle = '#92400e';
    for(let i=0; i<5; i++) ctx.fillRect(12.75*cellSize, by + i*(bh/5), bw, bh/5 - 2);"""

map_draw_new = """    // Grass Background
    ctx.fillStyle = '#166534';
    ctx.fillRect(0, 0, COLS * cellSize, ROWS * cellSize);
    
    ctx.fillStyle = '#15803d'; // Darker green pattern
    for(let i=0; i<COLS; i++) {
        for(let j=0; j<ROWS; j++) {
            if ((i+j)%2 === 0) {
                ctx.fillRect(i*cellSize, j*cellSize, cellSize, cellSize);
            }
        }
    }

    // Paths (Dirt)
    ctx.fillStyle = '#b45309'; // Dirt color
    let pWidth = 3 * cellSize;
    
    // Left path
    ctx.fillRect(2.5 * cellSize, 6 * cellSize, pWidth, 20 * cellSize);
    // Right path
    ctx.fillRect(12.5 * cellSize, 6 * cellSize, pWidth, 20 * cellSize);
    // King to Princess
    ctx.fillRect(4 * cellSize, 25.5 * cellSize, 10 * cellSize, pWidth); // Player
    ctx.fillRect(4 * cellSize, 3.5 * cellSize, 10 * cellSize, pWidth); // Enemy

    // River flow animation
    let rTime = globalTime;
    
    // Draw River Bank
    ctx.fillStyle = '#7e22ce'; // Dark magenta bank
    ctx.fillRect(0, 14.8*cellSize, COLS*cellSize, 2.9*cellSize);
    
    // Draw River
    ctx.fillStyle = '#d946ef'; // Magenta Arcane River
    ctx.fillRect(0, 15*cellSize, COLS*cellSize, 2.5*cellSize);
    
    // River glow/detail
    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.fillRect(0, 15.2*cellSize + Math.sin(rTime*2)*0.1*cellSize, COLS*cellSize, 0.15*cellSize);
    ctx.fillRect(0, 17.1*cellSize + Math.cos(rTime*2.5)*0.1*cellSize, COLS*cellSize, 0.1*cellSize);
    
    for(let i=0; i<COLS; i++) {
        let px = ((rTime * 1.5 + i) % COLS) * cellSize;
        ctx.fillRect(px, 15.8*cellSize + Math.sin(rTime*3 + i)*0.2*cellSize, 0.3*cellSize, 0.1*cellSize);
    }

    // Draw Bridges
    let bw = 2.5 * cellSize;
    let bh = 3.5 * cellSize;
    let by = 14.5 * cellSize;
    
    // Left Bridge
    ctx.fillStyle = '#451a03'; // Dark wood edge
    ctx.fillRect(2.65 * cellSize, by, bw + 0.2*cellSize, bh);
    ctx.fillStyle = '#78350f'; // Wood bridge
    ctx.fillRect(2.75 * cellSize, by, bw, bh);
    ctx.fillStyle = '#92400e'; // planks
    for(let i=0; i<5; i++) ctx.fillRect(2.75*cellSize, by + i*(bh/5), bw, bh/5 - 1);
    
    // Right Bridge
    ctx.fillStyle = '#451a03';
    ctx.fillRect(12.65 * cellSize, by, bw + 0.2*cellSize, bh);
    ctx.fillStyle = '#78350f';
    ctx.fillRect(12.75 * cellSize, by, bw, bh);
    ctx.fillStyle = '#92400e';
    for(let i=0; i<5; i++) ctx.fillRect(12.75*cellSize, by + i*(bh/5), bw, bh/5 - 1);"""

content = content.replace(map_draw_old, map_draw_new)

with open('aether-royale.html', 'w') as f:
    f.write(content)

