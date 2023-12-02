extends StaticBody3D

@export var start_distance = -3.0
@export var start_rotation = -1080 # 3 rotations

var intro_countdown = Global.intro_duration
var is_spinning = true

# Called when the node enters the scene tree for the first time.
func _ready():
	rotation_degrees.y = start_rotation
	position.z = start_distance
	print("Ready ", rotation_degrees.y)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
	
func _physics_process(delta: float) -> void:
	if( !is_spinning ):
		return
		
	intro_countdown -= delta
		
	if( intro_countdown <= 0  ):
		print("Stopping Intro")
		is_spinning = false
		rotation_degrees.z = 0
		position.z = 0
		return
		
	var intro_ratio = pow(intro_countdown / Global.intro_duration, 2);
	
	rotation_degrees.y = intro_ratio * start_rotation;
	position.z = intro_ratio * start_distance;
	
