var camera, scene, renderer;
var geometry, material, mesh, csgMesh;

window.onload = function(){
	init();
	animate();
};

function init() {

	camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.01, 10 );
	camera.position.z = 3;

	scene = new THREE.Scene();

	sphere = new THREE.SphereGeometry( 1, 32, 32 );
	sphereMesh = new THREE.Mesh( sphere );
	spherebsp = new ThreeBSP(sphere);
	
	hole = new THREE.CylinderGeometry( 0.1, 0.1, 2, 32 );
	holeMesh = new THREE.Mesh( hole );
	holebsp = new ThreeBSP(hole);

	csgMesh = spherebsp.subtract(holebsp).toMesh();
	csgMesh.material = new THREE.MeshNormalMaterial();

	scene.add( csgMesh );

	renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setSize( window.innerWidth, window.innerHeight );
	document.body.appendChild( renderer.domElement );

}

function animate() {

	requestAnimationFrame( animate );

	csgMesh.rotation.x += 0.01;
	csgMesh.rotation.y += 0.02;

	renderer.render( scene, camera );

}


