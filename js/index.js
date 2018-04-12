var camera, scene, renderer;
var geometry, material;
var meshes = [];

window.onload = function(){
	init();
	animate();
};

function getMaterial(){
  var material = new THREE.MeshNormalMaterial();
  material.transparent = true;
  material.opacity = 0.8;
  material.depthTest = true;
  material.depthWrite = false;
  return material;
}

function makeHaloObject(shapeFunc, ratio){
  var outerShape = new shapeFunc(1, 0);
  var innerShape = new shapeFunc(ratio, 0);
  return (new ThreeBSP(outerShape)).subtract(new ThreeBSP(innerShape));
}

function makeHaloCube(ratio){
  var outerCube = new ThreeBSP(new THREE.BoxGeometry(1, 1, 1));
  var innerCube = new ThreeBSP(new THREE.BoxGeometry(ratio, ratio, ratio));
  return outerCube.subtract(innerCube);
}

function makeShapes(haloRatio){
  var shapes = [
    makeHaloObject(THREE.TetrahedronGeometry, haloRatio),
    makeHaloCube(haloRatio),
    makeHaloObject(THREE.OctahedronGeometry, haloRatio),
    makeHaloObject(THREE.IcosahedronGeometry, haloRatio),
    makeHaloObject(THREE.DodecahedronGeometry, haloRatio)
  ];
  var dx = -2;
  var dy = 1;
  for(var i in shapes){
    var mesh = shapes[i].toMesh();
    mesh.material = getMaterial();
    mesh.geometry.translate(dx, dy, 0);
    meshes.push(mesh);
    dx += 2
    if(i==2){
      dx = -2;
      dy -= 2;
    }
  }

}

function init() {

	camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.01, 10 );
	camera.position.z = 3;

	scene = new THREE.Scene();

  makeShapes(0.85);
  for(var m in meshes){
    scene.add(meshes[m]);
  }

	renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setSize( window.innerWidth, window.innerHeight );
	document.body.appendChild( renderer.domElement );

}

function animate() {

	requestAnimationFrame( animate );

  for(var m in meshes){
    var mesh = meshes[m];
    mesh.rotation.x += 0.01;
    mesh.rotation.y += 0.02;
  }

	renderer.render( scene, camera );

}
