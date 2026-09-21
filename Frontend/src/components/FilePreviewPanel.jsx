import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { urlTelechargement, urlApercu } from '../services/generation'

// Ce panneau ne s'affiche jamais par défaut : il n'apparaît que lorsque
// l'utilisateur clique sur "Aperçu" pour un fichier généré. Le backend
// convertit le document (docx/xlsx) en PDF pour que le navigateur
// puisse l'afficher directement ici, sans téléchargement préalable.
function FilePreviewPanel({ fichier, onClose }) {
  const { t } = useTranslation()
  const [loaded, setLoaded] = useState(false)
  const [failed, setFailed] = useState(false)

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={onClose} />
      <div className="glass glass-rounded relative flex h-full w-full max-w-md flex-col overflow-hidden shadow-2xl sm:m-3 sm:h-[calc(100%-1.5rem)]">
        <div className="flex items-center gap-2 border-b border-white/10 px-4 py-3">
          <button
            type="button"
            onClick={onClose}
            className="glass glass-circle glass-interactive flex h-8 w-8 shrink-0 items-center justify-center"
            aria-label="close"
          >
            <svg viewBox="0 0 24 24" fill="none" strokeWidth="2" stroke="currentColor" className="h-4 w-4">
              <path strokeLinecap="round" d="M6 6l12 12M18 6L6 18" />
            </svg>
          </button>
          <span className="min-w-0 flex-1 truncate text-sm font-medium">
            {fichier.titre || fichier.type_fichier}
          </span>
          <a
            href={urlTelechargement(fichier.id)}
            className="glass-btn glass-pill shrink-0 px-3 py-1.5 text-xs"
          >
            {t('generated.download')}
          </a>
        </div>

        <div className="relative flex-1">
          {!loaded && !failed && (
            <div className="absolute inset-0 flex items-center justify-center text-xs text-white/40">
              {t('generated.loadingPreview')}
            </div>
          )}
          {failed ? (
            <div className="absolute inset-0 flex items-center justify-center px-6 text-center text-xs text-white/40">
              {t('generated.previewUnavailable')}
            </div>
          ) : (
            <iframe
              title={fichier.titre || fichier.type_fichier}
              src={urlApercu(fichier.id)}
              onLoad={() => setLoaded(true)}
              onError={() => setFailed(true)}
              className="h-full w-full bg-white/5"
            />
          )}
        </div>
      </div>
    </div>
  )
}

export default FilePreviewPanel
