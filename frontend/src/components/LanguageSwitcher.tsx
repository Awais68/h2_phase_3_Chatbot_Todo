'use client'

import React, { useState, useRef, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { supportedLanguages, type LanguageCode } from '@/lib/i18n-config'
import { Globe, ChevronDown, Check } from 'lucide-react'

/**
 * LanguageSwitcher Component
 *
 * A dropdown component for switching between supported languages.
 * Automatically handles RTL positioning.
 */
export function LanguageSwitcher() {
  const { i18n, t } = useTranslation()
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  const currentLang = (i18n.language || 'en') as LanguageCode
  const currentLanguage = supportedLanguages.find(l => l.code === currentLang) || supportedLanguages[0]

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Handle language change
  const handleLanguageChange = (langCode: LanguageCode) => {
    i18n.changeLanguage(langCode)
    setIsOpen(false)
  }

  // Get current language direction for styling
  const isRTL = currentLanguage.dir === 'rtl'

  return (
    <div
      ref={dropdownRef}
      className="relative language-switcher"
      dir={isRTL ? 'rtl' : 'ltr'}
    >
      {/* Trigger Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 rounded-lg
                   bg-secondary hover:bg-secondary/80
                   text-secondary-foreground
                   transition-colors duration-200
                   focus:outline-none focus:ring-2 focus:ring-ring"
        aria-label={t('language.switch')}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
      >
        <Globe className="w-4 h-4" aria-hidden="true" />
        <span className="text-sm font-medium hidden sm:inline">
          {currentLanguage.nativeName}
        </span>
        <ChevronDown
          className={`w-4 h-4 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
          aria-hidden="true"
        />
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div
          className="absolute top-full mt-2 min-w-[160px] rounded-lg shadow-lg
                     bg-popover border border-border
                     z-50 overflow-hidden
                     animate-in fade-in zoom-in-95 duration-200"
          style={{
            [isRTL ? 'left' : 'right']: 0,
          }}
          role="listbox"
          aria-label={t('language.selectLanguage')}
        >
          <div className="py-1">
            {supportedLanguages.map((language) => (
              <button
                key={language.code}
                onClick={() => handleLanguageChange(language.code)}
                className={`w-full flex items-center justify-between px-4 py-2
                           text-sm transition-colors duration-150
                           hover:bg-accent hover:text-accent-foreground
                           focus:outline-none focus:bg-accent
                           ${language.code === currentLang ? 'bg-accent/50' : ''}`}
                role="option"
                aria-selected={language.code === currentLang}
              >
                <span className="flex items-center gap-3">
                  {/* Language direction indicator */}
                  <span
                    className="text-xs text-muted-foreground w-4 text-center"
                    aria-hidden="true"
                  >
                    {language.code === 'ur' ? 'RTL' : 'LTR'}
                  </span>
                  <span>{language.nativeName}</span>
                </span>
                {language.code === currentLang && (
                  <Check className="w-4 h-4 text-primary" aria-hidden="true" />
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

/**
 * Compact Language Switcher for mobile or space-constrained areas
 */
export function LanguageSwitcherCompact() {
  const { i18n, t } = useTranslation()
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  const currentLang = (i18n.language || 'en') as LanguageCode
  const currentLanguage = supportedLanguages.find(l => l.code === currentLang) || supportedLanguages[0]
  const isRTL = currentLanguage.dir === 'rtl'

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleLanguageChange = (langCode: LanguageCode) => {
    i18n.changeLanguage(langCode)
    setIsOpen(false)
  }

  return (
    <div
      ref={dropdownRef}
      className="relative language-switcher-compact"
      dir={isRTL ? 'rtl' : 'ltr'}
    >
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="p-2 rounded-lg hover:bg-secondary transition-colors"
        aria-label={t('language.switch')}
      >
        <Globe className="w-5 h-5" />
      </button>

      {isOpen && (
        <div
          className="absolute top-full mt-2 min-w-[120px] rounded-lg shadow-lg
                     bg-popover border border-border z-50"
          style={{
            [isRTL ? 'left' : 'right']: 0,
          }}
        >
          <div className="py-1">
            {supportedLanguages.map((language) => (
              <button
                key={language.code}
                onClick={() => handleLanguageChange(language.code)}
                className={`w-full px-3 py-2 text-sm text-left
                           hover:bg-accent transition-colors
                           ${language.code === currentLang ? 'bg-accent/50 font-medium' : ''}`}
              >
                {language.nativeName}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default LanguageSwitcher
