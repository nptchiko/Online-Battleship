package com.example.demobattleship.ui

data class GameUiState(
    val room: String = "",
    val name: String = "raigeki",
    val playWithBot: Boolean = false,
    val oppName: String = "opp",
)
