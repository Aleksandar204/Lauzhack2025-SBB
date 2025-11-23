package com.coa.lauzhackreader.simulatedcards

data class CardResponse(
    val uid: String,
    val counter: Int,
    val mac: String,
    val challenge: String
)