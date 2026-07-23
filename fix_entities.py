import re

with open("aether-royale.html", "r") as f:
    content = f.read()

# Fix Tower
tower_draw = """    draw(ctx) {
        let offsetX = (cw - COLS * cellSize) / 2;
        let offsetY = (ch - ROWS * cellSize) / 2;
        let r = this.radius * cellSize;
        
        if (this.mesh) {
            let px = this.x * cellSize + offsetX;
            let py = this.y * cellSize + offsetY;
            this.mesh.position.set(px, ch - py, 0);
            this.mesh.rotation.x = -Math.PI / 6;
        }
        
        if (this.hp < this.maxHp) {
            drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
        }
    }"""
tower_draw_new = """    updateMesh() {
        let offsetX = (cw - COLS * cellSize) / 2;
        let offsetY = (ch - ROWS * cellSize) / 2;
        if (this.mesh) {
            let px = this.x * cellSize + offsetX;
            let py = this.y * cellSize + offsetY;
            this.mesh.position.set(px, ch - py, 0);
            this.mesh.rotation.x = -Math.PI / 6;
        }
    }
    
    draw(ctx) {
        let r = this.radius * cellSize;
        if (this.hp < this.maxHp) {
            drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
        }
    }"""
content = content.replace(tower_draw, tower_draw_new)

# Fix Troop
troop_draw = """    draw(ctx) {
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
            
            this.mesh.position.set(px, ch - visualY, 0);
            
            let rotZ = 0;
            if (this.target) {
                let dx = this.target.x - this.x;
                let dy = this.target.y - this.y;
                let angle = Math.atan2(dy, dx);
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
        
        if (this.hp < this.maxHp) {
            drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
        }
    }"""
troop_draw_new = """    updateMesh() {
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
            
            this.mesh.position.set(px, ch - visualY, 0);
            
            let rotZ = 0;
            if (this.target) {
                let dx = this.target.x - this.x;
                let dy = this.target.y - this.y;
                let angle = Math.atan2(dy, dx);
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
    }

    draw(ctx) {
        let r = this.radius * cellSize;
        if (this.hp < this.maxHp) {
            drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
        }
    }"""
content = content.replace(troop_draw, troop_draw_new)

# Fix Building
building_draw = """    draw(ctx) {
        let offsetX = (cw - COLS * cellSize) / 2;
        let offsetY = (ch - ROWS * cellSize) / 2;
        let r = this.radius * cellSize;
        
        if (this.mesh) {
            let px = this.x * cellSize + offsetX;
            let py = this.y * cellSize + offsetY;
            this.mesh.position.set(px, ch - py, 0);
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
        
        if (this.hp < this.maxHp) {
            drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
        }
    }"""
building_draw_new = """    updateMesh() {
        let offsetX = (cw - COLS * cellSize) / 2;
        let offsetY = (ch - ROWS * cellSize) / 2;
        if (this.mesh) {
            let px = this.x * cellSize + offsetX;
            let py = this.y * cellSize + offsetY;
            this.mesh.position.set(px, ch - py, 0);
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
    }

    draw(ctx) {
        let r = this.radius * cellSize;
        if (this.hp < this.maxHp) {
            drawHpBar(ctx, this.x * cellSize, this.y * cellSize - r - 10, this.hp, this.maxHp, this.level);
        }
    }"""
content = content.replace(building_draw, building_draw_new)

with open("aether-royale.html", "w") as f:
    f.write(content)
