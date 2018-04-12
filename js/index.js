var camera, scene, renderer;
var geometry, material, mesh, worldMesh, csgMesh, ballMesh;

var velocityX = 0, velocityY = 0;
var halfWidth = window.innerWidth / 2;
var halfHeight = window.innerHeight / 2;



window.onload = function(){
	init();
	animate();
};

const HOLE_COORDINATES = [
	0 * Math.PI, 
	0 * Math.PI, 
	0 * Math.PI
];

function init() {
	camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.1, 100 );
	camera.position.z = 20;

	scene = new THREE.Scene();

	var world = new THREE.CubeGeometry( 100, 100, 100 );
	worldMesh = new THREE.Mesh( world );
	worldMesh.material = new THREE.MeshBasicMaterial();

	sphere = new THREE.SphereGeometry( 10, 32, 32 );
	sphereMesh = new THREE.Mesh( sphere );
	spherebsp = new ThreeBSP(sphere);
	
	var pokedbsp = pokeHole( spherebsp, 10, HOLE_COORDINATES );

	csgMesh = pokedbsp.toMesh();
	csgMesh.parent = worldMesh;
	csgMesh.material = new THREE.MeshNormalMaterial();

	scene.add( csgMesh );

	makeBall();

	renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setSize( window.innerWidth, window.innerHeight );
	document.body.appendChild( renderer.domElement );

}

function pokeHole(shapebsp, extent, coordinates){
	var hole = new THREE.CylinderGeometry( 0.6, 0.6, extent*2, 32 );
	var holeMesh = new THREE.Mesh( hole );
	// TODO: position and rotation aren't working
	holeMesh.position.x = extent;
	holeMesh.rotation.x = coordinates[0] * Math.PI;
	holeMesh.rotation.y = coordinates[1] * Math.PI;
	holeMesh.rotation.z = coordinates[2] * Math.PI;
	var holebsp = new ThreeBSP(hole);
	return shapebsp.subtract(holebsp);
}

function makeBall(){
	ball = new THREE.SphereGeometry( 0.5, 32, 32 );
	ballMesh = new THREE.Mesh( ball );
	ballMesh.material = new THREE.MeshNormalMaterial();
	ballMesh.parent = worldMesh;
	scene.add(ballMesh);
	ballMesh.position.set(0, 0, 11);
}


function animate() {
	requestAnimationFrame( animate );

	worldMesh.rotation.copy( csgMesh.rotation );
	csgMesh.rotation.x += velocityX;
	csgMesh.rotation.y += velocityY;
	
	ballMesh.position.y = -velocityX * 30;
	ballMesh.position.x = velocityY * 30;

	evaluateCollision();

	renderer.render( scene, camera );
}

function evaluateCollision(){
	if( Math.abs(csgMesh.rotation.x - HOLE_COORDINATES[0]) < 0.1 &&
	    Math.abs(csgMesh.rotation.y - HOLE_COORDINATES[1]) < 0.1 ){
		console.log("HIT");
	}
}

window.onmousemove = function(ev){
	velocityY = (halfWidth - ev.clientX) / -10000;
	velocityX = (halfHeight - ev.clientY) / -10000;
}

