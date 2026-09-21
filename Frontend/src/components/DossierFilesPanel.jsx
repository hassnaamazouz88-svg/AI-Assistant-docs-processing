import { useTranslation } from 'react-i18next'

const STATUS_DOT = {
  en_attente: 'bg-neutral-400',
  traite: 'bg-emerald-500/70',
  echec: 'bg-rose-500/70',
}

function fileIconPath(nom = '') {
  const ext = nom.split('.').pop()?.toLowerCase()
  if (ext === 'pdf') {
    return 'M7 3.5h6.5L18 8v11.5a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-15a1 1 0 0 1 1-1Z M13 3.5V8h5 M9 13h1.5a1.2 1.2 0 1 1 0 2.4H9v-2.4Zm0 2.4v1.6'
  }
  return 'M7 3.5h6.5L18 8v11.5a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-15a1 1 0 0 1 1-1Z M13 3.5V8h5'
}

function DossierFilesPanel({ documents = [] }) {
  const { t } = useTranslation()

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="border-b border-soft px-4 py-3">
        <h2 className="text-xs font-semibold uppercase tracking-wide text-3">
          {t('files.title')}
        </h2>
      </div>
      <div className="flex-1 space-y-1.5 overflow-y-auto p-3">
        {documents.length === 0 ? (
          <p className="px-2 py-4 text-center text-xs text-3">{t('files.empty')}</p>
        ) : (
          documents.map((doc) => (
            <div
              key={doc.id ?? doc.nom_fichier}
              className="glass glass-rounded flex items-center gap-2.5 px-3 py-2.5"
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                strokeWidth="1.5"
                stroke="currentColor"
                className="h-4 w-4 shrink-0 text-2 opacity-80"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d={fileIconPath(doc.nom_fichier)} />
              </svg>
              <span className="min-w-0 flex-1 truncate text-xs text-2" title={doc.nom_fichier}>
                {doc.nom_fichier}
              </span>
              <span
                className={`h-1.5 w-1.5 shrink-0 rounded-full ${STATUS_DOT[doc.statut_traitement] ?? STATUS_DOT.en_attente}`}
                title={t(`files.statuses.${doc.statut_traitement}`, doc.statut_traitement)}
              />
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default DossierFilesPanel
