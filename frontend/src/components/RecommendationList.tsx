import { Suggestion } from '../types';

interface Props {
  suggestions: Suggestion[];
  onAcknowledge?: (suggestionId: number) => void;
  onArchive?: (suggestionId: number) => void;
}

export const RecommendationList = ({ suggestions, onAcknowledge, onArchive }: Props) => {
  if (!suggestions.length) {
    return <p>No recommendations yet. Trigger an evaluation to get started.</p>;
  }

  return (
    <div className="grid grid--two">
      {suggestions.map((suggestion) => (
        <div key={suggestion.id} className="card">
          <h3>{suggestion.title}</h3>
          <p>{suggestion.description}</p>
          <p>
            <strong>Impact:</strong> {suggestion.impact ?? 'TBD'} | <strong>Effort:</strong>{' '}
            {suggestion.effort ?? 'TBD'}
          </p>
          {suggestion.deadline && (
            <p>
              <strong>Suggested deadline:</strong>{' '}
              {new Date(suggestion.deadline).toLocaleDateString()}
            </p>
          )}
          <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.75rem' }}>
            {onAcknowledge && (
              <button
                type="button"
                onClick={() => onAcknowledge(suggestion.id)}
                disabled={!!suggestion.acknowledged_at}
              >
                {suggestion.acknowledged_at ? 'Acknowledged' : 'Acknowledge'}
              </button>
            )}
            {onArchive && (
              <button type="button" onClick={() => onArchive(suggestion.id)}>
                Archive
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};
