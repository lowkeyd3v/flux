import { useState, useEffect, useRef } from 'react'
import {
  isSpeechRecognitionSupported,
  createSpeechRecognizer,
} from '../utils/speech'
import { useLanguage } from '../context/LanguageContext'

export default function VoiceButton({ onTranscript, className = '' }) {
  const { language, t } = useLanguage()
  const [isListening, setIsListening] = useState(false)
  const [isSupported, setIsSupported] = useState(true)
  const recognizerRef = useRef(null)

  useEffect(() => {
    setIsSupported(isSpeechRecognitionSupported())
  }, [])

  const startListening = () => {
    if (!isSupported) {
      alert(t('voiceNotSupported'))
      return
    }

    try {
      const recognizer = createSpeechRecognizer({
        lang: language,
        onResult: (transcript) => {
          setIsListening(false)
          if (onTranscript && transcript) {
            onTranscript(transcript)
          }
        },
        onError: (err) => {
          setIsListening(false)
          console.warn('Speech recognition error:', err)
        },
        onEnd: () => {
          setIsListening(false)
        },
      })

      if (recognizer) {
        recognizerRef.current = recognizer
        setIsListening(true)
        recognizer.start()
      }
    } catch (e) {
      setIsListening(false)
      console.warn('Could not start recognition:', e)
    }
  }

  const stopListening = () => {
    if (recognizerRef.current) {
      try {
        recognizerRef.current.stop()
      } catch (_) {}
    }
    setIsListening(false)
  }

  const toggleListening = () => {
    if (isListening) {
      stopListening()
    } else {
      startListening()
    }
  }

  if (!isSupported) {
    return null
  }

  return (
    <button
      type="button"
      onClick={toggleListening}
      className={`relative inline-flex items-center justify-center p-2.5 rounded-lg border transition ${
        isListening
          ? 'bg-red-500 text-white border-red-600 shadow-md animate-pulse'
          : 'bg-white hover:bg-neutral-50 text-neutral-700 border-neutral-300 shadow-2xs hover:border-orange-400'
      } ${className}`}
      title={isListening ? t('voiceListening') : t('voiceSpeakNow')}
    >
      <span className="text-base">{isListening ? '⏹️' : '🎙️'}</span>
      {isListening && (
        <span className="absolute -top-1 -right-1 flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
        </span>
      )}
    </button>
  )
}
