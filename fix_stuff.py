import re

with open("aether-royale.html", "r") as f:
    content = f.read()

# 1. HP Bar text fix
hpbar_old = """    // HP text
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
    if (level !== null) {"""
hpbar_new = """    // HP text
    ctx.font = '900 11px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = 'black';
    ctx.strokeText(Math.floor(hp), x, y - 8);
    ctx.fillStyle = 'white';
    ctx.fillText(Math.floor(hp), x, y - 8);
    
    // Level badge
    if (level !== null) {"""
content = content.replace(hpbar_old, hpbar_new)

# 2. Revert Tower size
tower_size_old = """    let r = entity.radius * cellSize * 1.5; // Scaled up slightly for impact
    if (entity.isNexus) r *= 1.1;"""
tower_size_new = """    let r = entity.radius * cellSize;
    if (entity.isNexus) r *= 1.2;"""
content = content.replace(tower_size_old, tower_size_new)

with open("aether-royale.html", "w") as f:
    f.write(content)
