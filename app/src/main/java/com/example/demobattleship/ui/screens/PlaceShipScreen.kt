package com.example.demobattleship.ui.screens

import android.annotation.SuppressLint
import android.content.ClipData
import android.content.ClipDescription
import android.content.Context
import android.content.Intent
import android.content.pm.ActivityInfo
import android.content.res.Configuration
import androidx.annotation.DrawableRes
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.draganddrop.dragAndDropSource
import androidx.compose.foundation.draganddrop.dragAndDropTarget
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.foundation.layout.wrapContentSize
import androidx.compose.foundation.layout.wrapContentWidth
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Divider
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draganddrop.DragAndDropEvent
import androidx.compose.ui.draganddrop.DragAndDropTarget
import androidx.compose.ui.draganddrop.DragAndDropTransferData
import androidx.compose.ui.draganddrop.mimeTypes
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.demobattleship.MainActivity
import com.example.demobattleship.R
import com.example.demobattleship.data.DataResource
import com.example.demobattleship.data.model.Coordinate
import com.example.demobattleship.data.model.Ship
import com.example.demobattleship.ui.GameViewModel
import com.example.demobattleship.ui.PlaceShipViewModel
import com.example.demobattleship.ui.theme.DemoBattleShipTheme
import java.security.cert.TrustAnchor

@DrawableRes
fun getImage(typeShip: Int, index: Int): Int {
    return when (typeShip) {
        1 -> R.drawable.tau_1_01
        2 -> when (index) {
            1 -> R.drawable.tau_2_01
            else -> R.drawable.tau_2_02
        }
        3 -> when (index) {
            1 -> R.drawable.tau_3_01
            2 -> R.drawable.tau_3_02
            else -> R.drawable.tau_3_03
        }
        else -> when (index) {
            1 -> R.drawable.tau_4_01
            2 -> R.drawable.tau_4_02
            3 -> R.drawable.tau_4_03
            else -> R.drawable.tau_4_04
        }
    }
}

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun BoardScreen(placeShipViewModel: PlaceShipViewModel) {
    val board by placeShipViewModel.placeShipBoard.collectAsState()
    LazyVerticalGrid(
        columns = GridCells.Fixed(10),
        modifier = Modifier
            .height(252.dp)
            .width(252.dp),
        horizontalArrangement = Arrangement.spacedBy(0.dp),
        verticalArrangement = Arrangement.spacedBy(0.dp)
    ) {
        items(100) { index ->
            val x: Int = index / 10
            val y: Int = index % 10
            Box(
                modifier = Modifier
                    .size(25.dp)
                    .border(0.01.dp, color = Color.Gray)
                    .clickable {
                        val selectedCoor: String =
                            "" + (65 + x).toChar() + (48 + y).toChar()
                        placeShipViewModel.selectCoor(selectedCoor)
                    },

                contentAlignment = Alignment.Center
            ) {
                Image(
                    painter = painterResource(id = R.drawable.sea),
                    contentDescription = null,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier
                        .fillMaxSize()

                )
                if (board[x][y].selected) {
                    Image(
                        painter = painterResource(id = getImage(board[x][y].typeShip, board[x][y].index)),
                        contentDescription = null,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier
                            .fillMaxSize()
                            .graphicsLayer(rotationZ = if (board[x][y].direction) 0f else -90f)

                    )
                }

            }
        }
    }
}

fun errorInput(input: String): Boolean {
    if (input != "" && input.length != 2) return true
    if (!(input[0] in 'A'..'J' || input[1] in 'a'..'j')) {
        return true
    }
    if (!(input[1] in '0'..'9')) return true
    return false
}

@Composable
fun PlaceShipScreen(
    context: Context,
    onNextButtonClicked: () -> Unit,
    placeShipViewModel: PlaceShipViewModel,
    gameViewModel: GameViewModel,
    modifier: Modifier = Modifier
) {
    val selectedCoor by placeShipViewModel.selectedCoor.collectAsState()
    (context as MainActivity)?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
    Row(
        modifier = modifier.fillMaxSize(),
    ) {
        Box(modifier = Modifier
            .weight(0.8f)
            .fillMaxSize(),
            contentAlignment = Alignment.CenterEnd)
        {
            Column {

                Row {
                    Text(text = "", modifier = Modifier.size(30.dp, 25.dp))
                    for (i in 0..9) {
                        Text(
                            text = i.toString(),textAlign = TextAlign.Center,
                            fontSize = 13.sp,
                            modifier = Modifier
                                .size(25.dp)
                                .wrapContentSize(Alignment.Center)
                        )
                    }

                }
                Row {
                    Column {
                        for (i in 0..9) {
                            Text(
                                text = ('A' + i).toString(),
                                textAlign = TextAlign.Center,
                                fontSize = 13.sp,
                                modifier = Modifier
                                    .size(30.dp, 25.dp)
                                    .wrapContentSize(Alignment.Center)

                            )
                        }
                    }
                    BoardScreen(placeShipViewModel)
                }
            }


        }

        Column(
            modifier = Modifier
                .weight(1f)
                .fillMaxHeight()
        ) {
            Column(modifier = Modifier
                .fillMaxWidth()
                .fillMaxHeight(),
                verticalArrangement = Arrangement.SpaceEvenly,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                var shipType by remember {
                    mutableStateOf(4)
                }
                var isError by remember {
                    mutableStateOf(false)
                }
//                var input by remember {
//                    mutableStateOf("")
//                }
                var direction by remember {
                    mutableStateOf(false)
                }
                var curCount by remember {
                    mutableStateOf(0)
                }
                val shipName: String = when(shipType) {
                    4 -> "Very big ship"
                    3 -> "Big ship"
                    2 -> "Small ship"
                    1 -> "Very small ship"
                    else -> ""
                }

                if (shipType > 0) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(text = shipName, fontSize = 23.sp, fontWeight = FontWeight.SemiBold)
                        Text(text = " ${curCount}/${5 - shipType} | Len: ${shipType}", fontWeight = FontWeight.Light, fontSize = 14.sp)
                    }
                }
                else {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(text = "Very small ship", fontSize = 22.sp, fontWeight = FontWeight.SemiBold)
                        Text(text = " 4/4 | Len: 1", fontWeight = FontWeight.Light, fontSize = 13.sp)
                    }
                }


                Row {
                    for (index in 1..shipType) {
                        Image(
                            painter = painterResource(id = getImage(typeShip = shipType, index = index)),
                            contentDescription = null,
                            modifier = Modifier
                                .size(35.dp)
                                .graphicsLayer(rotationZ = -90f)
                        )
                    }
                }
                if (shipType == 0) {
                    Image(
                        painter = painterResource(id = getImage(typeShip = 1, index = 1)),
                        contentDescription = null,
                        modifier = Modifier
                            .size(35.dp)
                            .graphicsLayer(rotationZ = -90f)
                    )
                }




                OutlinedTextField(
                    singleLine = true,
                    textStyle = TextStyle(textAlign = TextAlign.Center),
                    value = selectedCoor.selectedCoor,
                    onValueChange = {

                        placeShipViewModel.selectCoor(it)
                                    },
                    placeholder = { Text(text = "Example: C4", color = Color.Gray, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth())},
                    isError =  (selectedCoor.selectedCoor != "" && selectedCoor.selectedCoor.length != 2) || isError,
                    modifier = Modifier.padding(horizontal = 75.dp)
                )
                if (shipType > 0) {
                    Column {
                        var result by remember {
                            mutableStateOf(false)
                        }
                        Button(
                            onClick = {
                                isError = errorInput(selectedCoor.selectedCoor)
                                if (isError == false) {
//                                placeShipViewModel.selectCoor(input)
                                    isError = !placeShipViewModel.selectCoorToPlace(
                                        typeShip = shipType,
                                        direction = direction
                                    )
                                    if (isError == false) {
                                        direction = false
                                        placeShipViewModel.selectCoor("")
                                        curCount += 1
                                        if (curCount >= (5 - shipType)) {
                                            curCount = 0
                                            shipType -= 1
                                        }

                                    }

                                    result = isError

                                }

                            },
                            modifier = Modifier.width(110.dp)
                        ) {
                            Text(text = "PLACE")
                        }
                        OutlinedButton(
                            onClick = { direction = !direction },
                            modifier = Modifier.width(110.dp)
                        ) {
                            Text(text = "ROTATE")
                        }

//                        Text(text = "result: ${selectedCoor.selectedCoor}")
//                        Text(text = if (direction) "doc" else "ngang")
                    }
                }
                else {

                    Button(
                        onClick = onNextButtonClicked
                    ) {
                        Text(text = "START", fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    }
                }


            }

        }

    }
}


@Preview(showBackground = true, device = "spec:width=712dp,height=360dp,orientation=landscape")
@Composable
fun Hah() {

    DemoBattleShipTheme {
//        BoardScreen(board = DataResource().loadBoard())
//        HomeScreen(context = LocalContext.current)
        PlaceShipScreen(
            context = LocalContext.current,
            onNextButtonClicked = {},
            placeShipViewModel = PlaceShipViewModel(),
            gameViewModel = GameViewModel()
        )
    }
}