// Not a real React component – just creates the entities as soon as it is rendered.
class StockSource extends window.React.Component {
    componentDidMount() {
      const { editorState, entityType, onComplete } = this.props;
  
      const content = editorState.getCurrentContent();
      const selection = editorState.getSelection();
  
      const demoStocks = ['AMD', 'AAPL', 'NEE', 'FSLR'];
      const randomStock = demoStocks[Math.floor(Math.random() * demoStocks.length)];
  
      // Uses the Draft.js API to create a new entity with the right data.
      const contentWithEntity = content.createEntity(
        entityType.type,
        'IMMUTABLE',
        { stock: randomStock },
      );
      const entityKey = contentWithEntity.getLastCreatedEntityKey();
  
      // We also add some text for the entity to be activated on.
      const text = `$${randomStock}`;
  
      const newContent = window.DraftJS.Modifier.replaceText(
        content,
        selection,
        text,
        null,
        entityKey,
      );
      const nextState = window.DraftJS.EditorState.push(
        editorState,
        newContent,
        'insert-characters',
      );
  
      onComplete(nextState);
    }
  
    render() {
      return null;
    }
}
const Stock = (props) => {
  const { entityKey, contentState } = props;
  const data = contentState.getEntity(entityKey).getData();

  return window.React.createElement(
    'a',
    {
      role: 'button',
      onMouseUp: () => {
        window.open(`https://finance.yahoo.com/quote/${data.stock}`);
      },
    },
    props.children,
  );
};

// Register the plugin directly on script execution so the editor loads it when initialising.
window.draftail.registerPlugin({
  type: 'STOCK',
  source: StockSource,
  decorator: Stock,
}, 'entityTypes');

document.querySelectorAll('[data-stock]').forEach((elt) => {
  const link = document.createElement('a');
  link.href = `https://finance.yahoo.com/quote/${elt.dataset.stock}`;
  link.innerHTML = `${elt.innerHTML}<svg width="50" height="20" stroke-width="2" stroke="blue" fill="rgba(0, 0, 255, .2)"><path d="M4 14.19 L 4 14.19 L 13.2 14.21 L 22.4 13.77 L 31.59 13.99 L 40.8 13.46 L 50 11.68 L 59.19 11.35 L 68.39 10.68 L 77.6 7.11 L 86.8 7.85 L 96 4" fill="none"></path><path d="M4 14.19 L 4 14.19 L 13.2 14.21 L 22.4 13.77 L 31.59 13.99 L 40.8 13.46 L 50 11.68 L 59.19 11.35 L 68.39 10.68 L 77.6 7.11 L 86.8 7.85 L 96 4 V 20 L 4 20 Z" stroke="none"></path></svg>`;

  elt.innerHTML = '';
  elt.appendChild(link);
});