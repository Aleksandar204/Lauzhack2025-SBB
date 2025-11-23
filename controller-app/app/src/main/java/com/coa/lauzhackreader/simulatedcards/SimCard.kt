package com.coa.lauzhackreader.simulatedcards

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue

data class SimCard(
    val uid: String,
    val secret: String,
    var counter: Int
) {
    var stateCounter by mutableStateOf(counter)
}