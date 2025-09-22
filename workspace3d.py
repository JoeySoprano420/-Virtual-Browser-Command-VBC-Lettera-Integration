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
