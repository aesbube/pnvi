extends Node3D

@onready var label = $HBoxContainer/Label
@onready var timerLabel = $HBoxContainer/TimerLabel
@onready var timer = $Timer
@onready var game_over_screen = $CanvasLayer/GameOverScreen
@onready var try_again_button = $CanvasLayer/GameOverScreen/VBoxContainer/TryAgainButton
@onready var win_screen = $CanvasLayer2/WinScreen
@onready var try_again_button_win = $CanvasLayer2/WinScreen/VBoxContainer/TryAgainButton

var time_left = 40
var game_over = false

func _ready() -> void:
	_update_timer_label()
	timer.start()
	Points.reset()
	Points.on_coin_pickup.connect(_on_coin_pickup)
	_on_coin_pickup()
	timer.timeout.connect(_on_timer_timeout)
	try_again_button.pressed.connect(_on_try_again_pressed)
	try_again_button_win.pressed.connect(_on_try_again_pressed)
	game_over_screen.visible = false
	win_screen.visible = false
	var screen_size = get_viewport().get_visible_rect().size
	game_over_screen.position = (screen_size - game_over_screen.size) / 2
	win_screen.position = (screen_size - win_screen.size) / 2

func _on_coin_pickup():
	label.text = "Points: " + str(Points.current)

func _on_timer_timeout() -> void:
	time_left -= 1
	_update_timer_label()

	if time_left <= 0:
		if Points.current < Points.MAX_POINTS:
			lost()
		else:
			won()
	if Points.current == Points.MAX_POINTS:
		won()

func _update_timer_label() -> void:
	timerLabel.text = "Time Left: " + str(time_left) + "s"

func _on_try_again_pressed() -> void:
	game_over = false  
	game_over_screen.visible = false
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	get_tree().reload_current_scene() 
	
func lost():
	timer.stop()
	game_over = true
	game_over_screen.visible = true
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	
func won():
	timer.stop()
	game_over = true
	win_screen.visible = true
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	
