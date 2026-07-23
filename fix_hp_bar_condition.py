import re

with open("aether-royale.html", "r") as f:
    content = f.read()

content = content.replace("""    draw(ctx) {
        let r = this.radius * cellSize;
        if (this.hp < this.maxHp) {
            drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
        }
    }""", """    draw(ctx) {
        let r = this.radius * cellSize;
        drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
    }""")

with open("aether-royale.html", "w") as f:
    f.write(content)
