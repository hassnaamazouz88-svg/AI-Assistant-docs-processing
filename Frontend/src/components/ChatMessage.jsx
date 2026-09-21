import { useTranslation } from 'react-i18next'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const markdownComponents = {
  p: ({ children }) => <p className="mb-2 last:mb-0 leading-relaxed">{children}</p>,
  strong: ({ children }) => <strong className="font-semibold text-1">{children}</strong>,
  em: ({ children }) => <em className="italic">{children}</em>,
  h1: ({ children }) => <h1 className="mt-1 mb-2 font-display text-base font-bold">{children}</h1>,
  h2: ({ children }) => <h2 className="mt-1 mb-2 font-display text-[15px] font-bold">{children}</h2>,
  h3: ({ children }) => <h3 className="mt-1 mb-1.5 font-display text-sm font-bold">{children}</h3>,
  ul: ({ children }) => <ul className="mb-2 ml-4 list-disc space-y-1 last:mb-0">{children}</ul>,
  ol: ({ children }) => <ol className="mb-2 ml-4 list-decimal space-y-1 last:mb-0">{children}</ol>,
  li: ({ children }) => <li className="leading-relaxed">{children}</li>,
  a: ({ children, href }) => (
    <a href={href} target="_blank" rel="noreferrer" className="text-[var(--aurora-2)] underline underline-offset-2">
      {children}
    </a>
  ),
  code: ({ children }) => (
    <code className="rounded bg-white/10 px-1 py-0.5 font-mono text-[0.85em]">{children}</code>
  ),
  blockquote: ({ children }) => (
    <blockquote className="mb-2 border-l-2 border-soft pl-3 text-2 last:mb-0">{children}</blockquote>
  ),
  hr: () => <hr className="my-2 border-soft" />,
  table: ({ children }) => (
    <div className="mb-2 overflow-x-auto last:mb-0">
      <table className="w-full border-collapse text-xs">{children}</table>
    </div>
  ),
  th: ({ children }) => <th className="border-b border-soft px-2 py-1 text-left font-semibold text-1">{children}</th>,
  td: ({ children }) => <td className="border-b border-soft px-2 py-1 align-top text-2">{children}</td>,
}

function ChatMessage({ message }) {
  const { t } = useTranslation()
  const estUtilisateur = message.role === 'user'

  return (
    <div className={`flex w-full min-w-0 ${estUtilisateur ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`glass min-w-0 max-w-[80%] break-words rounded-3xl px-4 py-2.5 ${
          estUtilisateur ? 'bubble-user rounded-br-md' : 'rounded-bl-md'
        }`}
      >
        {estUtilisateur ? (
          <p className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</p>
        ) : (
          <div className="text-sm text-1">
            <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
              {message.content}
            </ReactMarkdown>
          </div>
        )}
        {message.sources && message.sources.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1.5 border-t border-soft pt-2">
            <span className="text-[10px] font-medium uppercase tracking-wide text-3">
              {t('chat.sources')}
            </span>
            {message.sources.map((s, i) => (
              <span
                key={i}
                className="chip inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[11px]"
              >
                📄 {s.nom_fichier}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default ChatMessage
