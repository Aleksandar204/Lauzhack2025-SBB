package com.coa.lauzhackreader.simulatedcards

import android.util.Base64
import androidx.compose.runtime.mutableStateListOf
import javax.crypto.Mac
import javax.crypto.spec.SecretKeySpec

class CardSimulator {
    val cards = mutableStateListOf<SimCard>()

    init {
        // Create a few demo cards
        cards.add(SimCard(uid = "SUS", secret = "AMOGUS", counter = 1))
        cards.add(SimCard(uid = "AAA", secret = "BBBBBB", counter = 1))
    }

    fun generateResponse(uid: String, challenge: String): CardResponse { // Makes the requested card respond to a challenge given by the controller
        val card = cards.find { it.uid == uid }
            ?: error("Card not found")

        val combined = card.uid + challenge + card.stateCounter
        val mac = computeHmac(card.secret, combined)

        val response = CardResponse(
            uid = card.uid,
            counter = card.stateCounter,
            mac = mac,
            challenge = challenge
        )

        card.stateCounter += 1
        return response
    }

    private fun computeHmac(secret: String, data: String): String {
        val mac = Mac.getInstance("HmacSHA256") // MESSAGE AUTH CODE NEMA VEZE SA MAC ADDRESS
        val keySpec = SecretKeySpec(secret.toByteArray(), "HmacSHA256")
        mac.init(keySpec)
        val result = mac.doFinal(data.toByteArray())
        return Base64.encodeToString(result, Base64.NO_WRAP)
    }

    fun resetCard(uid: String) {
        val card = cards.find { it.uid == uid } ?: return
        card.stateCounter = 1
    }

    fun cloneCard(uid: String) {
        val original = cards.find { it.uid == uid } ?: return
        cards.add(
            SimCard(
                uid = original.uid,
                secret = original.secret,
                counter = original.stateCounter
            )
        )
    }
}