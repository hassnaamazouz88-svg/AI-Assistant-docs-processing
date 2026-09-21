import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import ChatWindow from '../components/ChatWindow'
import DossierFilesPanel from '../components/DossierFilesPanel'
import GeneratedFilesPanel from '../components/GeneratedFilesPanel'
import PreviewPanel from '../components/PreviewPanel'
import { getDossier } from '../services/dossiers'
import { getFichiersGeneres } from '../services/generation'

function DrawerToggle({ label, active, onClick, icon }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`glass glass-pill glass-interactive flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium lg:hidden ${
        active ? 'bg-white/15' : ''
      }`}
    >
      {icon}
      {label}
    </button>
  )
}

function Drawer({ open, onClose, children, side }) {
  if (!open) return null
  return (
    <div className="fixed inset-0 z-50 flex lg:hidden" role="dialog">
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />
      <div
        className={`glass relative flex h-full w-72 max-w-[80vw] flex-col ${
          side === 'right' ? 'ml-auto' : ''
        }`}
      >
        <button
          type="button"
          onClick={onClose}
          className="glass glass-circle absolute right-3 top-3 flex h-7 w-7 items-center justify-center"
        >
          <svg viewBox="0 0 24 24" fill="none" strokeWidth="2" stroke="currentColor" className="h-3.5 w-3.5">
            <path strokeLinecap="round" d="M6 6l12 12M18 6L6 18" />
          </svg>
        </button>
        {children}
      </div>
    </div>
  )
}

function ChatPage() {
  const { id } = useParams()
  const { t } = useTranslation()
  const [dossier, setDossier] = useState(null)
  const [fichiers, setFichiers] = useState([])
  const [chargementFichiers, setChargementFichiers] = useState(true)
  const [drawer, setDrawer] = useState(null) // 'files' | 'generated' | null
  // Fichier actuellement prévisualisé : le panneau (PreviewPanel)
  // ne se monte que lorsque cette valeur n'est pas nulle — donc jamais
  // affiché tant que l'utilisateur n'a pas cliqué sur "Aperçu".
  const [previewFichier, setPreviewFichier] = useState(null)

  useEffect(() => {
    getDossier(id).then(setDossier).catch(console.error)
  }, [id])

  const refreshFichiers = () => {
    setChargementFichiers(true)
    getFichiersGeneres(id)
      .then(setFichiers)
      .catch(console.error)
      .finally(() => setChargementFichiers(false))
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    refreshFichiers()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id])

  // Il n'y a plus de formulaire de génération séparé : on demande un
  // document normalement dans la discussion (voir ChatWindow), et la
  // colonne de droite n'apparaît que lorsqu'un fichier généré existe.
  const aDesFichiersGeneres = fichiers.length > 0

  return (
    <div className="mx-auto flex min-h-0 w-full max-w-[1600px] flex-1 flex-col px-4 pb-4 sm:px-6">
      <div className="mb-3 flex justify-center gap-2 lg:hidden">
        <DrawerToggle label={t('chat.toggleFiles')} active={drawer === 'files'} onClick={() => setDrawer('files')} />
        {aDesFichiersGeneres && (
          <DrawerToggle
            label={t('chat.toggleGenerated')}
            active={drawer === 'generated'}
            onClick={() => setDrawer('generated')}
          />
        )}
      </div>

      <div
        className={`grid min-h-0 flex-1 gap-4 ${
          aDesFichiersGeneres ? 'lg:grid-cols-[260px_1fr_300px]' : 'lg:grid-cols-[260px_1fr]'
        }`}
      >
        <aside className="glass glass-rounded hidden min-h-0 overflow-hidden lg:block">
          <DossierFilesPanel documents={dossier?.documents ?? []} />
        </aside>

        <div className="glass glass-rounded flex min-h-0 flex-col overflow-hidden">
          <ChatWindow dossierId={id} dossierNom={dossier?.nom} onFichierGenere={refreshFichiers} />
        </div>

        {aDesFichiersGeneres && (
          <aside className="glass glass-rounded hidden min-h-0 overflow-hidden lg:block">
            <GeneratedFilesPanel
              fichiers={fichiers}
              chargement={chargementFichiers}
              onPreview={setPreviewFichier}
            />
          </aside>
        )}
      </div>

      <Drawer open={drawer === 'files'} onClose={() => setDrawer(null)} side="left">
        <DossierFilesPanel documents={dossier?.documents ?? []} />
      </Drawer>
      {aDesFichiersGeneres && (
        <Drawer open={drawer === 'generated'} onClose={() => setDrawer(null)} side="right">
          <GeneratedFilesPanel
            fichiers={fichiers}
            chargement={chargementFichiers}
            onPreview={setPreviewFichier}
          />
        </Drawer>
      )}

      {/* Ne se rend que si previewFichier est renseigné — voir PreviewPanel.jsx */}
      <PreviewPanel fichier={previewFichier} onClose={() => setPreviewFichier(null)} />
    </div>
  )
}

export default ChatPage
