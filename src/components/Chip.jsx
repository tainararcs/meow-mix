export default function Chip({ value, label, active, onToggle }) {
  return (
    <button type='button'
      className={`chip ${active ? 'active' : ''}`}
      onClick={() => onToggle(value)} >
      {label}
    </button>
  );
}