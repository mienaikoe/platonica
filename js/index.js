var camera, scene, renderer;
var geometry, material, mesh;

init();
animate();

function init() {

	if( typeof(THREE) === 'undefined' ){
		setTimeout( init, 100 );
		return;
	} 

	camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.01, 10 );
	camera.position.z = 3;

	scene = new THREE.Scene();

	sphere = new THREE.SphereGeometry( 1, 1, 1 );
	hole = new THREE.CylinderGeometry( 1, 1, 3, 32 );

	sphereMesh = new THREE.Mesh( sphere );
	holeMesh = new THREE.Mesh( hole );
	spherebsp = new ThreeBSP(sphere);
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

	//mesh.rotation.x += 0.01;
	//mesh.rotation.y += 0.02;

	renderer.render( scene, camera );

}


