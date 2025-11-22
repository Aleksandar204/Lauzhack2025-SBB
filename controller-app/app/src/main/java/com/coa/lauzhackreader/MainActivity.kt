package com.coa.lauzhackreader

import android.nfc.NfcAdapter
import android.nfc.Tag
import android.nfc.tech.Ndef
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import com.coa.lauzhackreader.ui.theme.LauzhackReaderTheme

class MainActivity : ComponentActivity() {

    private var nfcAdapter: NfcAdapter? = null

    // Compose-friendly state held in Activity
    private var message by mutableStateOf("Press Start and bring a card close")
    private var isReading by mutableStateOf(false)

    // Reader callback (updates UI on main thread)
    private val readerCallback = NfcAdapter.ReaderCallback { tag: Tag ->
        // This callback is NOT on the main thread, so switch to UI thread to update state
        val id = bytesToHex(tag.id)
//            val techs = tag.techList.joinToString(", ")
        val maybeNdef = Ndef.get(tag)
        runOnUiThread {
            Toast.makeText(this, "Scanned ID: $id", Toast.LENGTH_LONG).show()
            message = "Sending data to server..."
        }
        var resp = sendDataToServer(id)
        runOnUiThread {
            Toast.makeText(this, resp, Toast.LENGTH_LONG).show()
            message = resp
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        nfcAdapter = NfcAdapter.getDefaultAdapter(this)
        enableEdgeToEdge()

        setContent {
            LauzhackReaderTheme {
                MainScreen(
                    lastTagId = message,
                    isReading = isReading,
                    onStart = {
                        if (nfcAdapter == null) {
                            message = "Device has NO NFC hardware"
                            return@MainScreen
                        }
                        if (nfcAdapter?.isEnabled == false) {
                            message = "NFC is turned OFF. Turn on in Settings."
                            return@MainScreen
                        }
                        startReaderMode()
                    },
                    onStop = {
                        stopReaderMode()
                    }
                )
            }
        }
    }

    override fun onPause() {
        super.onPause()
        // If you want reading only while app is visible, stop here:
        stopReaderMode()
    }

    private fun startReaderMode() {
        if (isReading) return
        nfcAdapter?.enableReaderMode(
            this,
            readerCallback,
            // Flags: accept common tech families and skip NDEF check for raw detection
            NfcAdapter.FLAG_READER_NFC_A
                    or NfcAdapter.FLAG_READER_NFC_B
                    or NfcAdapter.FLAG_READER_NFC_F
                    or NfcAdapter.FLAG_READER_NFC_V
                    or NfcAdapter.FLAG_READER_NFC_BARCODE
                    or NfcAdapter.FLAG_READER_SKIP_NDEF_CHECK,
            null
        )
        isReading = true
        message = "Reader mode ON — bring card close"
    }

    private fun stopReaderMode() {
        if (!isReading) return
        nfcAdapter?.disableReaderMode(this)
        isReading = false
        message = "Reader mode OFF"
    }

    private fun bytesToHex(bytes: ByteArray): String {
        return bytes.joinToString("") { "%02X".format(it) }
    }
}

private fun sendDataToServer(id: String) : String {
    return try {
        "Successful auth for ID: $id"
    } catch (e: Exception) {
        "Error: ${e.message}"
    }
}
