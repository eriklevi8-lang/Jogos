import re

with open("aether-royale.html", "r") as f:
    content = f.read()

# 1. Scale up troops
troop_scale_old = """    // Scale up overall size to make models much bigger
    let r = entity.radius * cellSize * 1.6;"""
troop_scale_new = """    // Scale up overall size to make models much bigger
    let r = entity.radius * cellSize * 2.5;"""
content = content.replace(troop_scale_old, troop_scale_new)

# 2. Fix Bat model
bat_old = """    } else if (cardId === 'dracos') {
        // Detailed Bat (Morcego)
        const mat = new THREE.MeshLambertMaterial({color: 0x4c1d95, side: THREE.DoubleSide}); // dark purple bat
        const body = new THREE.Mesh(new THREE.SphereGeometry(r*0.4, 8, 8), mat);
        body.position.z = -r*0.5;
        group.add(body);
        const ears = new THREE.Mesh(new THREE.ConeGeometry(r*0.2, r*0.4, 4), mat);
        ears.position.set(r*0.2, 0, -r*0.8);
        group.add(ears);
        const ears2 = new THREE.Mesh(new THREE.ConeGeometry(r*0.2, r*0.4, 4), mat);
        ears2.position.set(-r*0.2, 0, -r*0.8);
        group.add(ears2);
        const wingMat = new THREE.MeshLambertMaterial({color: 0x2e1065, side: THREE.DoubleSide});
        const wingL = new THREE.Mesh(new THREE.PlaneGeometry(r*1.5, r*0.8), wingMat);
        wingL.position.set(-r*0.8, 0, -r*0.5);
        group.add(wingL);
        const wingR = new THREE.Mesh(new THREE.PlaneGeometry(r*1.5, r*0.8), wingMat);
        wingR.position.set(r*0.8, 0, -r*0.5);
        group.add(wingR);
    }"""
bat_new = """    } else if (cardId === 'dracos') {
        // Detailed Bat (Morcego)
        const mat = new THREE.MeshLambertMaterial({color: 0x3b0764, side: THREE.DoubleSide});
        const wingMat = new THREE.MeshLambertMaterial({color: 0x1e1b4b, side: THREE.DoubleSide});
        const bodyGeo = new THREE.BoxGeometry(r*0.6, r*0.8, r*0.6);
        const body = new THREE.Mesh(bodyGeo, mat);
        body.position.z = -r*0.5;
        group.add(body);
        const headGeo = new THREE.BoxGeometry(r*0.5, r*0.5, r*0.5);
        const head = new THREE.Mesh(headGeo, mat);
        head.position.set(0, r*0.6, -r*0.5);
        group.add(head);
        const wingL = new THREE.Mesh(new THREE.BoxGeometry(r*1.8, r*0.8, r*0.1), wingMat);
        wingL.position.set(-r*1.2, 0, -r*0.5);
        wingL.name = "wingL"; // for animation
        group.add(wingL);
        const wingR = new THREE.Mesh(new THREE.BoxGeometry(r*1.8, r*0.8, r*0.1), wingMat);
        wingR.position.set(r*1.2, 0, -r*0.5);
        wingR.name = "wingR";
        group.add(wingR);
        const earGeo = new THREE.ConeGeometry(r*0.15, r*0.4, 4);
        const earL = new THREE.Mesh(earGeo, mat);
        earL.position.set(-r*0.2, r*0.9, -r*0.5);
        group.add(earL);
        const earR = new THREE.Mesh(earGeo, mat);
        earR.position.set(r*0.2, r*0.9, -r*0.5);
        group.add(earR);
        const eyeMat = new THREE.MeshLambertMaterial({color: 0xef4444});
        const eyeL = new THREE.Mesh(new THREE.BoxGeometry(r*0.1, r*0.1, r*0.1), eyeMat);
        eyeL.position.set(-r*0.15, r*0.7, -r*0.7);
        group.add(eyeL);
        const eyeR = new THREE.Mesh(new THREE.BoxGeometry(r*0.1, r*0.1, r*0.1), eyeMat);
        eyeR.position.set(r*0.15, r*0.7, -r*0.7);
        group.add(eyeR);
    }"""
content = content.replace(bat_old, bat_new)

with open("aether-royale.html", "w") as f:
    f.write(content)
