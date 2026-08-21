import { useState, useEffect } from 'react'
import { isSpeechSynthesisSupported, speakText, stopSpeaking } from '../utils/speech'
import { useLanguage } from '../context/LanguageContext'

export default function SpeakerButton({ text, className = '', label = null }) {
  const { language, t } = useLanguage()
  const [isPlaying, setIsPlaying] = useState(false)
  const [isSupported, setIsSupported] = useState(true)

  useEffect(() => {
    setIsSupported(isSpeechSynthesisSupported())
    return () => {
      stopSpeaking()
    }
  }, [])

  const handleToggle = (e) => {
    e.stopPropagation()
    if (!text || !isSupported) return

    if (isPlaying) {
      stopSpeaking()
      setIsPlaying(false)
    } else {
      const ok = speakText(text, language, () => {
        setIsPlaying(false)
      })
      if (ok) {
        setIsPlaying(true)
      }
    }
  }

  if (!isSupported || !text) {
    return null
  }

  return (
    <button
      type="button"
      onClick={handleToggle}
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium border transition ${
        isPlaying
          ? 'bg-orange-50 text-orange-700 border-orange-300 shadow-2xs animate-pulse'
          : 'bg-white hover:bg-neutral-50 text-neutral-600 border-neutral-200 shadow-2xs hover:text-orange-600 hover:border-orange-300'
      } ${className}`}
      title={isPlaying ? t('btnStopReading') : t('btnReadAloud')}
    >
      <span>{isPlaying ? '🔊' : '🔈'}</span>
      <span>{label || (isPlaying ? t('btnStopReading') : t('btnReadAloud'))}</span>
    </button>
  )
}
