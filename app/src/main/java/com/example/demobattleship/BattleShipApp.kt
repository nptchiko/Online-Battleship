package com.example.demobattleship

import android.util.Log
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.platform.LocalContext
import androidx.navigation.NavController
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.demobattleship.ui.BattleViewModel
import com.example.demobattleship.ui.GameViewModel
import com.example.demobattleship.ui.PlaceShipViewModel
import com.example.demobattleship.ui.screens.GameScreen
import com.example.demobattleship.ui.screens.HomeScreen
import com.example.demobattleship.ui.screens.PlaceShipScreen

@Composable
fun BattleShipApp(
    placeShipViewModel: PlaceShipViewModel,
    gameViewModel: GameViewModel,
    battleViewModel: BattleViewModel,
    navController: NavHostController = rememberNavController()
) {
    val context = LocalContext.current
    LaunchedEffect(Unit) {
        gameViewModel.socket.on("turn") {
            battleViewModel.updateTurn()
            battleViewModel.listenShootResult(gameViewModel.socket)
        }
    }
    NavHost(
        navController = navController,
        startDestination = "HomeScreen",
    ){
        composable(route = "HomeScreen") {
            HomeScreen(
                context = context,
                onNextButtonClicked = {
                    gameViewModel.readyToStart()
                    navController.navigate("PlaceShip")
                    gameViewModel.socket.off("room_status")
                },
                gameViewModel = gameViewModel
            )
        }
        composable(route = "PlaceShip") {
            PlaceShipScreen(
                context = context,
                onNextButtonClicked = {
                    gameViewModel.sendShipList(placeShipViewModel.shipList)
                    // TODO


                    navController.navigate("GameScreen")
                },
                placeShipViewModel = placeShipViewModel,
                gameViewModel = gameViewModel
            )
        }
        composable(route = "GameScreen") {
            GameScreen(
                context = context,
                gameViewModel = gameViewModel,
                battleViewModel = battleViewModel
            )
        }
    }
}