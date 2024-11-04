package com.example.demobattleship.data.model

import androidx.compose.runtime.MutableState
import androidx.compose.runtime.Stable
import androidx.compose.runtime.mutableStateOf

@Stable
class Ship(
    var coordinate: MutableState<Pair<Int, Int>> = mutableStateOf(Pair(-1, -1)),
    val length: Int = 1,
    var direction: MutableState<Direction> = mutableStateOf(Direction.EAST)
) {
    fun rotate() {
        this.direction.value = Direction.values()[(this.direction.value.value + 1) % 4]
    }
    fun placeShip(x: Int, y: Int) {
        this.coordinate.value = Pair(x, y)
        /* TODO */
    }
}