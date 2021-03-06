var camera, scene, renderer;
var geometry, material, mesh, csgMesh, ballMesh;
var pausing = false;
var velocityX = 0, velocityY = 0;
var halfWidth = window.innerWidth / 2;
var halfHeight = window.innerHeight / 2;
var meshes = [];

window.onload = function(){
	init();
	animate();
};

function getMaterial(){
  var material = new THREE.MeshNormalMaterial();
  material.transparent = true;
  material.opacity = 1.0;
  material.depthTest = true;
  material.depthWrite = false;
  return material;
}

function makeHaloObject(shapeFunc, ratio){
  var outerShape = new shapeFunc(10, 0);
  var innerShape = new shapeFunc(10*ratio, 0);
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

function makeShaders(){
  var material = new THREE.RawShaderMaterial( {
			vertexShader: document.getElementById( 'vertexShader' ).textContent,
			fragmentShader: document.getElementById( 'fragmentShader' ).textContent
		});
    material.transparent = true;
    material.opacity = 0.8;
    material.depthTest = true;
    material.depthWrite = false;
    return material;
}

// Please Use Spherical Coordinates to denote the hole locations
const HOLE_COORDINATES = [
	[
		0 * Math.PI,
		0 * Math.PI
	],[
		Math.PI * 0.50,
		0
	],[
		0,
		Math.PI * 0.50
	],[
		0,
		Math.PI * 0.25
	],[
		0,
		Math.PI * 0.75
	]
];

function init() {
	camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.1, 100 );
	camera.position.z = 20;

	scene = new THREE.Scene();

	var axesHelper = new THREE.AxesHelper( 20 );
	scene.add( axesHelper );

	sphere = new THREE.SphereGeometry( 10, 32, 32 );
  //sphere.computeVertexNormals();
	sphereMesh = new THREE.Mesh( sphere );
	spherebsp = new ThreeBSP(sphere);

	var nextBsp = spherebsp;
	HOLE_COORDINATES.forEach( function(hole){
		nextBsp = pokeHole( nextBsp, 10, hole );
	});
	csgMesh = nextBsp.toMesh();
	csgMesh.material = new THREE.MeshNormalMaterial();
	/*
	csgMesh.material.opacity = 0.1;
	csgMesh.material.depthTest = true;
	csgMesh.material.depthWrite = false;
	*/
	scene.add( csgMesh );

	makeBall();

	renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setSize( window.innerWidth, window.innerHeight );
	document.body.appendChild( renderer.domElement );

}

function pokeHole(shapebsp, extent, coordinates){
	//var hole = new THREE.SphereGeometry( 0.6, 32, 32 );
	var hole = new THREE.CylinderGeometry( 0.6, 0.6, 2 * extent, 32 );
	var holeMesh = new THREE.Mesh( hole );

	holeMesh.rotation.x = coordinates[1] + (Math.PI / 2);
	holeMesh.rotation.z = coordinates[0];

	var holebsp = new ThreeBSP(holeMesh);
	return shapebsp.subtract(holebsp);
}

function makeBall(){
	ball = new THREE.SphereGeometry( 0.5, 32, 32 );
	ballMesh = new THREE.Mesh( ball );
	ballMesh.material = new THREE.MeshNormalMaterial();
	scene.add(ballMesh);
	ballMesh.position.set(0, 0, 11);
}



var TWOPI = Math.PI * 2;

function animate() {
	requestAnimationFrame( animate );

	csgMesh.rotation.x = (csgMesh.rotation.x + velocityX) % TWOPI;
	csgMesh.rotation.y = (csgMesh.rotation.y + velocityY) % TWOPI;

	ballMesh.position.y = -velocityX * 30;
	ballMesh.position.x = velocityY * 30;

	evaluateCollision();

	renderer.render( scene, camera );
}


var THRESHOLD = 0.5;

function evaluateCollision(){
	var xDist = Math.abs(csgMesh.rotation.x - HOLE_COORDINATES[0])
	var yDist = Math.abs(csgMesh.rotation.y - HOLE_COORDINATES[1])
	var zDist = Math.abs(csgMesh.rotation.z - HOLE_COORDINATES[2])

	if( (xDist < THRESHOLD && yDist < THRESHOLD) ||
	    (xDist < THRESHOLD && zDist < THRESHOLD) ||
	    (yDist < THRESHOLD && zDist < THRESHOLD) ){
		console.log("HIT");
		pausing = true;
		// do animations
	}
}

window.onmousemove = function(ev){
	if( !pausing ){
		velocityY = (halfWidth - ev.clientX) / -10000;
		velocityX = (halfHeight - ev.clientY) / -10000;
	}
}
