import re

with open("aether-royale.html", "r") as f:
    content = f.read()

# 1. Update move logic
old_move_logic = """    moveTowardsTarget(dt) {
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

new_move_logic = """    moveTowardsTargetPos(goalX, goalY, dt) {
        let tx = goalX;
        let ty = goalY;

        if (!this.isAir) {
            let mySide = this.y > 15.5;
            let tSide = goalY > 15.5;
            if (mySide !== tSide) {
                if (!this.pathTimer || this.pathTimer <= 0 || !this.pathGoal || dist(this.pathGoal, {x: goalX, y: goalY}) > 2) {
                    let sx = Math.floor(this.x);
                    let sy = Math.floor(this.y);
                    let gx = Math.floor(goalX);
                    let gy = Math.floor(goalY);
                    
                    // Direct to bridge if moving to base
                    if (!this.target) {
                        let leftBridge = {x: 3.5, y: 15.5};
                        let rightBridge = {x: 13.5, y: 15.5};
                        let b = (dist(this, leftBridge) < dist(this, rightBridge)) ? leftBridge : rightBridge;
                        gx = Math.floor(b.x);
                        gy = Math.floor(b.y);
                    }
                    
                    this.path = aStar({x: sx, y: sy}, {x: gx, y: gy}, false);
                    this.pathTimer = 0.5; 
                    this.pathGoal = {x: goalX, y: goalY};
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
    }

    moveTowardsTarget(dt) {
        this.moveTowardsTargetPos(this.target.x, this.target.y, dt);
    }"""
content = content.replace(old_move_logic, new_move_logic)

# Fix the call when !this.target
old_no_target = """        if (!this.target) {
            // Move towards enemy base if no target in sight
            let tx = this.x;
            let ty = this.team === 1 ? 0 : ROWS;
            this.moveTowards(tx, ty, dt);
            return;
        }"""
new_no_target = """        if (!this.target) {
            let tx = this.x;
            let ty = this.team === 1 ? 0 : ROWS;
            this.moveTowardsTargetPos(tx, ty, dt);
            this.isMoving = true;
            return;
        }"""
content = content.replace(old_no_target, new_no_target)


with open("aether-royale.html", "w") as f:
    f.write(content)
