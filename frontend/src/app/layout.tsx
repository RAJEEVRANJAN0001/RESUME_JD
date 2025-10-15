import type { Metadata } from 'next'
import './globals.css'
import { ThemeProvider } from "@/components/theme-provider"
import { Toaster } from "@/components/ui/sonner"
import { AppWrapper } from "@/components/app-wrapper"

export const metadata: Metadata = {
  title: 'Smart Resume Screener',
  description: 'Intelligent resume parsing and screening using AI',
}

const hideTranslatorStyles = `
   /* Hide only specific translator tooltip elements that cause hydration issues */
   [class*="translate-tooltip-mtz"],
   [class*="translator-hidden"],
   .translator-container,
   #google-translate-element {
     display: none !important;
     visibility: hidden !important;
     opacity: 0 !important;
     pointer-events: none !important;
     height: 0 !important;
     width: 0 !important;
     overflow: hidden !important;
     position: absolute !important;
     left: -9999px !important;
     top: -9999px !important;
   }
 `

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning translate="no" className="notranslate">
      <head>
        <meta name="google" content="notranslate" />
        <meta name="googlebot" content="notranslate" />
        <style dangerouslySetInnerHTML={{ __html: hideTranslatorStyles }} />
      </head>
      <body suppressHydrationWarning className="antialiased notranslate">
        <script
          dangerouslySetInnerHTML={{
            __html: `
              // Only remove specific problematic translator elements
              (function() {
                function removeSpecificTranslatorElements() {
                  // Only target the specific problematic elements that cause hydration issues
                  const problematicSelectors = [
                    '[class*="translate-tooltip-mtz"]',
                    '[class*="translator-hidden"]',
                    '.translator-container',
                    '#google-translate-element'
                  ];

                  problematicSelectors.forEach(selector => {
                    const elements = document.querySelectorAll(selector);
                    elements.forEach(el => {
                      // Only remove if it's likely an extension-injected element
                      if (el && !el.closest('[data-reactroot], [data-nextjs-scroll-focus-boundary]')) {
                        el.remove();
                      }
                    });
                  });
                }

                // Run once after a short delay to avoid interfering with legitimate elements
                setTimeout(removeSpecificTranslatorElements, 50);
              })();
            `,
          }}
        />
        <script
          dangerouslySetInnerHTML={{
            __html: `
              // Fix for specific translator tooltip hydration issue only
              document.addEventListener('DOMContentLoaded', function() {
                // Only target the exact problematic div that causes hydration mismatch
                const problematicDiv = document.querySelector('div[class*="translate-tooltip-mtz"][class*="translator-hidden"]');
                if (problematicDiv) {
                  // Normalize the hidden attribute to prevent server/client mismatch
                  problematicDiv.setAttribute('hidden', 'true');
                  problematicDiv.style.display = 'none';
                  // Remove any child elements that might cause issues
                  while (problematicDiv.firstChild) {
                    problematicDiv.firstChild.remove();
                  }
                }
              });
            `,
          }}
        />
        <div suppressHydrationWarning>
          <AppWrapper>
            <ThemeProvider
              attribute="class"
              defaultTheme="system"
              enableSystem
              disableTransitionOnChange
            >
              {children}
              <Toaster />
            </ThemeProvider>
          </AppWrapper>
        </div>
      </body>
    </html>
  )
}
