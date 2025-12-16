import { useState, useEffect } from 'react';  
import ChipGroup from './ChipGroup';

// Arrays de objetos usados para popular ChipGroup.
const moodItems = [
  { value: 'alegre', label: 'Alegre' },
  { value: 'animado', label: 'Animado' },
  { value: 'ansioso', label: 'Ansioso' },
  { value: 'calmo', label: 'Calmo' },
  { value: 'concentrado', label: 'Concentrado' },
  { value: 'descontraido', label: 'Descontraído' },
  { value: 'frustracao', label: 'Frustração' },
  { value: 'melancolico', label: 'Melancólico' },
  { value: 'inspirado', label: 'Inspirado' },
  { value: 'preguicoso', label: 'Preguiçoso' },
  { value: 'raiva', label: 'Raiva' },
  { value: 'romantico', label: 'Romântico' },
];

const timeItems = [
  { value: 'manha', label: 'Manhã' },
  { value: 'tarde', label: 'Tarde' },
  { value: 'noite', label: 'Noite' },
  { value: 'madrugada', label: 'Madrugada' },
];

const goalItems = [
  { value: 'festa', label: 'Festa' },
  { value: 'treino', label: 'Treino' },
  { value: 'estudo', label: 'Estudo' },
  { value: 'foco', label: 'Foco' },
  { value: 'trabalho', label: 'Trabalho' },
  { value: 'viagem', label: 'Viagem' },
  { value: 'relaxar', label: 'Relaxar' },
  { value: 'meditacao', label: 'Meditação' },
  { value: 'nenhum', label: 'Nenhum' },
];

const genreItems = [
  { value: 'alternativo', label: 'Alternativo' },
  { value: 'arrocha', label: 'Arrocha' },
  { value: 'axe', label: 'Axé' },
  { value: 'blues', label: 'Blues' },
  { value: 'bossanova', label: 'Bossa Nova' },
  { value: 'classica', label: 'Clássica' },
  { value: 'country', label: 'Country' },
  { value: 'eletronica', label: 'Eletrônica' },
  { value: 'forro', label: 'Forró' },
  { value: 'funk', label: 'Funk' },
  { value: 'grunge', label: 'Grunge' },
  { value: 'hardrock', label: 'Hard Rock' },
  { value: 'indie', label: 'Indie' },
  { value: 'jazz', label: 'Jazz' },
  { value: 'lofi', label: 'Lo-fi' },
  { value: 'metal', label: 'Metal' },
  { value: 'mpb', label: 'MPB' },
  { value: 'pagode', label: 'Pagode' },
  { value: 'piseiro', label: 'Piseiro' },
  { value: 'pop', label: 'Pop' },
  { value: 'punk', label: 'Punk' },
  { value: 'rap', label: 'Rap' },
  { value: 'reggae', label: 'Reggae' },
  { value: 'rock', label: 'Rock' },
  { value: 'samba', label: 'Samba' }, 
  { value: 'sertanejo', label: 'Sertanejo' },
  { value: 'soul', label: 'Soul' },
  { value: 'trap', label: 'Trap' },
];

const rhythmItems = [
  { value: 'lento', label: 'Lento' },
  { value: 'moderado', label: 'Moderado' },
  { value: 'rapido', label: 'Rápido' },
];

const noveltyItems = [
  { value: 'novas', label: 'Apenas novas' },
  { value: 'classicas', label: 'Apenas clássicas' },
  { value: 'mix', label: 'Mix' },
];

const languageItems = [
  { value: 'chines', label: 'Chinês' },
  { value: 'coreano', label: 'Coreano' },
  { value: 'espanhol', label: 'Espanhol' },
  { value: 'ingles', label: 'Inglês' },
  { value: 'japones', label: 'Japonês' },
  { value: 'portugues', label: 'Português' },
  { value: 'mix', label: 'Mix' }
]

function errorsValidation(mood, timeOfDay, goal, genres, rhythm, language, novelty, limit) {
  // Validações básicas.
  const errors = [];
  if (mood.length === 0) errors.push('Escolha um humor');
  if (timeOfDay.length === 0) errors.push('Escolha o horário do dia');
  if (goal.length === 0) errors.push('Escolha uma finalidade para a playlist');
  if (genres.length === 0) errors.push('Escolha pelo menos 1 gênero');
  if (rhythm.length === 0) errors.push('Escolha um ritmo');
  if (language.length === 0) errors.push('Escolha um idioma');
  if (novelty.length === 0) errors.push('Escolha o tipo de novidade');
  if (!limit || limit < 5 || limit > 200) errors.push('Quantidade de músicas inválida (5–200)');

  if (errors.length) {
    alert(errors.join('\n'));
    return false;
  }

  return true;
}

async function login() {
  const result = await fetch('http://127.0.0.1:8000/login');
  const data = await result.json();
  window.location.href = data.url; // Redireciona para a página de login.
  return;
}

export default function Form({ setPlaylistCreated }) {
  // Estado para o link recebido da playlist.
  const [playlistUrl, setPlaylistUrl] = useState(null);

  // Estados (um state por grupo). useState([]) inicializa com array vazio.
  const [mood, setMood] = useState([]);                 
  const [timeOfDay, setTimeOfDay] = useState([]);
  const [goal, setGoal] = useState([]);             
  const [genres, setGenres] = useState([]);
  const [rhythm, setRhythm] = useState([]);
  const [language, setLanguage] = useState([]);       
  const [limit, setLimit] = useState(20);
  const [novelty, setNovelty] = useState([]);
  const [obs, setObs] = useState('');

  /* Captura o access_token quando o Spotify redireciona de volta (callback).
     Salva no localStorage para que o usuário mão precise logar de novamente.
  */
  useEffect(() => { 
    // Acessa parâmetros da URL.
    const params = new URLSearchParams(window.location.search); 

    const access_token_url = params.get("access_token");
    const refresh_token_url = params.get("refresh_token");

    if (access_token_url && refresh_token_url) {
      localStorage.setItem('access_token', access_token_url);
      localStorage.setItem('refresh_token', refresh_token_url);

      // Limpa a URL para não expor os tokens.
      window.history.replaceState({}, '', '/');
    }
  }, []); // Garante que esse efeito execute uma única vez.


  /* Verifica se o usuário já está logado.
     Se não estiver, manda para o login.
   */
  const handleSubmit = async (e) => {
    // Evita reload do formulário.
    e.preventDefault();
    
    if (!errorsValidation(mood, timeOfDay, goal, genres, rhythm, language, novelty, limit)) return;

    // Verifica o token (verifica se o usuário está logado).
    const access_token = localStorage.getItem('access_token')

    // Não logado, então inicia login.
    if (!access_token) {
      await login();
      return; 
    }
    
    // Monta o payload (dados de API).
    const payload = { mood, timeOfDay, goal, genres, rhythm, language, limit, novelty, obs, access_token, refresh_token: localStorage.getItem('refresh_token'), };

    // Envio pro backend.
    try {
      // Cria Playlists e adiciona músicas.
      const result = await fetch('https://meow-mix.onrender.com/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload), // Transforma en json.
      });
      if (!result.ok) {
        throw new Error(`Erro do servidor: ${result.status}`);
      }
      const data = await result.json();

      if (data.playlist_url) {
        setPlaylistUrl(data.playlist_url);
        setPlaylistCreated();
      }
    } catch (err) {
      console.error('Erro ao enviar ao backend:', err);
    }

    // localStorage.removeItem('access_token');
    // localStorage.removeItem('refresh_token');
  };

  return (
    <>
      <form className='card' onSubmit={handleSubmit}>
        <h3><i className='bi bi-music-note'></i>Humor desejado</h3>
        <ChipGroup items={moodItems} selected={mood} setSelected={setMood}/> 

        <h3><i className='bi bi-music-note'></i>Horário do dia</h3>
        <ChipGroup items={timeItems} selected={timeOfDay} setSelected={setTimeOfDay} single={true}/>

        <h3><i className='bi bi-music-note'></i>Finalidade da playlist</h3>
        <ChipGroup items={goalItems} selected={goal} setSelected={setGoal} single={true}/>

        <h3><i className='bi bi-music-note'></i>Gêneros preferidos</h3>
        <ChipGroup items={genreItems} selected={genres} setSelected={setGenres}/>

        <h3><i className='bi bi-music-note'></i>Ritmo preferido</h3>
        <ChipGroup items={rhythmItems} selected={rhythm} setSelected={setRhythm} single={true}/>

        <h3><i className='bi bi-music-note'></i>Idioma</h3>
        <ChipGroup items={languageItems} selected={language} setSelected={setLanguage}/>

        <h3><i className='bi bi-music-note'></i>Quantidade de músicas</h3>
        <input type='number' value={limit} onChange={(e) => setLimit(Number(e.target.value))} min='5' max='200'/>

        <h3><i className='bi bi-music-note'></i>Preferência por novidade</h3>
        <ChipGroup items={noveltyItems} selected={novelty} setSelected={setNovelty} single={true}/>

        <h3><i className='bi bi-music-note'></i>Observações</h3>
        <textarea value={obs} onChange={(e) => setObs(e.target.value)} rows='3' placeholder='Evitar os gêneros musicais: sertanejo, metal'/>

        <div>
          <button type='submit'>Gerar Playlist</button>
        </div>
      </form>
      
      {playlistUrl && (
        <div key={playlistUrl} className="playlist-result">
          <center><i className="bi bi-spotify"></i></center><p>Sua playlist está pronta!</p><br/>
          <a href={playlistUrl} target="_blank" rel="noopener noreferrer">Abrir playlist no Spotify</a>
        </div>
      )}
    </>
  );
}