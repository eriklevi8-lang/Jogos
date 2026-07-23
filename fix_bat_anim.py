import re

with open("aether-royale.html", "r") as f:
    content = f.read()

anim_old = """            } else if (this.isAir) {
                visualY += Math.sin(globalTime * 4) * (r * 0.2);
            }"""

anim_new = """            } else if (this.isAir) {
                visualY += Math.sin(globalTime * 4) * (r * 0.2);
                let wL = this.mesh.getObjectByName('wingL');
                let wR = this.mesh.getObjectByName('wingR');
                if (wL && wR) {
                    wL.rotation.y = Math.sin(globalTime * 20) * 0.8;
                    wR.rotation.y = -Math.sin(globalTime * 20) * 0.8;
                }
            }"""

content = content.replace(anim_old, anim_new)

with open("aether-royale.html", "w") as f:
    f.write(content)
