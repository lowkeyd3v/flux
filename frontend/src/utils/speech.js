/**
 * Browser Speech Recognition (STT) and Speech Synthesis (TTS) Utilities.
 * Optimized for Indian English (en-IN) and Hindi (hi-IN).
 */

export const isSpeechSynthesisSupported = () => {
  return typeof window !== 'undefined' && 'speechSynthesis' in window
}

export const isSpeechRecognitionSupported = () => {
  if (typeof window === 'undefined') return false
  return 'SpeechRecognition' in window || 'webkitSpeechRecognition' in window
}

/**
 * Strips markdown symbols, asterisks, brackets, and URLs to produce natural conversational speech text.
 */
export const cleanTextForSpeech = (rawText) => {
  if (!rawText) return ''
  return rawText
    .replace(/\[Source:[^\]]+\]/g, '')
    .replace(/https?:\/\/[^\s]+/g, '')
    .replace(/[#*`_~]/g, '')
    .replace(/₹/g, ' rupees ')
    .replace(/\s+/g, ' ')
    .trim()
}

/**
 * Text-to-Speech (TTS) readout using browser window.speechSynthesis.
 */
export const speakText = (text, lang = 'en', onEnd = null) => {
  if (!isSpeechSynthesisSupported()) return false

  // Stop any currently ongoing speech
  stopSpeaking()

  const clean = cleanTextForSpeech(text)
  if (!clean) return false

  const utterance = new SpeechSynthesisUtterance(clean)

  // Map app language code to speech synthesis BCP-47 language tag
  const langTag = lang === 'hi' ? 'hi-IN' : 'en-IN'
  utterance.lang = langTag
  utterance.rate = 0.95
  utterance.pitch = 1.0

  // Attempt to select an Indian voice if available
  const voices = window.speechSynthesis.getVoices()
  const preferredVoice = voices.find(
    (v) =>
      v.lang.toLowerCase().startsWith(langTag.toLowerCase().slice(0, 2)) ||
      v.lang.toLowerCase().includes('in') ||
      v.name.toLowerCase().includes('india') ||
      v.name.toLowerCase().includes('hindi')
  )
  if (preferredVoice) {
    utterance.voice = preferredVoice
  }

  if (onEnd) {
    utterance.onend = onEnd
    utterance.onerror = onEnd
  }

  window.speechSynthesis.speak(utterance)
  return true
}

/**
 * Halts active text-to-speech synthesis.
 */
export const stopSpeaking = () => {
  if (isSpeechSynthesisSupported()) {
    window.speechSynthesis.cancel()
  }
}

/**
 * Factory for Web Speech Recognition.
 */
export const createSpeechRecognizer = ({ lang = 'en', onResult, onError, onEnd }) => {
  if (!isSpeechRecognitionSupported()) return null

  const SpeechRecognitionClass =
    window.SpeechRecognition || window.webkitSpeechRecognition
  const recognizer = new SpeechRecognitionClass()

  // Set language for recognition
  recognizer.lang = lang === 'hi' ? 'hi-IN' : lang === 'hinglish' ? 'hi-IN' : 'en-IN'
  recognizer.continuous = false
  recognizer.interimResults = false
  recognizer.maxAlternatives = 1

  recognizer.onresult = (event) => {
    if (event.results && event.results[0] && event.results[0][0]) {
      const transcript = event.results[0][0].transcript
      if (onResult) onResult(transcript)
    }
  }

  recognizer.onerror = (event) => {
    if (onError) onError(event.error)
  }

  recognizer.onend = () => {
    if (onEnd) onEnd()
  }

  return recognizer
}
