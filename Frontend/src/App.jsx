import { Routes, Route } from 'react-router-dom'
import AuroraBackground from './components/AuroraBackground'
import Navbar from './components/Navbar'
import DossiersListPage from './pages/DossiersListPage'
import UploadPage from './pages/UploadPage'
import ChatPage from './pages/ChatPage'

function App() {
  return (
    <div className="relative flex min-h-screen flex-col">
      <AuroraBackground />
      <Navbar />
      <main className="flex min-h-0 flex-1 flex-col">
        <Routes>
          <Route path="/" element={<DossiersListPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/dossiers/:id/chat" element={<ChatPage />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
