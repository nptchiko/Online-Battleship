package com.example.demobattleship.data

import com.example.demobattleship.data.model.Coordinate
import com.example.demobattleship.data.model.Ship

class DataResource {
    fun loadBoard(): List<Coordinate> {
        val board = mutableListOf<Coordinate>()
        for (row in 0..9) {
            for (col in 0..9) {
                board.add(Coordinate(x = row, y = col, isShip =  (row * 10 + col) % 6 == 0))
            }
        }
        return board
    }

    fun loadInitialShip(): List<Ship> {
        return listOf<Ship>(
            Ship(),
            Ship(),
            Ship(),
            Ship(),
            Ship()
        )
    }
}