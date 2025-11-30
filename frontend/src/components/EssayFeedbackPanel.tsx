import { Essay } from '../types';
import { MessageSquare, Edit3 } from 'lucide-react';

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
    return (
      <div className="empty-state">
        <Edit3 size={48} className="empty-icon" />
        <p>No essays uploaded yet. Add your first draft to see AI-powered feedback.</p>
      </div>
    );
  }

  return (
    <div className="essay-grid">
      {essays.map((essay) => (
        <div key={essay.id} className="card essay-card">
          <div className="essay-content">
            <h3>{essay.prompt}</h3>
            <p className="essay-preview">{preview(essay.content)}</p>
          </div>
          <div className="essay-actions">
            <button
              type="button"
              onClick={() => onCritique(essay.id)}
              disabled={loadingId === essay.id}
              className="critique-button"
            >
              <MessageSquare size={16} />
              {loadingId === essay.id ? 'Requesting feedback…' : 'Request critique'}
            </button>
          </div>
        </div>
      ))}
      <style>{`
        .essay-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
          gap: 1.5rem;
        }

        .essay-card {
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          height: 100%;
        }

        .essay-content h3 {
          font-size: 1.1rem;
          margin-top: 0;
          margin-bottom: 0.75rem;
          line-height: 1.4;
        }

        .essay-preview {
          color: #64748b;
          font-size: 0.95rem;
          margin-bottom: 1.5rem;
        }

        .essay-actions {
          padding-top: 1rem;
          border-top: 1px solid #e2e8f0;
        }

        .critique-button {
          width: 100%;
          justify-content: center;
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
        }

        .empty-state {
          text-align: center;
          padding: 4rem 2rem;
          background: white;
          border-radius: 1rem;
          color: #64748b;
        }

        .empty-icon {
          margin-bottom: 1rem;
          opacity: 0.5;
        }
      `}</style>
    </div>
  );
};
