import { Essay } from '../types';

interface Props {
  essays: Essay[];
  onCritique: (essayId: number) => void;
  loadingId?: number | null;
}

const preview = (content: string) => {
  if (content.length <= 160) {
    return content;
  }
  return `${content.slice(0, 160)}…`;
};

export const EssayFeedbackPanel = ({ essays, onCritique, loadingId }: Props) => {
  if (!essays.length) {
    return <p>No essays uploaded yet. Add your first draft to see AI-powered feedback.</p>;
  }

  return (
    <div className="grid">
      {essays.map((essay) => (
        <div key={essay.id} className="card">
          <h3>{essay.prompt}</h3>
          <p>{preview(essay.content)}</p>
          <button type="button" onClick={() => onCritique(essay.id)} disabled={loadingId === essay.id}>
            {loadingId === essay.id ? 'Requesting feedback…' : 'Request critique'}
          </button>
        </div>
      ))}
    </div>
  );
};
