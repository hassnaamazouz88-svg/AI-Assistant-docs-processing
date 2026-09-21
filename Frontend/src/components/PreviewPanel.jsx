import { useTranslation } from 'react-i18next'
import { urlApercu, urlTelechargement } from '../services/generation'

/**
 * Panneau d'aperçu — ne s'affiche QUE lorsque l'utilisateur clique sur
 * "Aperçu" d'un fichier généré (via `fichier` non nul). Le backend
 * convertit déjà tout (docx/xlsx) en PDF pour la prévisualisation
 * (/preview), donc l'iframe peut afficher n'importe quel format généré
 * directement dans le navigateur, sans téléchargement préalable.
 */
function PreviewPanel({ fichier, onClose }) {
  const { t } = useTranslation()

  if (!fichier) return null

  return (
    <div className="fixed inset-0 z-[60] flex justify-end" role="dialog" aria-modal="true">
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />

      <div className="glass relative flex h-full w-full max-w-xl flex-col border-l border-soft">
        <div className="bar-solid flex items-center justify-between gap-2 border-b border-soft px-4 py-3">
          <div className="min-w-0">
            <p className="truncate text-sm font-medium text-1">
              {fichier.titre || fichier.type_fichier}
            </p>
            <p className="text-[10px] uppercase tracking-wide text-3">{fichier.type_fichier}</p>
          </div>
          <div className="flex shrink-0 items-center gap-2">
            <a
              href={urlTelechargement(fichier.id)}
              className="glass-btn glass-pill px-3 py-1.5 text-xs"
            >
              {t('generated.download')}
            </a>
            <button
              type="button"
              onClick={onClose}
              aria-label={t('common.close')}
              className="glass glass-circle glass-interactive flex h-8 w-8 items-center justify-center text-1"
            >
              <svg viewBox="0 0 24 24" fill="none" strokeWidth="2" stroke="currentColor" className="h-3.5 w-3.5">
                <path strokeLinecap="round" d="M6 6l12 12M18 6L6 18" />
              </svg>
            </button>
          </div>
        </div>

        <div className="flex-1 bg-white">
          <iframe
            src={urlApercu(fichier.id)}
            title={fichier.titre || fichier.type_fichier}
            className="h-full w-full border-0"
          />
        </div>
      </div>
    </div>
  )
}

export default PreviewPanel
