const canvas = document.getElementById('bg-canvas');
const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 30;

const particleCount = 300;
const positions = new Float32Array(particleCount * 3);
for (let i = 0; i < particleCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 80;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 80;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 80;
}
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
const particleMat = new THREE.PointsMaterial({
    color: 0x82b1ff,
    size: 0.5,
    transparent: true,
    opacity: 0.7
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);

const spheres = [];
const sphereColors = [0x82b1ff, 0xb388ff, 0x64ffda];
for (let i = 0; i < 3; i++) {
    const geo = new THREE.SphereGeometry(4, 32, 32);
    const mat = new THREE.MeshBasicMaterial({
        color: sphereColors[i],
        transparent: true,
        opacity: 0.08
    });
    const sphere = new THREE.Mesh(geo, mat);
    sphere.position.set(
        (Math.random() - 0.5) * 40,
        (Math.random() - 0.5) * 40,
        (Math.random() - 0.5) * 20 - 10
    );
    scene.add(sphere);
    spheres.push(sphere);
}

let mouseX = 0, mouseY = 0;
document.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
});

function animate() {
    requestAnimationFrame(animate);

    particles.rotation.y += 0.0006;
    particles.rotation.x += 0.0002;

    spheres.forEach((s, i) => {
        s.position.y += Math.sin(Date.now() * 0.0003 + i) * 0.01;
    });

    camera.position.x += (mouseX * 5 - camera.position.x) * 0.02;
    camera.position.y += (-mouseY * 5 - camera.position.y) * 0.02;
    camera.lookAt(scene.position);

    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});