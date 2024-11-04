package com.example.demobattleship

import TestScreen
import android.os.Bundle
import android.text.BoringLayout
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.demobattleship.data.DataResource
import com.example.demobattleship.data.model.Coordinate
import com.example.demobattleship.ui.BattleViewModel
import com.example.demobattleship.ui.GameViewModel
import com.example.demobattleship.ui.PlaceShipViewModel
import com.example.demobattleship.ui.screens.GameScreen
import com.example.demobattleship.ui.screens.HomeScreen
import com.example.demobattleship.ui.screens.PlaceShipScreen
import com.example.demobattleship.ui.theme.DemoBattleShipTheme
import io.socket.emitter.Emitter

class MainActivity : ComponentActivity() {
    private val gameViewModel: GameViewModel by viewModels()
    private val placeShipViewModel: PlaceShipViewModel by viewModels()
    private val battleViewModel: BattleViewModel by viewModels()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        gameViewModel.socket.connect()
        gameViewModel.connectSocket()
        setContent {
            DemoBattleShipTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
//                    BoardScreen(board = DataResource().loadBoard())
//                    HomeScreen(context = LocalContext.current, gameViewModel)
//                    PlaceShipScreen(
//                        context = LocalContext.current,
//                        gameViewModel = gameViewModel,
//                        placeShipViewModel = PlaceShipViewModel()
//                    )
//                    GameScreen(
//                        context = LocalContext.current,
//                        gameViewModel = gameViewModel
//                    )
                    BattleShipApp(
                        placeShipViewModel = placeShipViewModel,
                        gameViewModel = gameViewModel,
                        battleViewModel = battleViewModel
                    )
                }
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        gameViewModel.disconnectSocket()
    }
}


@Composable
fun LeftPlayer(
    avt: Int,
    name: String,
    time: String,
    score: Int,
    playerTurn: Boolean,
    modifier: Modifier = Modifier.size(70.dp)
) {
    Row(
        modifier = modifier.fillMaxSize(),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceAround
    ) {
        Column(horizontalAlignment = Alignment.End, verticalArrangement = Arrangement.SpaceAround) {
            Text(text = name, fontSize = 16.sp)
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier.background(color = Color.Green, shape = RectangleShape)
            ) {
                Text(text = time)
            }
        }
        Image(
            painter = painterResource(id = avt),
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .size(40.dp)
                .background(shape = CircleShape, color = Color.Unspecified)
        )
        Text(text = score.toString(), fontSize = 22.sp, fontWeight = FontWeight.Bold)
    }
}


@Composable
fun CoordinateCard(isShip: Boolean, isSelected: Boolean, onClick:() -> Unit) {

    Box(
        modifier = Modifier
            .size(25.dp)
    ) {
        Button(
            onClick = onClick,
            enabled = !isSelected,
            colors = ButtonDefaults.buttonColors(
                containerColor = Color.Blue,
                disabledContainerColor = if (isShip) Color.Green else Color.LightGray
            ),
            border = BorderStroke(0.2.dp, Color.Black),
            shape = RoundedCornerShape(0.dp),
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(0.dp)
        ) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Image(
                    painter = painterResource(id = R.drawable.sea),
                    contentDescription = null,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
                Image(
                    painter = painterResource(id = if (isSelected)
                        (if (isShip) R.drawable.ship else R.drawable.miss_shot)
                    else R.drawable.sea),
                    contentDescription = null,
                    contentScale = if (isShip) ContentScale.FillBounds else ContentScale.Inside,
                    modifier = Modifier.size(20.dp)
                )
            }

        }
    }
}


@Composable
fun BoardScreen(board: List<Coordinate>) {
    var x by remember {
        mutableIntStateOf(0)
    }
    var y by remember {
        mutableIntStateOf(0)
    }
    LazyVerticalGrid(
        columns = GridCells.Fixed(10) ,
        modifier = Modifier
            .height(252.dp)
            .width(252.dp),
        horizontalArrangement = Arrangement.spacedBy(0.dp),
        verticalArrangement = Arrangement.spacedBy(0.dp)
    ) {
        items(board) {coordinate ->
            CoordinateCard(
                isShip = coordinate.isShip,
                isSelected = coordinate.selected.value,
                onClick = {
                    coordinate.select()
                    x = coordinate.x
                    y = coordinate.y
                }
            )
        }
    }
}


@Preview(showBackground = true, device = "spec:width=712dp,height=360dp,orientation=landscape")@Composable
fun GreetingPreview() {
    DemoBattleShipTheme {
//        BoardScreen(board = DataResource().loadBoard())
//        HomeScreen(context = LocalContext.current)
//        PlaceShipScreen(context = LocalContext.current)
    }
}