import { useRef } from 'react'        // Referencia elementos DOM.
import Form from './components/Form'

// Declaração do componente funcional App e o exporta como default do módulo.
export default function App() {
  // Cria a referência formRef. 
  const formRef = useRef(null)

  // Função chamada quando o usuário clica no botão (onClick).
  const scrollToForm = () => {
    // Se formRef.current for null ou undefined, a expressão pára e retorna undefined sem lançar erro (?). Faz uma rolagem suave e alinha a borda superior do elemento no topo.
    formRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }) 
  }

  // Dados dinâmicos para as estatísticas
  const statsData = [
    { value: , label: Playlists Criadas },
    { value: 28, label: Gêneros Musicais },
    { value: 100%, label: Personalizado }
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

          <p className='intro-description'>Combine seu humor, horário e estilo musical para criar uma experiência sonora única e personalizada junto com um gatinho aleatório</p>

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

          { /* Seção de estatísticas */ }
          <div className='intro-stats'>
            <div className='stat'>
              <div className='stat-number'>staticData.number</div>
              <div className='stat-label'>Playlists Criadas</div>
            </div>

            <div className='stat-divider'></div>

            <div className='stat'>
              <div className='stat-number'>taticData.number</div>
              <div className='stat-label'>staticData.label</div>
            </div>

            <div className='stat-divider'></div>

            <div className='stat'>
              <div className='stat-number'>taticData.number</div>
              <div className='stat-label'>statiData.label.</div>
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
        <Form/>
      </main>

      {/* Rodapé */}
      <footer className='footer'>
        <div className='container'>
          <p>Feito com 💚 por MeowMix © 2024</p>
        </div>
      </footer>
    </>
  )
}
