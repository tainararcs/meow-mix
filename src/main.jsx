import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// Cria a árvore DOM a partir da div com ID root.
// <App/>: Renderiza o componente App (componente principal/raiz da aplicação).
createRoot(document.getElementById('root')).render(
  <StrictMode> 
    <App/> 
  </StrictMode>,
)