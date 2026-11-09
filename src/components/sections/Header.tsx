import { useEffect, useRef, useState } from 'react'
import { BRAND } from '../../config/brand'
import { LANGUAGES, NAV } from '../../content/site'
import { Container } from '../ui/Container'
import { ChevronDown, Globe } from '../ui/Icons'
import { Logo } from '../ui/Logo'

export function Header() {
  const [menuOpen, setMenuOpen] = useState(false)
  const [langOpen, setLangOpen] = useState(false)
  const [lang, setLang] = useState('EN')
  const langRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const close = (e: MouseEvent) => {
      if (langRef.current && !langRef.current.contains(e.target as Node)) setLangOpen(false)
    }
    document.addEventListener('mousedown', close)
    return () => document.removeEventListener('mousedown', close)
  }, [])

  useEffect(() => {
    document.body.style.overflow = menuOpen ? 'hidden' : ''
  }, [menuOpen])

  return (
    <header className="sticky top-0 z-30 border-b border-line bg-paper/90 backdrop-blur">
      <Container className="grid h-[60px] grid-cols-[1fr_auto] items-center gap-4 sm:h-[68px] xl:grid-cols-[auto_1fr_auto]">
        <a href="#top" className="flex items-center text-coal" aria-label={`${BRAND.name} home`}>
          <Logo />
        </a>

        <nav className="hidden xl:col-start-2 xl:ms-14 xl:block" aria-label="Main">
          <ul className="flex items-center gap-8">
            {NAV.map((item) => (
              <li key={item.label}>
                <a href={item.href} className="text-body-s whitespace-nowrap text-quiet transition-colors hover:text-graphite">
                  {item.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        <div className="flex items-center justify-end gap-1 sm:gap-2 xl:col-start-3">
          <div className="relative hidden xl:block" ref={langRef}>
            <button
              type="button"
              onClick={() => setLangOpen((v) => !v)}
              aria-expanded={langOpen}
              className="text-body-s flex h-10 items-center gap-1.5 rounded-button px-2.5 font-semibold text-quiet transition-colors hover:bg-bone hover:text-graphite"
            >
              <Globe className="h-4 w-4" />
              <span className="uppercase tracking-[0.03em]">{lang}</span>
              <ChevronDown className={`h-3.5 w-3.5 transition-transform ${langOpen ? 'rotate-180' : ''}`} />
            </button>
            {langOpen && (
              <ul className="absolute end-0 top-12 grid w-40 grid-cols-2 gap-1 rounded-panel bg-paper p-1.5 shadow-[var(--shadow-lift)]">
                {LANGUAGES.map((l) => (
                  <li key={l}>
                    <button
                      type="button"
                      onClick={() => {
                        setLang(l)
                        setLangOpen(false)
                      }}
                      className={`text-body-s w-full rounded-md px-2.5 py-1.5 text-start font-medium transition-colors hover:bg-bone ${l === lang ? 'text-forest' : 'text-graphite'}`}
                    >
                      {l}
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <a
            href={BRAND.signInUrl}
            className="text-body-s hidden h-10 items-center whitespace-nowrap rounded-button px-4 font-semibold text-quiet ring-1 ring-inset ring-line transition-colors hover:text-graphite sm:inline-flex"
          >
            Sign in
          </a>
          <a
            href={BRAND.getStartedUrl}
            className="text-body-s inline-flex h-9 items-center whitespace-nowrap rounded-button bg-forest px-4 font-semibold text-paper transition-colors hover:bg-forest-deep sm:h-10"
          >
            Get Started
          </a>
          <button
            type="button"
            onClick={() => setMenuOpen((v) => !v)}
            aria-label="Menu"
            aria-expanded={menuOpen}
            className="grid h-9 w-9 place-items-center rounded-button text-coal transition-colors hover:bg-bone xl:hidden"
          >
            <span className="relative block h-3 w-[18px]">
              <span className={`absolute left-0 h-[2px] w-full rounded-full bg-current transition-all ${menuOpen ? 'top-[5px] rotate-45' : 'top-0'}`} />
              <span className={`absolute left-0 h-[2px] w-full rounded-full bg-current transition-all ${menuOpen ? 'top-[5px] -rotate-45' : 'top-[10px]'}`} />
            </span>
          </button>
        </div>
      </Container>

      {menuOpen && (
        <div className="fixed inset-x-0 bottom-0 top-[60px] z-30 overflow-y-auto bg-paper sm:top-[68px] xl:hidden">
          <Container className="py-6">
            <ul className="divide-y divide-line border-y border-line">
              {NAV.map((item) => (
                <li key={item.label}>
                  <a href={item.href} onClick={() => setMenuOpen(false)} className="text-body-l block py-4 font-medium text-coal">
                    {item.label}
                  </a>
                </li>
              ))}
            </ul>
            <div className="mt-6 flex flex-wrap gap-2">
              {LANGUAGES.map((l) => (
                <button
                  key={l}
                  type="button"
                  onClick={() => setLang(l)}
                  className={`text-body-s rounded-button px-3 py-1.5 font-semibold ${l === lang ? 'bg-forest text-paper' : 'bg-bone text-graphite'}`}
                >
                  {l}
                </button>
              ))}
            </div>
            <a
              href={BRAND.signInUrl}
              className="text-body-m mt-6 flex h-12 items-center justify-center rounded-button font-semibold text-graphite ring-1 ring-inset ring-line"
            >
              Sign in
            </a>
          </Container>
        </div>
      )}
    </header>
  )
}
