import { createContext, useContext, useState, useEffect } from 'react'
import en from '../translations/en'
import hi from '../translations/hi'
import hinglish from '../translations/hinglish'

const dictionaries = {
  en,
  hi,
  hinglish,
}

const LanguageContext = createContext({
  language: 'en',
  setLanguage: () => {},
  t: (key) => key,
})

const STORAGE_KEY = 'flux_language_preference'

export function LanguageProvider({ children }) {
  const [language, setLanguageState] = useState(() => {
    return localStorage.getItem(STORAGE_KEY) || 'en'
  })

  const setLanguage = (newLang) => {
    if (dictionaries[newLang]) {
      setLanguageState(newLang)
      localStorage.setItem(STORAGE_KEY, newLang)
    }
  }

  const t = (key, params = {}) => {
    const dict = dictionaries[language] || dictionaries.en
    let translation = dict[key] || dictionaries.en[key] || key

    if (typeof translation === 'string') {
      Object.keys(params).forEach((paramKey) => {
        translation = translation.replace(new RegExp(`\\{${paramKey}\\}`, 'g'), params[paramKey])
      })
    }

    return translation
  }

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  return useContext(LanguageContext)
}
