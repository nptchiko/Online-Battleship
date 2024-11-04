package com.example.demobattleship.data.model

data class CoorPlaceShip(
    val index: Int = 0,
    val selected: Boolean = false,      // khong can thiet lam
    val direction: Boolean = false,     // false là dọc, true là ngang
    val typeShip: Int = 0,
)