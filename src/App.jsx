import { useRef, useState } from 'react'  // Referencia elementos DOM.
import Form from './components/Form'

export default function App() {
  // Cria uma referência referência para o formulário para rolagem da página. 
  const formRef = useRef(null)

  // Implementa a rolagem para exibir o formulário.
  const scrollToForm = () => {
    formRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }) 
  }
  
  // Estado para a contagem de playlist criadas. Inicializa o contador com o valor do localStorage.
  const [playlistCreated, setPlaylistCreated] = useState(() => { 
    const created = localStorage.getItem('playlistsCreated')
    return created ? Number(created) : 0 // Converte o valor.
  })

  // Incrementa o contador de playlists criadas.
  const handlePlaylistCreated = () => {
    setPlaylistCreated(prev => {
      const count = prev + 1
      localStorage.setItem('playlistsCreated', count)
      return count
    })
  }
  
  // Dados dinâmicos para as estatísticas.
  const statsData = [
    { label: 'Playlists Criadas' },
    { number: '28', label: 'Gêneros Musicais' },
    { number: '100%', label: 'Personalizado' }
  ]

  return (
    <>
      {/* Seção de introdução */}
      <section className='intro'>
        <div className='intro-background'>
          <div className='intro-glow intro-glow-1'></div>
          <div className='intro-glow intro-glow-2'></div>
          <div className='intro-glow intro-glow-3'></div>
        </div>

        <div className='container intro-content'>
          <div className='intro-badge'>
            <span className='pulse-dot'></span>Powered by AI
          </div>

          <h1 className='intro-title'>🐱 MeowMix</h1>

          <p className='intro-subtitle'>A playlist perfeita para cada momento da sua vida</p>

          <p className='intro-description'>Combine seu humor, horário e estilo musical e descubra uma playlist única com a companhia de um gatinho surpresa!</p>

          <div className='intro-features'>
            <div className='feature-item'>
              <span className='feature-icon'><i className='bi bi-headphones'></i></span>
              <span>Personalização Total</span>
            </div>

            <div className='feature-item'>
              <span className='feature-icon'><i className='bi bi-robot'></i></span>
              <span>IA Avançada</span>
            </div>

            <div className='feature-item'>
              <span className='feature-icon'><i className='bi bi-fast-forward-fill'></i></span>
              <span>Resultado Instantâneo</span>
            </div>
          </div>

          <button className='btn-playlist' onClick={scrollToForm}>
            <span>Criar Minha Playlist</span>
            <svg width='20' height='20' viewBox='0 0 20 20' fill='none'>
              <path d='M10 4V16M10 16L4 10M10 16L16 10' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round'/>
            </svg>
          </button>

          <div className='intro-stats'>
            <div className='stat'>
              <div className='stat-number'>{playlistCreated}</div>
              <div className='stat-label'>{statsData[0].label}</div>
            </div>

            <div className='stat-divider'></div>

            <div className='stat'>
              <div className='stat-number'>{statsData[1].number}</div>
              <div className='stat-label'>{statsData[1].label}</div>
            </div>

            <div className='stat-divider'></div>

            <div className='stat'>
              <div className='stat-number'>{statsData[2].number}</div>
              <div className='stat-label'>{statsData[2].label}</div>
            </div>
          </div>
        </div>

        <div className='scroll-indicator'>
          <div className='scroll-mouse'>
            <div className='scroll-wheel'></div>
          </div>
        </div>
      </section>

      {/* Seção de formulário */}
      <main className='container form-section' ref={formRef}>
        <div className='section-header'>
          <h2 className='section-title'><i className='bi bi-music-note-list'></i> Configure Sua Playlist</h2>
          <p className='section-subtitle'>Responda algumas perguntas e deixe a magia acontecer</p>
        </div>
        <Form setPlaylistCreated={handlePlaylistCreated}/>
      </main>

      {/* Rodapé */}
      <footer className='footer'>
        <div className='container'>
          <p>Feito com 💚 por MeowMix</p>
          <p>© 2025</p>
        </div>
      </footer>
    </>
  )
}