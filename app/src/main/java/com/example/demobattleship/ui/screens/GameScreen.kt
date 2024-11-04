package com.example.demobattleship.ui.screens

import android.annotation.SuppressLint
import android.content.Context
import android.content.pm.ActivityInfo
import android.util.Log
import androidx.compose.foundation.Image
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.demobattleship.MainActivity
import com.example.demobattleship.ui.GameViewModel
import com.example.demobattleship.ui.theme.DemoBattleShipTheme
import com.example.demobattleship.R
import com.example.demobattleship.ui.BattleViewModel


@SuppressLint("StateFlowValueCalledInComposition")
@Composable
fun GameScreen(
    context: Context,
    gameViewModel: GameViewModel,
    battleViewModel: BattleViewModel
) {
    (context as MainActivity)?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
//    val gameUiState by gameViewModel.uiState.collectAsState()


    val oppBoard by battleViewModel.oppBoard.collectAsState()
    val yourBoard by battleViewModel.yourBoard.collectAsState()

    val turnState by battleViewModel.turnState.collectAsState()

//    battleViewModel.listenShootResult(gameViewModel.socket)
    Log.d("turn: ", if (turnState.yourTurn) "player" else "bot")
    Column(modifier = Modifier.fillMaxSize()) {
        Row(
            modifier = Modifier.weight(1.2f),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.Bottom
        ) {
            Text(text = gameViewModel.uiState.value.name, modifier = Modifier.weight(8f))
            Box(modifier = Modifier.weight(1.6f))
            Text(text = gameViewModel.uiState.value.oppName, modifier = Modifier.weight(8f))
        }
        Row(
            modifier = Modifier.weight(9f),
            horizontalArrangement = Arrangement.SpaceAround,
            verticalAlignment = Alignment.CenterVertically
        ) {


            Box(
                modifier = Modifier.weight(8f),
                contentAlignment = Alignment.Center
            ) {
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
                                .clickable (enabled = !turnState.yourTurn) {
//                                    val selectedCoor: String =
//                                        "" + (65 + x).toChar() + (48 + y).toChar()
//                                    battleViewModel.shootBot(x, y, gameViewModel.socket)
//                                placeShipViewModel.selectCoor(selectedCoor)
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
                            if (yourBoard[x][y].shipType != 0) {
                                Image(
                                    painter = painterResource(id = if (yourBoard[x][y].shipType == 1) R.drawable.space_in_sea else R.drawable.miss_shot),
                                    contentDescription = null,
                                    contentScale = ContentScale.Crop,
                                    modifier = Modifier
                                        .fillMaxSize()
                                    //                                    .graphicsLayer(rotationZ = if (board[x][y].direction) 0f else -90f)

                                )
                            }

                        }
                    }
                }
            }



            Image(
                painter = painterResource(
                    id = if (turnState.yourTurn) R.drawable.your_turn else R.drawable.opp_turn
                ),
                contentDescription = null,
                modifier = Modifier
                    .size(100.dp, 200.dp)
                    .weight(1.7f)
            )



            Box(
                modifier = Modifier.weight(8f),
                contentAlignment = Alignment.Center
            ) {
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
                                .clickable(enabled = turnState.yourTurn) {
                                    val selectedCoor: String =
                                        "" + (65 + x).toChar() + (48 + y).toChar()
                                    battleViewModel.shootBot(x, y, gameViewModel.socket)
//                                placeShipViewModel.selectCoor(selectedCoor)
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
                            if (oppBoard[x][y].shipType != 0) {
                                Image(
                                    painter = painterResource(id = if (oppBoard[x][y].shipType == 1) R.drawable.space_in_sea else R.drawable.miss_shot),
                                    contentDescription = null,
                                    contentScale = ContentScale.Crop,
                                    modifier = Modifier
                                        .fillMaxSize()
    //                                    .graphicsLayer(rotationZ = if (board[x][y].direction) 0f else -90f)

                                )
                            }
                        }
                    }
                }
            }


        }
    }


}



@Preview(showBackground = true, device = "spec:width=712dp,height=360dp,orientation=landscape")
@Composable
fun GameScreenTest() {

    DemoBattleShipTheme {
//        BoardScreen(board = DataResource().loadBoard())
//        HomeScreen(context = LocalContext.current)
        GameScreen(
            context = LocalContext.current,
            gameViewModel = GameViewModel(),
            battleViewModel = BattleViewModel()
        )
    }
}