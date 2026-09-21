import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { getDossiers } from '../services/dossiers'
import DossierCard from '../components/DossierCard'

function EmptyState() {
  const { t } = useTranslation()
  return (
    <div className="glass glass-rounded animate-fade-in-up flex flex-col items-center gap-3 px-6 py-16 text-center">
      <div className="glass-circle flex h-16 w-16 items-center justify-center bg-white/5">
        <svg viewBox="0 0 24 24" fill="none" strokeWidth="1.5" stroke="currentColor" className="h-7 w-7 opacity-70">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M4 7.5A2.5 2.5 0 0 1 6.5 5h4l2 2.5h7A2.5 2.5 0 0 1 22 10v7a2.5 2.5 0 0 1-2.5 2.5h-13A2.5 2.5 0 0 1 4 17V7.5Z"
          />
        </svg>
      </div>
      <h2 className="font-display text-lg font-semibold text-1">{t('dossiers.empty')}</h2>
      <p className="max-w-sm text-sm text-2">{t('dossiers.emptyHint')}</p>
      <Link to="/upload" className="glass-btn glass-pill mt-2 px-5 py-2.5 text-sm">
        + {t('nav.newDossier')}
      </Link>
    </div>
  )
}

function SkeletonCard() {
  return <div className="skeleton glass-rounded h-24 w-full border border-soft" />
}

function DossiersListPage() {
  const { t } = useTranslation()
  const [dossiers, setDossiers] = useState([])
  const [chargement, setChargement] = useState(true)

  const refresh = () => getDossiers().then(setDossiers).catch(console.error)

  useEffect(() => {
    getDossiers()
      .then(setDossiers)
      .catch(console.error)
      .finally(() => setChargement(false))
  }, [])

  return (
    <div className="mx-auto w-full max-w-6xl flex-1 px-4 py-8 sm:px-6">
      <div className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <h1 className="font-display text-2xl font-bold tracking-tight text-1 sm:text-3xl">
            {t('dossiers.list')}
          </h1>
          <p className="mt-1 text-sm text-2">{t('dossiers.listSubtitle')}</p>
        </div>
        <Link
          to="/upload"
          className="glass-btn glass-pill inline-flex shrink-0 items-center px-4 py-2.5 text-sm sm:hidden"
        >
          + {t('nav.newDossier')}
        </Link>
      </div>

      {chargement ? (
        <div className="grid gap-4">
          <SkeletonCard />
          <SkeletonCard />
          <SkeletonCard />
        </div>
      ) : dossiers.length === 0 ? (
        <EmptyState />
      ) : (
        <div className="grid gap-4">
          {dossiers.map((dossier, i) => (
            <div
              key={dossier.id}
              className="animate-fade-in-up"
              style={{ animationDelay: `${i * 60}ms` }}
            >
              <DossierCard dossier={dossier} onRefresh={refresh} />
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default DossiersListPage
