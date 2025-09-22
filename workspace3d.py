<html>
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
let scene = new THREE.Scene();
let camera = new THREE.PerspectiveCamera(75,window.innerWidth/window.innerHeight,0.1,1000);
let renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Scroll panel = Lettera code block
function createScroll(text,x,y,z) {
  let geometry = new THREE.PlaneGeometry(2,1);
  let material = new THREE.MeshBasicMaterial({color:0xffffff});
  let scroll = new THREE.Mesh(geometry, material);
  scroll.position.set(x,y,z);
  scene.add(scroll);
  return scroll;
}

let scroll = createScroll("Persistent Equation: Counter = 0",0,1,-5);

camera.position.z = 5;
function animate(){
  requestAnimationFrame(animate);
  renderer.render(scene,camera);
}
animate();
</script>
</head>
<body></body>
</html>

<script src="https://cdn.jsdelivr.net/npm/three/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/cannon/build/cannon.min.js"></script>
<script>
let world = new CANNON.World();
world.gravity.set(0,-9.82,0);

// Floor
let groundBody = new CANNON.Body({ mass:0 });
let groundShape = new CANNON.Plane();
groundBody.addShape(groundShape);
world.addBody(groundBody);

// Ball
let ballBody = new CANNON.Body({ mass:1 });
let ballShape = new CANNON.Sphere(1);
ballBody.addShape(ballShape);
ballBody.position.set(0,5,0);
world.addBody(ballBody);

// Render loop
function animate(){
  world.step(1/60);
  if(ballBody.position.y < 0){
    console.log("Ball hit the floor!");
  }
  requestAnimationFrame(animate);
}
animate();
</script>

