import re

with open("aether-royale.html", "r") as f:
    content = f.read()

def replace_draw_method(content, class_name, new_draw_method):
    pattern = r"(class " + class_name + r".*?    draw\(ctx\) \{)(.*?)(^\s*\})([^}]*?\})"
    # Actually it's better to just search for class and then draw
    
    # We can do this manually:
    idx = content.find(f"class {class_name} extends")
    if idx == -1: return content
    draw_idx = content.find("    draw(ctx) {", idx)
    if draw_idx == -1: return content
    
    # find the matching closing brace for draw(ctx) {
    brace_count = 0
    end_idx = -1
    for i in range(draw_idx + 15, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            if brace_count == 0:
                end_idx = i + 1
                break
            else:
                brace_count -= 1
                
    if end_idx != -1:
        return content[:draw_idx] + new_draw_method + content[end_idx:]
    return content

troop_new = """    draw(ctx) {
        let offsetX = (cw - COLS * cellSize) / 2;
        let offsetY = (ch - ROWS * cellSize) / 2;
        let r = this.radius * cellSize;
        
        if (this.mesh) {
            let px = this.x * cellSize + offsetX;
            let py = this.y * cellSize + offsetY;
            
            // moving anim
            let visualY = py;
            if (this.isMoving && !this.isAir) {
                visualY += Math.abs(Math.sin(globalTime * 15)) * (r * -0.3);
                this.mesh.rotation.y = Math.sin(globalTime * 10) * 0.2;
            } else if (this.isAir) {
                visualY += Math.sin(globalTime * 4) * (r * 0.2);
            }
            
            this.mesh.position.set(px, visualY, 0);
            
            let rotZ = 0;
            if (this.target) {
                let angle = Math.atan2(this.target.y - this.y, this.target.x - this.x);
                rotZ = angle - Math.PI/2; 
            } else {
                rotZ = this.team === 1 ? 0 : Math.PI;
            }
            
            this.mesh.rotation.z = rotZ;
            this.mesh.rotation.x = -Math.PI / 6; // Tilt for 3D perspective
            
            if (this.deployTimer > 0) {
                this.mesh.traverse((child) => {
                    if (child.isMesh) {
                        child.material.transparent = true;
                        child.material.opacity = 0.5;
                    }
                });
            } else {
                this.mesh.traverse((child) => {
                    if (child.isMesh) {
                        child.material.transparent = false;
                        child.material.opacity = 1.0;
                    }
                });
            }
        }
        
        if (this.hp < this.maxHp && this.deployTimer <= 0) {
            drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
        }
    }"""

tower_new = """    draw(ctx) {
        let offsetX = (cw - COLS * cellSize) / 2;
        let offsetY = (ch - ROWS * cellSize) / 2;
        let r = this.radius * cellSize;
        
        if (this.mesh) {
            let px = this.x * cellSize + offsetX;
            let py = this.y * cellSize + offsetY;
            this.mesh.position.set(px, py, 0);
            this.mesh.rotation.x = -Math.PI / 6;
        }
        
        if (this.hp < this.maxHp && this.deployTimer <= 0) {
            drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
        }
    }"""

building_new = """    draw(ctx) {
        let offsetX = (cw - COLS * cellSize) / 2;
        let offsetY = (ch - ROWS * cellSize) / 2;
        let r = this.radius * cellSize;
        
        if (this.mesh) {
            let px = this.x * cellSize + offsetX;
            let py = this.y * cellSize + offsetY;
            this.mesh.position.set(px, py, 0);
            this.mesh.rotation.x = -Math.PI / 6;
            
            if (this.deployTimer > 0) {
                this.mesh.traverse((child) => {
                    if (child.isMesh) {
                        child.material.transparent = true;
                        child.material.opacity = 0.5;
                    }
                });
            } else {
                this.mesh.traverse((child) => {
                    if (child.isMesh) {
                        child.material.transparent = false;
                        child.material.opacity = 1.0;
                    }
                });
            }
        }
        
        if (this.hp < this.maxHp && this.deployTimer <= 0) {
            drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
        }
    }"""

content = replace_draw_method(content, "Troop", troop_new)
content = replace_draw_method(content, "Tower", tower_new)
content = replace_draw_method(content, "Building", building_new)

with open("aether-royale.html", "w") as f:
    f.write(content)

