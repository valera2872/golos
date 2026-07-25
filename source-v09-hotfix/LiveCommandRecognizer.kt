package com.quietdiary.app

import android.content.Context
import android.os.Build
import android.os.ParcelFileDescriptor
import android.util.Log
import com.google.mlkit.genai.common.FeatureStatus
import com.google.mlkit.genai.common.audio.AudioSource
import com.google.mlkit.genai.speechrecognition.SpeechRecognition
import com.google.mlkit.genai.speechrecognition.SpeechRecognizer
import com.google.mlkit.genai.speechrecognition.SpeechRecognizerOptions
import com.google.mlkit.genai.speechrecognition.SpeechRecognizerResponse
import com.google.mlkit.genai.speechrecognition.speechRecognizerOptions
import com.google.mlkit.genai.speechrecognition.speechRecognizerRequest
import java.io.FileOutputStream
import java.text.Normalizer
import java.util.Locale
import java.util.concurrent.atomic.AtomicBoolean
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

/**
 * Streams the same PCM that is being saved into Google's on-device recognizer.
 * It detects control commands and keeps a live transcript, without opening a second microphone.
 */
class LiveCommandRecognizer private constructor(
    private val listener: Listener,
) {
    enum class Command { SAVE, CANCEL }

    interface Listener {
        fun onCommand(command: Command)
        fun onTranscript(text: String)
        fun onUnavailable(message: String)
    }

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private val stopped = AtomicBoolean(false)
    private var recognizer: SpeechRecognizer? = null
    private var readPipe: ParcelFileDescriptor? = null
    private var writePipe: ParcelFileDescriptor? = null
    private var output: FileOutputStream? = null
    private var recognitionJob: Job? = null
    private var lastCommandAt = 0L
    private var committedText = ""
    private var partialText = ""

    fun start() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.S) {
            listener.onUnavailable("Голосовые команды требуют Android 12+")
            return
        }
        try {
            val pipe = ParcelFileDescriptor.createPipe()
            readPipe = pipe[0]
            writePipe = pipe[1]
            output = FileOutputStream(pipe[1].fileDescriptor)
        } catch (e: Exception) {
            listener.onUnavailable(friendly(e))
            return
        }

        recognitionJob = scope.launch {
            try {
                val active = SpeechRecognition.getClient(
                    speechRecognizerOptions {
                        locale = Locale.forLanguageTag("ru-RU")
                        preferredMode = SpeechRecognizerOptions.Mode.MODE_BASIC
                    }
                )
                recognizer = active
                if (active.checkStatus() != FeatureStatus.AVAILABLE) {
                    throw IllegalStateException("Системная модель Google не подготовлена")
                }
                val request = speechRecognizerRequest {
                    audioSource = AudioSource.fromPfd(readPipe!!)
                }
                active.startRecognition(request).collect { response ->
                    when (response) {
                        is SpeechRecognizerResponse.PartialTextResponse -> handlePartial(response.text)
                        is SpeechRecognizerResponse.FinalTextResponse -> handleFinal(response.text)
                        is SpeechRecognizerResponse.ErrorResponse -> {
                            if (!stopped.get()) listener.onUnavailable(friendly(response.e))
                        }
                        else -> Unit
                    }
                }
            } catch (e: Exception) {
                if (!stopped.get()) listener.onUnavailable(friendly(e))
            }
        }
    }

    @Synchronized
    fun write(samples: ShortArray, count: Int) {
        if (stopped.get() || count <= 0) return
        try {
            val bytes = ByteArray(count * 2)
            var out = 0
            for (i in 0 until count) {
                val value = samples[i].toInt()
                bytes[out++] = (value and 0xff).toByte()
                bytes[out++] = ((value shr 8) and 0xff).toByte()
            }
            output?.write(bytes)
            output?.flush()
        } catch (e: Exception) {
            if (!stopped.get()) listener.onUnavailable(friendly(e))
            stop()
        }
    }

    @Synchronized
    fun snapshot(): String = combinedText()

    fun stop() {
        if (!stopped.compareAndSet(false, true)) return

        var localOutput: FileOutputStream? = null
        var localWritePipe: ParcelFileDescriptor? = null
        var localReadPipe: ParcelFileDescriptor? = null
        var localRecognizer: SpeechRecognizer? = null
        var localJob: Job? = null
        synchronized(this) {
            localOutput = output
            output = null
            localWritePipe = writePipe
            writePipe = null
            localReadPipe = readPipe
            readPipe = null
            localRecognizer = recognizer
            recognizer = null
            localJob = recognitionJob
            recognitionJob = null
        }

        try { localOutput?.close() } catch (_: Exception) {}
        try { localWritePipe?.close() } catch (_: Exception) {}
        try { runBlocking { localRecognizer?.stopRecognition() } } catch (_: Exception) {}
        try { localRecognizer?.close() } catch (_: Exception) {}
        try { localReadPipe?.close() } catch (_: Exception) {}
        localJob?.cancel()
    }

    @Synchronized
    private fun handlePartial(text: String?) {
        partialText = text?.trim().orEmpty()
        val combined = combinedText()
        if (combined.isNotBlank()) listener.onTranscript(combined)
        detect(combined)
    }

    @Synchronized
    private fun handleFinal(text: String?) {
        val clean = text?.trim().orEmpty()
        if (clean.isNotBlank()) {
            committedText = when {
                committedText.isBlank() -> clean
                clean.startsWith(committedText, ignoreCase = true) -> clean
                committedText.endsWith(clean, ignoreCase = true) -> committedText
                else -> "$committedText $clean"
            }.trim()
        }
        partialText = ""
        val combined = combinedText()
        if (combined.isNotBlank()) listener.onTranscript(combined)
        detect(combined)
    }

    private fun combinedText(): String {
        val committed = committedText.trim()
        val partial = partialText.trim()
        return when {
            committed.isBlank() -> partial
            partial.isBlank() -> committed
            partial.startsWith(committed, ignoreCase = true) -> partial
            committed.endsWith(partial, ignoreCase = true) -> committed
            else -> "$committed $partial"
        }.trim()
    }

    private fun detect(text: String?) {
        val normalized = normalize(text ?: return)
        if (normalized.isBlank()) return
        val now = System.currentTimeMillis()
        if (now - lastCommandAt < 1800L) return

        val command = when {
            endsWithAny(normalized, "не сохранять", "отмена", "отменить", "удалить запись") -> Command.CANCEL
            endsWithAny(normalized, "сохранить", "сохрани", "готово сохранить", "запись сохранить") -> Command.SAVE
            else -> null
        }
        if (command != null) {
            lastCommandAt = now
            listener.onCommand(command)
        }
    }

    private fun endsWithAny(value: String, vararg variants: String): Boolean =
        variants.any { value == it || value.endsWith(" $it") }

    private fun normalize(value: String): String =
        Normalizer.normalize(value.lowercase(Locale.ROOT), Normalizer.Form.NFD)
            .replace("\\p{M}+".toRegex(), "")
            .replace('ё', 'е')
            .replace("[^а-яa-z0-9 ]".toRegex(), " ")
            .replace("\\s+".toRegex(), " ")
            .trim()

    private fun friendly(e: Throwable): String {
        val raw = e.message?.trim().orEmpty()
        return if (raw.isNotEmpty()) raw else e.javaClass.simpleName
    }

    companion object {
        private const val TAG = "LiveCommandRecognizer"

        @JvmStatic
        fun create(context: Context, listener: Listener): LiveCommandRecognizer {
            Log.d(TAG, "Creating command recognizer for ${context.packageName}")
            return LiveCommandRecognizer(listener)
        }
    }
}
