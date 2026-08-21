import { Routes, Route } from 'react-router-dom'
import { LanguageProvider } from './context/LanguageContext'
import MainLayout from './layouts/MainLayout'
import HomePage from './pages/HomePage'
import VendorPage from './pages/VendorPage'

function App() {
  return (
    <LanguageProvider>
      <MainLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/vendor" element={<VendorPage />} />
        </Routes>
      </MainLayout>
    </LanguageProvider>
  )
}

export default App
