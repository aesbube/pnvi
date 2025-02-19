extends Node

signal on_coin_pickup
const MAX_POINTS = 10
var current = 0

func pickup():
	current += 1
	on_coin_pickup.emit()

func reset():
	current = 0
