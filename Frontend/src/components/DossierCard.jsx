import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { lancerIngestion } from '../services/dossiers'

const STATUT_STYLES = {
  en_attente: 'bg-white/10 text-2 border-soft',
  en_cours: 'bg-sky-400/10 text-sky-300 border-sky-400/25',
  pret: 'bg-emerald-400/10 text-emerald-300 border-emerald-400/25',
  echec: 'bg-rose-400/10 text-rose-300 border-rose-400/25',
}

const STATUT_DOT = {
  en_attente: 'bg-gray-400/70',
  en_cours: 'bg-sky-400 animate-pulse',
  pret: 'bg-emerald-400',
  echec: 'bg-rose-400',
}

function DossierCard({ dossier, onRefresh }) {
  const { t } = useTranslation()
  const [relance, setRelance] = useState(false)

  const handleRelancer = async (e) => {
    e.preventDefault() // empêche le clic de déclencher le Link
    e.stopPropagation()
    if (relance) return
    setRelance(true)
    try {
      await lancerIngestion(dossier.id)
      onRefresh() // recharge la liste pour voir le nouveau statut
    } catch (err) {
      alert(t('dossiers.relaunchError', { message: err.message }))
    } finally {
      setRelance(false)
    }
  }

  const estEnEchec = dossier.statut === 'echec'
  const peutRelancer = dossier.statut === 'en_attente' || estEnEchec
  const docCount = dossier.documents?.length ?? 0

  return (
    <Link
      to={`/dossiers/${dossier.id}/chat`}
      className="glass glass-rounded glass-interactive group flex items-center justify-between gap-4 px-5 py-4"
    >
      <div className="flex min-w-0 items-center gap-4">
        <div className="glass-circle flex h-11 w-11 shrink-0 items-center justify-center bg-white/5">
          <svg viewBox="0 0 24 24" fill="none" strokeWidth="1.6" stroke="currentColor" className="h-5 w-5 opacity-75">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M7 3.5h6.5L18 8v11.5a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-15a1 1 0 0 1 1-1Z"
            />
            <path strokeLinecap="round" strokeLinejoin="round" d="M13 3.5V8h5" />
          </svg>
        </div>
        <div className="min-w-0">
          <h3 className="truncate font-display text-base font-semibold text-1">{dossier.nom}</h3>
          <p className="text-xs text-3">
            {t('dossiers.documentsCount', { count: docCount })}
          </p>
        </div>
      </div>

      <div className="flex shrink-0 items-center gap-2">
        <span
          className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium ${STATUT_STYLES[dossier.statut] ?? STATUT_STYLES.en_attente}`}
        >
          <span className={`h-1.5 w-1.5 rounded-full ${STATUT_DOT[dossier.statut] ?? STATUT_DOT.en_attente}`} />
          {t(`dossiers.statuses.${dossier.statut}`, dossier.statut)}
        </span>
        {peutRelancer && (
          <button
            onClick={handleRelancer}
            type="button"
            disabled={relance}
            title={estEnEchec ? t('dossiers.relaunchHint') : undefined}
            className={`glass glass-pill glass-interactive flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium disabled:opacity-50 ${
              estEnEchec ? 'border-rose-400/30' : ''
            }`}
          >
            {estEnEchec && (
              <svg viewBox="0 0 24 24" fill="none" strokeWidth="2" stroke="currentColor" className="h-3 w-3 text-rose-300">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v4m0 3.5h.01M10.3 3.9 2.6 17.3a1.5 1.5 0 0 0 1.3 2.2h16.2a1.5 1.5 0 0 0 1.3-2.2L13.7 3.9a1.5 1.5 0 0 0-2.6 0Z" />
              </svg>
            )}
            {relance ? t('dossiers.relaunching') : t('dossiers.relaunch')}
          </button>
        )}
        <svg
          viewBox="0 0 24 24"
          fill="none"
          strokeWidth="1.8"
          stroke="currentColor"
          className="h-4 w-4 shrink-0 opacity-40 transition-transform group-hover:translate-x-0.5 group-hover:opacity-80"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
        </svg>
      </div>
    </Link>
  )
}

export default DossierCard
