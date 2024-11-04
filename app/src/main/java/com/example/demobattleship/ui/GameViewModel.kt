package com.example.demobattleship.ui

import android.app.AlertDialog
import android.util.Log
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.demobattleship.ui.GameUiState
import com.google.gson.Gson
import com.google.gson.JsonElement
import com.google.gson.JsonObject
import com.google.gson.JsonParser
import com.google.gson.reflect.TypeToken
import io.socket.client.IO
import io.socket.client.Socket
import io.socket.emitter.Emitter
import io.socket.engineio.client.transports.WebSocket
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import okhttp3.OkHttpClient
import java.lang.RuntimeException
import java.net.URISyntaxException
import java.util.concurrent.TimeUnit

class GameViewModel: ViewModel() {
    private val _uiState = MutableStateFlow(GameUiState())
    val uiState: StateFlow<GameUiState> = _uiState.asStateFlow()
    private val _sid = MutableStateFlow<String>("")

    var gameStart: Boolean = false
    var socket: Socket
    val gson = Gson()
    val mapAdapter = gson.getAdapter(object: TypeToken<Map<String, Any?>>() {})
    val clientBuilder: OkHttpClient.Builder = OkHttpClient.Builder()
        // tăng thời gian timeout lên vô hạn để ko bị disconnect
        .connectTimeout(0, TimeUnit.MILLISECONDS)
        .readTimeout(0, TimeUnit.MILLISECONDS)
        .writeTimeout(0, TimeUnit.MILLISECONDS)
    init {
        try {
            val options = IO.Options().apply {
                timeout = 60000

                reconnectionAttempts = 3
                reconnectionDelay = 2000
                callFactory = clientBuilder.build()     // tăng thời gian timeout len vo han
//                transports = arrayOf(WebSocket.NAME)
            }
//            socket = IO.socket("https://stallion-special-lamb.ngrok-free.app", options)
                socket = IO.socket("http://192.168.88.212:5000", options)
        } catch (e: URISyntaxException) {
            Log.e("Socket", "URISyntaxException: ${e.message}")
            throw RuntimeException(e)
        }
    }

    @Synchronized
    fun connectSocket() {
        socket.on(Socket.EVENT_CONNECT) {
            Log.d("Socket", "Connected")
            if (_sid.value != "") {
                socket.emit("handle_data", _sid.value)

            }
        }.on(Socket.EVENT_CONNECT_ERROR) { args ->
            Log.e("Socket", "Connection Error: ${args[0]}")
            socket.connect()
        }
        Log.d("hihi","haha")
//        socket.connect()
    }

    fun receiveClientId(sid: String) {
        _sid.value = sid
    }

    @Synchronized
    fun disconnectSocket() {
        socket.disconnect()
    }

    @Synchronized
    fun sendRoomIdToServer(roomId: String, userName: String) {
        _uiState.value = _uiState.value.copy(room = roomId, name = userName)
//        val data: JsonObject = gson.fromJson(gson.toJson(_uiState.value), JsonObject::class.java)
        val data = JsonObject().apply {
            addProperty("name", _uiState.value.name)
            addProperty("room", _uiState.value.room)
        }
        val t = Gson().toJson(_uiState.value)
        socket.emit("check_room_to_join", gson.toJson(_uiState.value))
        Log.d("data", gson.toJson(_uiState.value))
    }

    @Synchronized
    fun addBot() {
        socket.emit("ready_to_start_bot", "add bot")
        _uiState.value = _uiState.value.copy(playWithBot = true)
    }

    fun oppJoin(oppName: String) {
        _uiState.value = _uiState.value.copy(
            oppName = oppName
        )
    }

    @Synchronized
    fun readyToStart() {
        if (_uiState.value.playWithBot) {
            socket.emit("ready_to_start_bot", "bot")
        }
        else {
            socket.emit("ready_to_start", "player")
        }
    }

    @Synchronized
    fun sendShipList(shipList: MutableList<JsonObject>) {
        val data = JsonObject()
        for (i in 0 until shipList.size) {
            data.add((i+1).toString(), shipList[i])
        }
        socket.emit("place_ship", data.toString())
        Log.d("send ship", "send thanh cong")
    }

    fun playingWithBot(): Boolean {
        return _uiState.value.playWithBot
    }

}
