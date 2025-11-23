package com.example.controllerdemo

import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.coa.lauzhackreader.simulatedcards.CardResponse
import com.coa.lauzhackreader.simulatedcards.CardSimulator
import com.coa.lauzhackreader.simulatedcards.SimCard
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import okhttp3.RequestBody.Companion.toRequestBody

@Composable
fun SimulatedCardScreen() {

    val simulator = remember { CardSimulator() }
    var selectedCard by remember { mutableStateOf<SimCard?>(null) }
    var lastResponse by remember { mutableStateOf<CardResponse?>(null) }
    var challenge by remember { mutableStateOf("123456") }
    var lastreturndata by remember { mutableStateOf("test123")}
    var scope = rememberCoroutineScope()

    var ctx = LocalContext.current

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(80.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {

        Text("Simulated Cards", style = MaterialTheme.typography.titleLarge)

        LazyColumn(
            modifier = Modifier.weight(1f)
        ) {
            items(simulator.cards.size) { i ->
                val card = simulator.cards[i]
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 4.dp),
                    onClick = { selectedCard = card }
                ) {
                    Column(Modifier.padding(16.dp)) {
                        Text("UID: ${card.uid}")
                        Text("Counter: ${card.stateCounter}")
                        if (selectedCard?.uid == card.uid) {
                            Text("(Selected)", color = MaterialTheme.colorScheme.primary)
                        }
                    }
                }
            }
        }

        OutlinedTextField(
            value = challenge,
            onValueChange = { challenge = it },
            label = { Text("Challenge") },
            modifier = Modifier.fillMaxWidth()
        )

        Row(
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Button(
                onClick = {
                    selectedCard?.let { card ->
                        scope.launch(Dispatchers.IO) {
                            val response = simulator.generateResponse(card.uid, challenge)

                            val serverResult = sendSecureDataToServer(response)

                            // Update Compose states on MAIN thread
                            withContext(Dispatchers.Main) {
                                lastResponse = response
                                lastreturndata = serverResult
                            }
                        }
                    }
                },
                enabled = selectedCard != null
            ) {
                Text("Scan Card")
            }
        }

        lastResponse?.let { resp ->
            Card(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(16.dp)) {
                    Text("Last Response", style = MaterialTheme.typography.titleMedium)
                    Text("UID: ${resp.uid}")
                    Text("Counter: ${resp.counter}")
                    Text("MAC: ${resp.mac.take(36)}...")
                    Text("Debuginfo: $lastreturndata")
                }
            }
        }
    }
}

private fun sendSecureDataToServer(reqData: CardResponse): String {
    return try {
        val client = OkHttpClient()

        val json = """
        {
          "uid": "${reqData.uid}",
          "counter": ${reqData.counter},
          "mac": "${reqData.mac}",
          "challenge": "${reqData.challenge}",
          "timestamp": ${System.currentTimeMillis()},
        }
        """.trimIndent()

        val body = json.toRequestBody("application/json; charset=utf-8".toMediaType())

        val request = Request.Builder()
            .url("https://opulent-fishstick-6q7q69xqgpjhwwj-8000.app.github.dev/check?trip_id=abc&controllor_id=controllerId")
            .post(body)
            .build()

        client.newCall(request).execute().use { resp ->
            val respBody = resp.body?.string()
            if (!resp.isSuccessful) {
                return "HTTP ${resp.code}: ${resp.message} — body=${respBody ?: "empty"}"
            }
            return respBody ?: "Empty response"
        }
    } catch (e: Exception) {
        return "Error: ${e::class.java.name}: ${e.message ?: "<no message>"}\n${e.stackTraceToString()}"
    }
}