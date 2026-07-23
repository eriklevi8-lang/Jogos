import re

with open("aether-royale.html", "r") as f:
    content = f.read()

# 1. Add screenShake global
content = content.replace("let globalTime = 0;", "let globalTime = 0;\nlet screenShake = 0;")

# 2. Add screenShake update
update_old = """        for (let i = particles.length - 1; i >= 0; i--) {
            particles[i].update(dt);
            if (particles[i].life <= 0) particles.splice(i, 1);
        }"""
update_new = """        for (let i = particles.length - 1; i >= 0; i--) {
            particles[i].update(dt);
            if (particles[i].life <= 0) particles.splice(i, 1);
        }
        
        if (screenShake > 0) {
            screenShake -= dt * 5;
            if (screenShake < 0) screenShake = 0;
        }"""
content = content.replace(update_old, update_new)

# 3. Apply screen shake in draw
draw_old = """    ctx.translate(offsetX, offsetY);

    // Grass Background"""
draw_new = """    ctx.translate(offsetX, offsetY);
    if (screenShake > 0) {
        ctx.translate((Math.random() - 0.5) * screenShake * 10, (Math.random() - 0.5) * screenShake * 10);
    }

    // Grass Background"""
content = content.replace(draw_old, draw_new)

# 4. Tower damage screenshake
tower_damage_old = """    damage(amt) {
        super.damage(amt);
        if (this.isNexus && !this.active) this.active = true;
    }"""
tower_damage_new = """    damage(amt) {
        super.damage(amt);
        if (this.isNexus && !this.active) this.active = true;
        
        screenShake = 1.0; // impact
        for(let i=0; i<15; i++) {
            particles.push(new Particle(this.x * cellSize, (this.y - this.radius) * cellSize, '#ef4444'));
        }
    }"""
content = content.replace(tower_damage_old, tower_damage_new)

# 5. Add hover state and preview tracking
content = content.replace("let isGameOver = false;", "let isGameOver = false;\nlet hoverX = -1, hoverY = -1;")

tracking_code = """canvas.addEventListener('pointerdown', handleBoardClick);

    // Add pointer hover tracking
    canvas.addEventListener('pointermove', (e) => {
        let rect = canvas.getBoundingClientRect();
        let offsetX = (cw - COLS * cellSize) / 2;
        let offsetY = (ch - ROWS * cellSize) / 2;
        hoverX = (e.clientX - rect.left - offsetX) / cellSize;
        hoverY = (e.clientY - rect.top - offsetY) / cellSize;
    });
    canvas.addEventListener('pointerleave', () => {
        hoverX = -1;
        hoverY = -1;
    });"""
content = content.replace("canvas.addEventListener('pointerdown', handleBoardClick);", tracking_code)

# 6. Draw Preview
preview_code = """
    // Sort by Y for fake depth
    entities.sort((a,b) => a.y - b.y);

    // Draw Preview
    if (selectedCardIdx >= 0 && hoverX >= 0 && hoverY >= 0 && hoverX <= COLS && hoverY <= ROWS) {
        let cardId = hand[selectedCardIdx];
        let card = CARDS_DB[cardId];
        
        let isValid = true;
        if (card.type !== 'spell' && hoverY < 16) isValid = false;
        if (elixir < card.cost) isValid = false;
        
        ctx.save();
        ctx.globalAlpha = 0.5;
        
        if (card.type !== 'spell') {
            ctx.fillStyle = isValid ? 'rgba(255, 255, 255, 0.2)' : 'rgba(255, 0, 0, 0.2)';
            ctx.fillRect(0, 16*cellSize, COLS*cellSize, (ROWS-16)*cellSize);
        }
        
        let px = hoverX * cellSize;
        let py = hoverY * cellSize;
        
        if (card.type === 'spell') {
            let r = card.radius * cellSize;
            ctx.beginPath();
            ctx.arc(px, py, r, 0, Math.PI*2);
            ctx.fillStyle = isValid ? 'rgba(217, 70, 239, 0.4)' : 'rgba(255, 0, 0, 0.4)';
            ctx.fill();
            ctx.strokeStyle = isValid ? '#d946ef' : '#ef4444';
            ctx.lineWidth = 2;
            ctx.stroke();
        } else {
            let r = 1.2 * cellSize;
            ctx.fillStyle = isValid ? '#3b82f6' : '#ef4444';
            ctx.beginPath(); ctx.ellipse(px, py + r*0.5, r, r/2, 0, 0, Math.PI*2); ctx.fill();
            
            ctx.beginPath(); ctx.arc(px, py, r, 0, Math.PI*2); ctx.fill();
            ctx.font = `${r*1.3}px Arial`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(card.icon, px, py + r*0.1);
        }
        
        ctx.restore();
    }
"""
content = content.replace("// Sort by Y for fake depth\n    entities.sort((a,b) => a.y - b.y);", preview_code)

# CSS changes for hover
css_hover_old = """        .card-slot:active {
            transform: scale(0.95);
        }"""
        
css_hover_new = """        .card-slot:active {
            transform: scale(0.95);
        }
        
        .card-slot:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.5), inset 0 0 10px rgba(255,255,255,0.6);
            z-index: 10;
        }"""
content = content.replace(css_hover_old, css_hover_new)

with open("aether-royale.html", "w") as f:
    f.write(content)

