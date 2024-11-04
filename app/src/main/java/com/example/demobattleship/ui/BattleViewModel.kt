package com.example.demobattleship.ui

import android.util.Log
import androidx.lifecycle.ViewModel
import com.example.demobattleship.data.model.CoorGameState
import com.example.demobattleship.data.model.CoorPlaceShip
import com.example.demobattleship.data.model.TurnState
import com.google.gson.JsonObject
import com.google.gson.JsonParser
import io.socket.client.Socket
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class BattleViewModel: ViewModel() {
    private val _turnState = MutableStateFlow(TurnState())
    val turnState: StateFlow<TurnState> = _turnState.asStateFlow()

    private val _yourBoard = MutableStateFlow(MutableList(10) {MutableList<CoorGameState> (10) { CoorGameState() } })
    val yourBoard: StateFlow<MutableList<MutableList<CoorGameState>>> = _yourBoard.asStateFlow()

    private val _oppBoard = MutableStateFlow(MutableList(10) {MutableList<CoorGameState> (10) { CoorGameState() } })
    val oppBoard: StateFlow<MutableList<MutableList<CoorGameState>>> = _oppBoard.asStateFlow()

    fun updateTurn() {
        _turnState.value = _turnState.value.copy(
            yourTurn = true
        )
        Log.d("turn: ", "player")
    }

    @Synchronized
    fun listenShootResult(socket: Socket) {
        socket.off("update_context")
        socket.on("update_context") { args ->
            val data = JsonParser.parseString(args[0].toString()).asJsonObject
            Log.d("received data", data.toString())

            val context = data.get("context").asJsonObject
            val coord = context.get("coord").asJsonArray
            val x = coord[0].asInt
            val y = coord[1].asInt
            val result = context.get("result").asBoolean
            val myTurn = data.get("my_turn").asBoolean

            if (myTurn) {
                _oppBoard.value[x][y] = _oppBoard.value[x][y].copy(
                    shipType = if (result) 1 else -1
                )
            } else {
                _yourBoard.value[x][y] = _yourBoard.value[x][y].copy(
                    shipType = if (result) 1 else -1
                )
                Log.d("bot ban", "bot ban")
            }

            if (result == false) {
                _turnState.value = _turnState.value.copy(
                    yourTurn = !myTurn
                )
            }
        }
    }

    @Synchronized
    fun shootBot(x: Int, y: Int, socket: Socket) {
        val dataEmit = JsonObject().apply {
            addProperty("x", x)
            addProperty("y", y)
        }
        socket.emit("shoot_bot", dataEmit.toString())
        Log.d("shoot bot", "success")
    }
}