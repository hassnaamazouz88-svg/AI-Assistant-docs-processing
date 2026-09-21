import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useTheme } from '../context/ThemeContext'

const LANGUAGES = [
  { code: 'fr', label: 'FR' },
  { code: 'en', label: 'EN' },
  { code: 'ar', label: 'AR' },
]

function SunIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" strokeWidth="1.8" stroke="currentColor" {...props}>
      <circle cx="12" cy="12" r="4.5" strokeLinecap="round" />
      <path
        strokeLinecap="round"
        d="M12 2.5v2M12 19.5v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2.5 12h2M19.5 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"
      />
    </svg>
  )
}

function MoonIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" strokeWidth="1.8" stroke="currentColor" {...props}>
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M20.5 14.5A8.5 8.5 0 1 1 9.5 3.5a7 7 0 0 0 11 11Z"
      />
    </svg>
  )
}

function GlobeIcon(props) {
  return (
    <svg viewBox="0 0 24 24" fill="none" strokeWidth="1.8" stroke="currentColor" {...props}>
      <circle cx="12" cy="12" r="9" />
      <path strokeLinecap="round" d="M3 12h18M12 3c2.6 2.6 4 5.7 4 9s-1.4 6.4-4 9c-2.6-2.6-4-5.7-4-9s1.4-6.4 4-9Z" />
    </svg>
  )
}

function LanguageSwitcher() {
  const { i18n, t } = useTranslation()
  const [open, setOpen] = useState(false)
  const ref = useRef(null)

  useEffect(() => {
    function onClickOutside(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false)
    }
    document.addEventListener('mousedown', onClickOutside)
    return () => document.removeEventListener('mousedown', onClickOutside)
  }, [])

  const current = LANGUAGES.find((l) => l.code === i18n.language) ?? LANGUAGES[0]

  useEffect(() => {
    document.documentElement.lang = i18n.language
    document.documentElement.dir = i18n.language === 'ar' ? 'rtl' : 'ltr'
  }, [i18n.language])

  const choose = (code) => {
    i18n.changeLanguage(code)
    setOpen(false)
  }

  return (
    <div className="relative" ref={ref}>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-label={t('common.language')}
        className="glass glass-pill glass-interactive flex items-center gap-1.5 px-3 py-2 text-xs font-semibold"
      >
        <GlobeIcon className="h-4 w-4 opacity-80" />
        {current.label}
      </button>
      {open && (
        <div className="glass glass-rounded absolute right-0 rtl:right-auto rtl:left-0 mt-2 flex flex-col gap-1 p-1.5 shadow-2xl z-50 min-w-[7rem]">
          {LANGUAGES.map((lang) => (
            <button
              key={lang.code}
              type="button"
              onClick={() => choose(lang.code)}
              className={`rounded-xl px-3 py-1.5 text-left text-sm transition-colors ${lang.code === current.code
                ? 'bg-white/15 font-semibold'
                : 'hover:bg-white/10'
                }`}
            >
              {lang.label}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

function Navbar() {
  const { t } = useTranslation()
  const { theme, toggleTheme } = useTheme()

  return (
    <header className="sticky top-0 z-40 px-4 pt-4 sm:px-6">
      <nav className="glass glass-rounded mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 py-3 sm:px-5">
        <Link to="/" className="flex items-center gap-2.5 shrink-0">
          <span className="glass-circle flex h-9 w-9 items-center justify-center bg-gradient-to-br from-[var(--aurora-1)] to-[var(--aurora-2)] shadow-lg">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              className="h-5 w-5 text-white"
            >
              <defs>
                <mask id="moroccan-star-mask">
                  <rect width="24" height="24" fill="white" />

                  {/* Intersections */}
                  <circle cx="10.15" cy="8.05" r="1.05" fill="black" />
                  <circle cx="13.85" cy="8.05" r="1.05" fill="black" />
                  <circle cx="8.65" cy="12.75" r="1.05" fill="black" />
                  <circle cx="15.35" cy="12.75" r="1.05" fill="black" />
                  <circle cx="12" cy="15.15" r="1.05" fill="black" />
                </mask>
              </defs>

              {/* Lignes qui passent en dessous */}
              <g
                mask="url(#moroccan-star-mask)"
                stroke="currentColor"
                strokeWidth="1.35"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M12 2.2 L17.58 19.35" />
                <path d="M17.58 19.35 L2.95 8.75" />
                <path d="M2.95 8.75 L21.05 8.75" />
                <path d="M21.05 8.75 L6.42 19.35" />
                <path d="M6.42 19.35 L12 2.2" />
              </g>

              {/* Portions qui passent au-dessus */}
              <g
                stroke="currentColor"
                strokeWidth="1.35"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M9.55 7.55 L10.75 8.55" />
                <path d="M13.25 8.55 L14.45 7.55" />
                <path d="M8.05 12.25 L9.25 13.25" />
                <path d="M14.75 13.25 L15.95 12.25" />
                <path d="M11.4 14.35 L12.6 15.95" />
              </g>
            </svg>
          </span>
          <span className="leading-tight">
            <span className="block font-display text-sm font-semibold tracking-tight text-1">
              {t('app.title')}
            </span>
            <span className="block text-[11px] text-3">
              {t('app.subtitle')}
            </span>
          </span>
        </Link>

        <div className="flex items-center gap-2">
          <LanguageSwitcher />
          <button
            type="button"
            onClick={toggleTheme}
            aria-label="theme"
            className="glass glass-circle glass-interactive flex h-9 w-9 items-center justify-center text-1"
          >
            {theme === 'dark' ? <SunIcon className="h-4 w-4" /> : <MoonIcon className="h-4 w-4" />}
          </button>
        </div>
      </nav>
    </header>
  )
}

export default Navbar
