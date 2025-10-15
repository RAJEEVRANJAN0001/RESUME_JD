import { useEffect } from 'react'

export function useHydrationFix() {
  useEffect(() => {
    // Remove any translator-injected elements on mount
    const cleanTranslatorElements = () => {
      const translatorElements = document.querySelectorAll(
        '[class*="translator"], [class*="translate-tooltip"], [class*="mtz"]'
      )
      translatorElements.forEach(el => {
        if (el.parentNode) {
          el.parentNode.removeChild(el)
        }
      })
    }

    // Run immediately
    cleanTranslatorElements()

    // Run again after a short delay to catch late injections
    const timer = setTimeout(cleanTranslatorElements, 100)

    return () => clearTimeout(timer)
  }, [])
}
