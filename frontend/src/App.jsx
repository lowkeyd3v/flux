import { Routes, Route } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import HomePage from './pages/HomePage'
import VendorPage from './pages/VendorPage'

function App() {
  return (
    <MainLayout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/vendor" element={<VendorPage />} />
      </Routes>
    </MainLayout>
  )
}

export default App
