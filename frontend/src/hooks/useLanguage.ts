'use client'

import { useCallback } from 'react'
import { useTranslation as useReactI18NextTranslation } from 'react-i18next'
import {
  supportedLanguages,
  type LanguageCode,
  getLanguageDirection,
  getLanguageFont,
  applyDirection,
  formatDate,
  formatRelativeTime,
  getStoredLanguage,
} from '@/lib/i18n-config'

/**
 * Extended useTranslation hook with additional language utilities
 *
 * Provides all standard i18n functionality plus:
 * - Language direction (RTL/LTR) helpers
 * - Language font helpers
 * - Date formatting
 * - Direct language change with direction application
 */
export function useLanguage() {
  const {
    i18n,
    t,
    ready,
  } = useReactI18NextTranslation()

  const currentLang = (i18n.language || 'en') as LanguageCode

  /**
   * Change the current language and apply direction
   */
  const changeLanguage = useCallback((langCode: LanguageCode) => {
    // Validate language code
    if (!supportedLanguages.some(l => l.code === langCode)) {
      console.warn(`[useLanguage] Unknown language code: ${langCode}`)
      return
    }

    // Change language
    i18n.changeLanguage(langCode)

    // Apply direction to document
    applyDirection(langCode)
  }, [i18n])

  /**
   * Get direction for any language
   */
  const getDirection = useCallback((lang: LanguageCode) => {
    return getLanguageDirection(lang)
  }, [])

  /**
   * Get font for any language
   */
  const getFont = useCallback((lang: LanguageCode) => {
    return getLanguageFont(lang)
  }, [])

  /**
   * Get current language info
   */
  const currentLanguage = supportedLanguages.find(l => l.code === currentLang) || supportedLanguages[0]

  /**
   * Check if current language is RTL
   */
  const isRTL = currentLanguage.dir === 'rtl'

  /**
   * Get stored language preference
   */
  const getStoredLang = useCallback(() => {
    return getStoredLanguage()
  }, [])

  /**
   * Format date according to current language
   */
  const formatDateCurrent = useCallback((date: Date | string) => {
    return formatDate(date, currentLang)
  }, [currentLang])

  /**
   * Format relative time according to current language
   */
  const formatRelativeTimeCurrent = useCallback((
    value: number,
    unit: 'day' | 'hour' | 'minute'
  ) => {
    return formatRelativeTime(value, unit, currentLang)
  }, [currentLang])

  /**
   * Get all supported languages
   */
  const languages = supportedLanguages

  return {
    // Standard i18n properties
    i18n,
    t,
    ready,
    language: currentLang,

    // Extended language utilities
    changeLanguage,
    getDirection,
    getFont,
    currentLanguage,
    isRTL,
    getStoredLang,
    formatDate: formatDateCurrent,
    formatRelativeTime: formatRelativeTimeCurrent,
    languages,

    // Shorthand for direction-aware class names
    dir: currentLanguage.dir,
  }
}

/**
 * Hook for getting language direction state
 */
export function useLanguageDirection() {
  const { i18n } = useReactI18NextTranslation()
  const currentLang = (i18n.language || 'en') as LanguageCode
  return getLanguageDirection(currentLang)
}

/**
 * Hook for getting language font
 */
export function useLanguageFont() {
  const { i18n } = useReactI18NextTranslation()
  const currentLang = (i18n.language || 'en') as LanguageCode
  return getLanguageFont(currentLang)
}

export default useLanguage
