import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { envoyerMessage, getConversations, getHistorique } from '../services/chat'
import { genererDocument } from '../services/generation'
import ChatMessage from './ChatMessage'

function ThinkingIndicator() {
  const { t } = useTranslation()
  return (
    <div className="flex justify-start">
      <div className="glass flex items-center gap-2 rounded-3xl rounded-bl-md px-4 py-3">
        <span className="text-xs text-3">{t('chat.thinking')}</span>
        <span className="flex gap-1">
          <span className="thinking-dot h-1.5 w-1.5 rounded-full bg-white/60" style={{ animationDelay: '0ms' }} />
          <span className="thinking-dot h-1.5 w-1.5 rounded-full bg-white/60" style={{ animationDelay: '150ms' }} />
          <span className="thinking-dot h-1.5 w-1.5 rounded-full bg-white/60" style={{ animationDelay: '300ms' }} />
        </span>
      </div>
    </div>
  )
}

// Détecte si la demande de l'utilisateur est une demande de génération
// de document plutôt qu'une question sur le dossier, pour router vers
// le bon endpoint sans passer par un formulaire dédié.
const MOTS_GENERATION = [
  'genere', 'générer', 'generer', 'génère',
  'redige', 'rédige', 'rediger', 'rédiger',
  'produis', 'produire',
  'cree le document', 'crée le document', 'creer le document', 'créer le document',
  'cree un document', 'crée un document',
  'exporte', 'exporter', 'export',
  'telecharge', 'télécharge', 'telecharger', 'télécharger',
  'fournis-moi un fichier', 'fournis moi un fichier',
  'donne-moi le document', 'donne moi le document',
  'generate', 'draft the document', 'write the document', 'create the document',
]

function normaliser(texte) {
  return texte
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
}

function estUneDemandeDeGeneration(texte) {
  const normalise = normaliser(texte)
  if (MOTS_GENERATION.some((mot) => normalise.includes(normaliser(mot)))) return true
  // Mentionner explicitement un format de fichier téléchargeable est en
  // soi un signal fort de demande de document, même sans verbe
  // déclencheur ("... en Excel", "... au format pdf", etc.) — c'est ce
  // qui manquait et faisait répondre le RAG au lieu de générer le fichier.
  return ['xlsx', 'excel', 'pdf', 'docx', 'word', 'tableur', 'spreadsheet'].some((mot) =>
    normalise.includes(mot)
  )
}

// Déduit le format demandé à partir du texte du message (mentionné en
// toutes lettres). DOCX reste le format par défaut si rien n'est précisé.
function detecterFormat(texte) {
  const normalise = normaliser(texte)
  if (normalise.includes('xlsx') || normalise.includes('excel') || normalise.includes('tableur') || normalise.includes('spreadsheet')) {
    return 'xlsx'
  }
  if (normalise.includes('pdf')) {
    return 'pdf'
  }
  return 'docx'
}

let compteurMessages = 0
function nouvelIdMessage() {
  compteurMessages += 1
  return `msg-${Date.now()}-${compteurMessages}`
}

function ChatWindow({ dossierId, dossierNom, onFichierGenere }) {
  const { t } = useTranslation()
  const [messages, setMessages] = useState([])
  const [conversationId, setConversationId] = useState(null)
  const [question, setQuestion] = useState('')
  const [enCours, setEnCours] = useState(false)
  const [chargementHistorique, setChargementHistorique] = useState(true)
  const bottomRef = useRef(null)
  // Passe à true dès le premier message envoyé par l'utilisateur dans
  // cette session : au-delà de ce point, plus rien ne doit jamais
  // remplacer `messages` par un historique venu du serveur, même en
  // cas d'effet relancé en retard — seul un ajout (append) est permis.
  const conversationDemarreeRef = useRef(false)

  useEffect(() => {
    // `cancelled` évite qu'un chargement d'historique en retard (double
    // appel en mode développement, ou changement de dossier) n'écrase
    // des messages déjà envoyés par l'utilisateur entre-temps — c'est
    // ce qui causait la disparition de nouveaux messages.
    let cancelled = false

    async function chargerHistorique() {
      try {
        const conversations = await getConversations(dossierId)
        if (cancelled || conversationDemarreeRef.current) return
        if (conversations.length > 0) {
          const derniere = conversations[0]
          const historique = await getHistorique(derniere.id)
          if (cancelled || conversationDemarreeRef.current) return
          setConversationId(derniere.id)
          setMessages(
            historique.map((m) => ({ id: nouvelIdMessage(), role: m.role, content: m.content }))
          )
        }
      } catch (err) {
        if (!cancelled) console.error(err)
      } finally {
        if (!cancelled) setChargementHistorique(false)
      }
    }
    chargerHistorique()

    return () => {
      cancelled = true
    }
  }, [dossierId])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, enCours])

  const handleEnvoyer = async (e) => {
    e.preventDefault()
    if (!question.trim() || enCours) return

    conversationDemarreeRef.current = true

    const texteEnvoye = question
    const idMessageUtilisateur = nouvelIdMessage()
    setMessages((prev) => [...prev, { id: idMessageUtilisateur, role: 'user', content: texteEnvoye }])
    setQuestion('')
    setEnCours(true)

    // Fonctionnement normal : si le message ressemble à une demande de
    // génération de document, on appelle directement le service de
    // génération, dans le format mentionné dans le message (docx par
    // défaut) — le fichier obtenu s'affichera ensuite à droite de la
    // discussion ; sinon on pose la question normalement au RAG.
    if (estUneDemandeDeGeneration(texteEnvoye)) {
      try {
        const format = detecterFormat(texteEnvoye)
        const resultat = await genererDocument(dossierId, texteEnvoye, format, conversationId)
        setConversationId(resultat.conversation_id)
        setMessages((prev) => [
          ...prev,
          { id: nouvelIdMessage(), role: 'assistant', content: t('chat.fileGenerated', { titre: resultat.titre }) },
        ])
        onFichierGenere?.()
      } catch (err) {
        setMessages((prev) => [...prev, { id: nouvelIdMessage(), role: 'assistant', content: `⚠️ ${err.message}` }])
      } finally {
        setEnCours(false)
      }
      return
    }

    try {
      const resultat = await envoyerMessage(dossierId, texteEnvoye, conversationId)
      setConversationId(resultat.conversation_id)
      setMessages((prev) => [
        ...prev,
        { id: nouvelIdMessage(), role: 'assistant', content: resultat.answer, sources: resultat.sources },
      ])
    } catch (err) {
      setMessages((prev) => [...prev, { id: nouvelIdMessage(), role: 'assistant', content: `⚠️ ${err.message}` }])
    } finally {
      setEnCours(false)
    }
  }

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="bar-solid flex items-center gap-2 border-b border-soft px-4 py-3 sm:px-5">
        <Link
          to="/"
          className="glass glass-circle glass-interactive flex h-8 w-8 shrink-0 items-center justify-center text-1"
          aria-label={t('chat.back')}
        >
          <svg viewBox="0 0 24 24" fill="none" strokeWidth="2" stroke="currentColor" className="h-4 w-4">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
        </Link>
        <span className="text-sm font-medium text-1">{dossierNom || t('chat.back')}</span>
      </div>

      {/* Conteneur relatif : la liste de messages occupe tout l'espace
          (position absolue) et passe donc réellement derrière la barre
          de saisie, elle-même positionnée en absolu par-dessus. */}
      <div className="relative min-h-0 flex-1">
        <div className="absolute inset-0 flex flex-col gap-3 overflow-y-auto px-4 pb-24 pt-4 sm:px-5">
          {chargementHistorique ? (
            <div className="flex h-full items-center justify-center text-sm text-3">
              {t('chat.historyLoading')}
            </div>
          ) : messages.length === 0 ? (
            <div className="flex h-full items-center justify-center px-6 text-center text-sm text-3">
              {t('chat.emptyState')}
            </div>
          ) : (
            messages.map((msg) => <ChatMessage key={msg.id} message={msg} />)
          )}
          {enCours && <ThinkingIndicator />}
          <div ref={bottomRef} />
        </div>

        <form
          onSubmit={handleEnvoyer}
          className="bar-floating glass-pill absolute inset-x-3 bottom-3 flex gap-2 p-1.5 shadow-2xl sm:inset-x-4"
        >
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder={t('chat.placeholder')}
            className="glass-input glass-pill flex-1 border-none bg-transparent px-4 py-2.5 text-sm text-1 shadow-none"
          />
          <button
            type="submit"
            disabled={enCours || !question.trim()}
            className="glass-btn glass-pill shrink-0 px-5 py-2.5 text-sm"
          >
            {t('chat.send')}
          </button>
        </form>
      </div>
    </div>
  )
}

export default ChatWindow
