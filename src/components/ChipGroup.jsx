import Chip from './Chip';

export default function ChipGroup({ items = [], selected = [], setSelected, single = false }) {
  const toggle = (val) => {
    if (single) {
      setSelected(selected[0] === val ? [] : [val]);
      return;
    }
    setSelected(prev => (prev.includes(val) ? prev.filter(x => x !== val) : [...prev, val]));
  };

  return (
    <div className='chip-group'>
      {items.map(item => (
        <Chip
          key={item.value}
          value={item.value}
          label={item.label}
          active={selected.includes(item.value)}
          onToggle={toggle} />
      ))}
    </div>
  );
}