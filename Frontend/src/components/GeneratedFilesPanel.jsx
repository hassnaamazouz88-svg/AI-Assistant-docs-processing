import { useTranslation } from 'react-i18next'
import { urlTelechargement } from '../services/generation'

function GeneratedFileRow({ fichier, onPreview }) {
  const { t } = useTranslation()
  return (
    <div className="glass glass-rounded flex flex-col gap-2 px-3 py-3">
      <div className="flex items-start gap-2.5">
        <svg viewBox="0 0 24 24" fill="none" strokeWidth="1.5" stroke="currentColor" className="h-4 w-4 shrink-0 text-2 opacity-80 mt-0.5">
          <path strokeLinecap="round" strokeLinejoin="round" d="M7 3.5h6.5L18 8v11.5a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-15a1 1 0 0 1 1-1Z" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M13 3.5V8h5" />
        </svg>
        <div className="min-w-0 flex-1">
          <p className="truncate text-xs font-medium text-1">{fichier.titre || fichier.type_fichier}</p>
          <p className="text-[10px] uppercase tracking-wide text-3">{fichier.type_fichier}</p>
        </div>
      </div>
      <div className="flex gap-1.5">
        {/* Bouton, pas un lien : ouvre l'aperçu dans le panneau à la
            demande (voir PreviewPanel), au lieu d'un nouvel onglet. */}
        <button
          type="button"
          onClick={() => onPreview(fichier)}
          className="glass glass-pill glass-interactive flex-1 px-2.5 py-1.5 text-center text-[11px] font-medium text-1"
        >
          {t('generated.preview')}
        </button>
        <a
          href={urlTelechargement(fichier.id)}
          className="glass-btn glass-pill flex-1 px-2.5 py-1.5 text-center text-[11px]"
        >
          {t('generated.download')}
        </a>
      </div>
    </div>
  )
}

// Ce panneau n'a plus de formulaire : la génération se déclenche
// normalement, en le demandant dans la discussion. Il liste simplement
// les documents déjà générés et n'apparaît (voir ChatPage) que lorsque
// la liste n'est pas vide.
function GeneratedFilesPanel({ fichiers, chargement, onPreview }) {
  const { t } = useTranslation()

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="border-b border-soft px-4 py-3">
        <h2 className="text-xs font-semibold uppercase tracking-wide text-3">
          {t('generated.title')}
        </h2>
      </div>

      <div className="flex-1 space-y-2 overflow-y-auto p-3">
        {chargement ? (
          <div className="skeleton glass-rounded h-16 w-full border border-soft" />
        ) : fichiers.length === 0 ? (
          <div className="px-2 py-4 text-center">
            <p className="text-xs text-3">{t('generated.empty')}</p>
            <p className="mt-1 text-[11px] text-3">{t('generated.emptyHint')}</p>
          </div>
        ) : (
          fichiers.map((f) => <GeneratedFileRow key={f.id} fichier={f} onPreview={onPreview} />)
        )}
      </div>
    </div>
  )
}

export default GeneratedFilesPanel
