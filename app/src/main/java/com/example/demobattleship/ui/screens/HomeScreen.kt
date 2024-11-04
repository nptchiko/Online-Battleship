package com.example.demobattleship.ui.screens

import android.annotation.SuppressLint
import android.app.AlertDialog
import android.content.Context
import android.content.pm.ActivityInfo
import android.util.Log
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentSize
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Divider
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat.getDrawable
import com.example.demobattleship.MainActivity
import com.example.demobattleship.R
import com.example.demobattleship.ui.GameViewModel
import com.example.demobattleship.ui.theme.DemoBattleShipTheme
import com.google.accompanist.drawablepainter.rememberDrawablePainter
import com.google.gson.Gson
import com.google.gson.JsonObject
import com.google.gson.JsonParser

fun checkValidRoomId(roomId: String): Boolean {
    if (roomId.length != 6) return false else {
        return try {
            roomId.toInt()
            true
        } catch(e: NumberFormatException) {
            false
        }
    }
}


@SuppressLint("StateFlowValueCalledInComposition")
@Composable
fun HomeScreen(
    context: Context,
    onNextButtonClicked: () -> Unit,
    gameViewModel: GameViewModel
) {
    var openAlertDialog by remember {
        mutableStateOf(false)
    }
    var roomId by remember {
        mutableStateOf("")
    }
    var userName by remember {
        mutableStateOf("")
    }
    var screenId by remember {
        mutableStateOf(0)
    }
    var status by remember {
        mutableStateOf("")
    }
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
//        verticalArrangement = Arrangement.SpaceBetween,
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 15.dp)
    ) {

        Box(contentAlignment = Alignment.BottomCenter) {
            Image(
                painter = painterResource(id = R.drawable.battleshiplogo),
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier.size(380.dp)
            )
            Image(
                painter = painterResource(id = R.drawable.battleshiptitle),
                contentDescription = null,
                modifier = Modifier.width(180.dp)
            )
        }
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceEvenly,
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 65.dp, vertical = 60.dp)
        ) {
            if (screenId == 1) {


                Button(
                    onClick = {
                        gameViewModel.addBot()
                        Log.d("addbot", "add bot")
                    /*TODO*/
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF234EC6), contentColor = Color.White),
                    shape = RoundedCornerShape(8.dp),
                    elevation = ButtonDefaults.buttonElevation(2.dp),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 15.dp)
                ) {
                    Text(text = stringResource(id = R.string.add_bot), fontWeight = FontWeight.Bold, fontSize = 17.sp)
                }
                Image(
                    painter = rememberDrawablePainter(
                        drawable = getDrawable(
                            context,
                            R.drawable.magnifying_glass
                        )
                    ),
                    contentDescription = null,
                    modifier = Modifier.size(50.dp)
                )
                Text(text = stringResource(id = R.string.waiting), fontSize = 17.sp)
            }
            else if (screenId == 0) {
                OutlinedTextField(
                    singleLine = true,
                    value = userName,
                    onValueChange = {userName = it},
                    label = { Text(text = "User Name")},
                    placeholder = { Text(text = "Enter your name")},
//                    modifier = Modifier.width(230.dp)
                    modifier = Modifier.padding(horizontal = 16.dp)
                )
                Row {

                }
                OutlinedTextField(
                    singleLine = true,
                    value = roomId,
                    onValueChange = {roomId = it},
                    label = { Text(text = stringResource(id = R.string.label))},
                    placeholder = { Text(text = stringResource(id = R.string.enter_room_id))},
                    supportingText = { Text(text = stringResource(id = R.string.support_text))},
                    isError = roomId != "" && !(roomId.length == 6 && checkValidRoomId(roomId)),
//                    modifier = Modifier.width(230.dp)
                    modifier = Modifier.padding(horizontal = 16.dp)
                )
                Button(
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF234EC6), contentColor = Color.White),
                    shape = RoundedCornerShape(8.dp),
                    enabled = (roomId.length == 6) && (checkValidRoomId(roomId)) && (userName != ""),
                    elevation = ButtonDefaults.buttonElevation(2.dp),
                    onClick = {

                        /*TODO*/
//                    (context as MainActivity)?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE

                        gameViewModel.sendRoomIdToServer(roomId = roomId, userName = userName)
                        gameViewModel.socket.on("room_status") { args ->
                            val data = JsonParser.parseString(args[0].toString()).asJsonObject
                            Log.d("receive from socket", data.toString())
                            status = data.get("status").asString
                            if (status == "00") {
                                openAlertDialog =  true
                                roomId = ""
                            }
                            else {
                                screenId = 1
                                if (status != "01") {
                                    val oppName = data.get("name").asString
                                    gameViewModel.oppJoin(data.get("name").asString)
                                    Log.d("opp name", oppName)

                                    // đã có opp trong phòng, show name của 2 players
                                    screenId = 2
                                }
                            }


                        }


                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 40.dp)
                ) {
                    Text(text = stringResource(id = R.string.join_room), fontWeight = FontWeight.Bold, fontSize = 17.sp)
                }
            }
            else {
                Log.d("ready to start", "đã đủ 2 players")

                Log.d("player1", "player1: " + gameViewModel.uiState.value.name)
                Log.d("player2", "player2: " + gameViewModel.uiState.value.oppName)
                Column(
                    modifier = Modifier.fillMaxSize(),
                    verticalArrangement = Arrangement.SpaceBetween,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Column (
                        modifier = Modifier.width(140.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                    ){
                        Text(
                            text = gameViewModel.uiState.value.name,
                            fontSize = 20.sp,
                            modifier = Modifier.fillMaxWidth(),
                            textAlign = TextAlign.Start

                        )
                        Image(
                            painter = painterResource(id = R.drawable.player_versus_player),
                            contentDescription = null,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier
                                .size(140.dp)
                                .fillMaxWidth()

                        )
                        Text(
                            text = gameViewModel.uiState.value.oppName,
                            fontSize = 20.sp,
                            modifier = Modifier.fillMaxWidth(),
                            textAlign = TextAlign.End

                        )
                    }

                    Button(
                        onClick = onNextButtonClicked
                    ) {
                        Text(text = "READY", fontWeight = FontWeight.Bold, fontSize = 22.sp)
                    }
                }
                
            }

        }

    }
    if (openAlertDialog) {
        AlertDialog(
            onDismissRequest = { openAlertDialog = false },
            confirmButton = {
                TextButton(onClick = { openAlertDialog = false }) {
                    Text(text = "Đóng")
                }
            },
            title = { Text("Phòng đã đầy", fontWeight = FontWeight.Bold, fontSize = 18.sp)},
            text = {
                Text("Vui lòng nhập ID khác")
                Log.d("alert dialog", "open")
            }
        )
    }
}



@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    DemoBattleShipTheme {
//        BoardScreen(board = DataResource().loadBoard())
//        HomeScreen(context = LocalContext.current)
    }
}