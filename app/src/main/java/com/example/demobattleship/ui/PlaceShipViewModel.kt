package com.example.demobattleship.ui

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import com.example.demobattleship.data.model.CoorPlaceShip
import com.example.demobattleship.data.model.PlaceShipState
import com.google.gson.JsonObject
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class PlaceShipViewModel: ViewModel() {
    var shipList: MutableList<JsonObject> = mutableListOf()

    private val _gameStartConfirmed = MutableStateFlow(false)
    val gameStartConfirmed: StateFlow<Boolean> = _gameStartConfirmed.asStateFlow()

    fun confirmGameStart() {
        _gameStartConfirmed.value = true
    }

    private val _inWaiting = MutableStateFlow(false)
    val inWaiting: StateFlow<Boolean> = _inWaiting.asStateFlow()

    fun updateInWaiting() {
        _inWaiting.value = true
    }

    private val _placeShipBoard = MutableStateFlow(MutableList(10) {MutableList<CoorPlaceShip> (10) { CoorPlaceShip() } })
    val placeShipBoard: StateFlow<MutableList<MutableList<CoorPlaceShip>>> = _placeShipBoard.asStateFlow()

    private val _selectedCoor = MutableStateFlow(PlaceShipState())
    val selectedCoor: StateFlow<PlaceShipState> = _selectedCoor.asStateFlow()

    fun selectCoor(input: String) {
        _selectedCoor.value = _selectedCoor.value.copy(selectedCoor = input)
    }


    fun selectCoorToPlace(typeShip: Int, direction: Boolean): Boolean {
        if (_selectedCoor.value.selectedCoor.length != 2) return false
        val x = _selectedCoor.value.selectedCoor[0] - 'A'
        val y = _selectedCoor.value.selectedCoor[1] - '0'
        if (direction) {
            if (x + typeShip - 1 > 9) return false
            for (i in 0 until typeShip) {
                if (_placeShipBoard.value[x + i][y].selected) return false
            }
        } else {
            if (y + typeShip - 1 > 9) return false
            for (i in 0 until typeShip) {
                if (_placeShipBoard.value[x][y + i].selected) return false
            }
        }

        _placeShipBoard.value[x][y] = _placeShipBoard.value[x][y].copy(index = 1, selected = true, direction = direction, typeShip = typeShip)

        if (direction) {
            for (i in 1 until typeShip) {
                _placeShipBoard.value[x + i][y] = _placeShipBoard.value[x + i][y].copy(index = 1 + i, selected = true, direction = direction, typeShip = typeShip)
            }
        } else {
            for (i in 1 until typeShip) {
                _placeShipBoard.value[x][y + i] = _placeShipBoard.value[x][y + i].copy(index = 1 + i, selected = true, direction = direction, typeShip = typeShip)
            }
        }

        // add ship to list
        val innerJson = JsonObject().apply {
            addProperty("len", typeShip)
            val coorJson = JsonObject().apply {
                addProperty("x", x)
                addProperty("y", y)
            }
            add("coord", coorJson)
            addProperty("dir", if (direction) 1 else 2)
        }
        shipList.add(innerJson)


        return true // dat tau hop le
    }


}