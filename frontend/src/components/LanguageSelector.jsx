import { useLanguage } from '../context/LanguageContext'

export default function LanguageSelector() {
  const { language, setLanguage, t } = useLanguage()

  const languages = [
    { code: 'en', label: 'English', flag: '🇬🇧' },
    { code: 'hi', label: 'हिंदी', flag: '🇮🇳' },
    { code: 'hinglish', label: 'Hinglish', flag: '🔤' },
  ]

  return (
    <div className="flex items-center gap-1 bg-neutral-100 p-1 rounded-lg border border-neutral-200 text-xs">
      {languages.map((lang) => {
        const isActive = language === lang.code
        return (
          <button
            key={lang.code}
            type="button"
            onClick={() => setLanguage(lang.code)}
            className={`px-2.5 py-1 rounded-md font-medium transition flex items-center gap-1.5 ${
              isActive
                ? 'bg-white text-orange-600 shadow-xs font-semibold'
                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-200/60'
            }`}
            title={`Switch to ${lang.label}`}
          >
            <span>{lang.flag}</span>
            <span>{lang.label}</span>
          </button>
        )
      })}
    </div>
  )
}
