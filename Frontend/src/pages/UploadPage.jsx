import { Link, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import UploadDossier from '../components/UploadDossier'
import { lancerIngestion } from '../services/dossiers'

function UploadPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()

  const handleUploadSuccess = async (dossier) => {
    try {
      await lancerIngestion(dossier.id)
    } catch (err) {
      console.error(err)
    }
    navigate('/')
  }

  return (
    <div className="mx-auto w-full max-w-2xl flex-1 px-4 py-8 sm:px-6">
      <Link
        to="/"
        className="mb-6 inline-flex items-center gap-1.5 text-sm text-2 transition-colors hover:text-1"
      >
        <svg viewBox="0 0 24 24" fill="none" strokeWidth="2" stroke="currentColor" className="h-4 w-4">
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        {t('upload.back')}
      </Link>

      <div className="glass glass-rounded animate-fade-in-up p-6 sm:p-8">
        <h1 className="font-display text-2xl font-bold tracking-tight text-1">{t('upload.title')}</h1>
        <p className="mt-1 mb-6 text-sm text-2">{t('upload.subtitle')}</p>
        <UploadDossier onSuccess={handleUploadSuccess} />
      </div>
    </div>
  )
}

export default UploadPage
