package com.example.demobattleship.data.model

import androidx.compose.runtime.MutableState

enum class Direction(val value: Int) {
    NORTH(0),
    EAST(1),
    SOUTH(2),
    WEST(3);

    val next: Direction
        get() = values()[(this.ordinal + 1) % values().size]
}
