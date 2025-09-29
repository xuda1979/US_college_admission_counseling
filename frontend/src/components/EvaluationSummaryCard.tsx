import { Evaluation } from '../types';

const formatDate = (value?: string | null) => {
  if (!value) return 'Latest Evaluation';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? 'Latest Evaluation' : date.toLocaleDateString();
};

export const EvaluationSummaryCard = ({ evaluation }: { evaluation: Evaluation }) => {
  return (
    <div className="card">
      <h3>{formatDate(evaluation.created_at)}</h3>
      <p>{evaluation.summary ?? 'No summary available yet.'}</p>
      {evaluation.scores && (
        <ul>
          {Object.entries(evaluation.scores).map(([key, value]) => (
            <li key={key}>
              <strong>{key}:</strong> {String(value)}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
