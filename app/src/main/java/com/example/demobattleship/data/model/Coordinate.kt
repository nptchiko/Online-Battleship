package com.example.demobattleship.data.model

import androidx.compose.runtime.MutableState
import androidx.compose.runtime.Stable
import androidx.compose.runtime.mutableStateOf

@Stable
class Coordinate(
    val isShip: Boolean,
    var selected: MutableState<Boolean> = mutableStateOf(false),
    val x: Int,
    val y: Int
) {
    fun select() {
        if (!selected.value) {
            selected.value = true;
        }
    }
}