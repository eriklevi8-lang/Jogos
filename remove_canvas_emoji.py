import re

with open("aether-royale.html", "r") as f:
    content = f.read()

troop_draw_emoji_old = """        // Draw emoji overlay in canvas
        ctx.font = `${r*1.2}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.icon, 0, this.isMoving ? -r*0.6 : -r*0.5);
        
        ctx.restore();"""

troop_draw_emoji_new = """        ctx.restore();"""
content = content.replace(troop_draw_emoji_old, troop_draw_emoji_new)


build_draw_emoji_old = """        // Only draw emoji
        ctx.font = `${r}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.icon, 0, -r*0.5);
        
        ctx.restore();"""
build_draw_emoji_new = """        ctx.restore();"""
content = content.replace(build_draw_emoji_old, build_draw_emoji_new)

with open("aether-royale.html", "w") as f:
    f.write(content)
