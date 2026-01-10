'use client'

import { useEffect } from 'react'
import { PWAProviders } from "@/components/PWAProviders"
import "@/lib/i18n-config"
import { useLanguage } from '@/hooks/useLanguage'

/**
 * Language-aware layout wrapper
 * Handles RTL direction changes and font loading
 */
function LanguageLayout({ children }: { children: React.ReactNode }) {
    const { isRTL, dir } = useLanguage()

    // Apply RTL direction to document
    useEffect(() => {
        document.documentElement.dir = dir
        document.documentElement.lang = isRTL ? 'ur' : 'en'
    }, [dir, isRTL])

    return (
        <div
            dir={dir}
            lang={isRTL ? 'ur' : 'en'}
        >
            {children}
        </div>
    )
}

/**
 * Client-side layout wrapper
 * Contains all client-side logic and providers
 */
export function ClientLayout({ children }: { children: React.ReactNode }) {
    return (
        <PWAProviders>
            <LanguageLayout>
                <div className="flex flex-col min-h-screen">
                    {children}
                </div>
            </LanguageLayout>
        </PWAProviders>
    )
}
