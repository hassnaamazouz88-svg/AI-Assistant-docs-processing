import { useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { uploadDossier } from '../services/dossiers'

function UploadDossier({ onSuccess }) {
  const { t } = useTranslation()
  const [nom, setNom] = useState('')
  const [files, setFiles] = useState([])
  const [enCours, setEnCours] = useState(false)
  const [erreur, setErreur] = useState(null)
  const [dragActive, setDragActive] = useState(false)
  const inputRef = useRef(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!nom.trim() || files.length === 0) {
      setErreur(t('upload.validationError'))
      return
    }

    setEnCours(true)
    setErreur(null)

    try {
      const dossier = await uploadDossier(nom, files)
      onSuccess(dossier)
      setNom('')
      setFiles([])
    } catch (err) {
      setErreur(err.message)
    } finally {
      setEnCours(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragActive(false)
    if (e.dataTransfer.files?.length) {
      setFiles(Array.from(e.dataTransfer.files))
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-5">
      <div>
        <label className="mb-1.5 block text-sm font-medium text-2">{t('upload.name')}</label>
        <input
          type="text"
          value={nom}
          onChange={(e) => setNom(e.target.value)}
          className="glass-input glass-rounded w-full px-4 py-2.5 text-sm text-1"
          placeholder={t('upload.namePlaceholder')}
        />
      </div>

      <div>
        <label className="mb-1.5 block text-sm font-medium text-2">{t('upload.files')}</label>
        <div
          onClick={() => inputRef.current?.click()}
          onDragOver={(e) => {
            e.preventDefault()
            setDragActive(true)
          }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          className={`glass-rounded flex cursor-pointer flex-col items-center gap-2 border border-dashed px-4 py-8 text-center transition-colors ${
            dragActive ? 'border-[var(--aurora-2)] bg-white/10' : 'border-soft hover:border-[var(--aurora-2)]/50'
          }`}
        >
          <svg viewBox="0 0 24 24" fill="none" strokeWidth="1.5" stroke="currentColor" className="h-8 w-8 opacity-60">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 16V4m0 0l-4 4m4-4l4 4M4 16.5V19a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2.5"
            />
          </svg>
          <p className="text-sm text-2">{t('upload.dropHint')}</p>
          <p className="text-xs text-3">{t('upload.filesHint')}</p>
          <input
            ref={inputRef}
            type="file"
            multiple
            onChange={(e) => setFiles(Array.from(e.target.files))}
            className="hidden"
            accept=".pdf,.docx,.doc,.xlsx,.zip"
          />
        </div>
        {files.length > 0 && (
          <ul className="mt-3 flex flex-col gap-1.5">
            {files.map((f, i) => (
              <li
                key={`${f.name}-${i}`}
                className="glass glass-rounded flex items-center justify-between px-3 py-2 text-xs text-2"
              >
                <span className="truncate">{f.name}</span>
                <span className="ml-2 shrink-0 text-3">{(f.size / 1024).toFixed(0)} Ko</span>
              </li>
            ))}
          </ul>
        )}
        {files.length > 0 && (
          <p className="mt-2 text-xs text-3">
            {t('upload.filesSelected', { count: files.length })}
          </p>
        )}
      </div>

      {erreur && (
        <p className="glass glass-rounded border-[var(--aurora-3)]/30 px-3 py-2 text-sm text-[var(--aurora-3)]">
          {erreur}
        </p>
      )}

      <button type="submit" disabled={enCours} className="glass-btn glass-pill px-4 py-2.5 text-sm">
        {enCours ? t('upload.submitting') : t('upload.submit')}
      </button>
    </form>
  )
}

export default UploadDossier
