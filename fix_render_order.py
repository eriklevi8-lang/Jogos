import re

with open("aether-royale.html", "r") as f:
    content = f.read()

# Hide threeCanvas
css_old = """        #threeCanvas {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            pointer-events: none;
            z-index: 2;
        }"""
css_new = """        #threeCanvas {
            display: none;
        }"""
content = content.replace(css_old, css_new)

# In draw(), separate mesh update and rendering
draw_end = """    entities.forEach(e => e.draw(ctx));
    projectiles.forEach(p => p.draw(ctx));

    // Draw effects
    particles.forEach(p => p.draw(ctx));
    effects.forEach(ef => {
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

    // Render 3D Scene
    if (typeof threeRenderer !== 'undefined' && threeRenderer) {
        threeRenderer.render(threeScene, threeCamera);
    }
    
    ctx.restore();
}"""

draw_end_new = """    // Update mesh positions
    entities.forEach(e => {
        if (e.updateMesh) e.updateMesh();
    });

    // Render 3D Scene
    if (typeof threeRenderer !== 'undefined' && threeRenderer) {
        threeRenderer.render(threeScene, threeCamera);
        ctx.save();
        ctx.resetTransform();
        ctx.drawImage(threeRenderer.domElement, 0, 0);
        ctx.restore();
    }

    entities.forEach(e => e.draw(ctx));
    projectiles.forEach(p => p.draw(ctx));

    // Draw effects
    particles.forEach(p => p.draw(ctx));
    effects.forEach(ef => {
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
content = content.replace(draw_end, draw_end_new)

with open("aether-royale.html", "w") as f:
    f.write(content)
