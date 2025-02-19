extends CharacterBody3D


const SPEED = 5.0
const JUMP_VELOCITY = 4.5
const SENSITIVITY = 0.0025
@onready var character_skin = $CharacterSkin
@export var stopping_speed := 1.0
@export var move_speed := 6.0

func _ready():
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _unhandled_input(event):
	if event is InputEventMouseMotion:
		rotate_y(-event.relative.x * SENSITIVITY)

func _physics_process(delta: float) -> void:
	if is_game_over():
		velocity = Vector3.ZERO
		return 
	if not is_on_floor():
		velocity += get_gravity() * delta
	var is_just_jumping = Input.is_action_just_pressed("jump") and is_on_floor()
	if is_just_jumping:
		velocity.y = JUMP_VELOCITY

	var input_dir := Input.get_vector("left", "right", "forward", "backward")
	var direction := (transform.basis * Vector3(input_dir.x, 0, -input_dir.y)).normalized()
	if direction:
		velocity.x = direction.x * SPEED
		velocity.z = direction.z * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)
		velocity.z = move_toward(velocity.z, 0, SPEED)
		
	if is_just_jumping:
		character_skin.jump()
	elif not is_on_floor() and velocity.y < 0:
		character_skin.fall()
	elif is_on_floor():
		var xz_velocity := Vector3(velocity.x, 0, velocity.z)
		if xz_velocity.length() > stopping_speed:
			character_skin.set_moving(true)
			character_skin.set_moving_speed(
				inverse_lerp(0.0, move_speed, xz_velocity.length())
			)
		else:
			character_skin.set_moving(false)

	move_and_slide()

func is_game_over() -> bool:
	return get_tree().current_scene.find_child("GameOverScreen").visible or get_tree().current_scene.find_child("WinScreen").visible
