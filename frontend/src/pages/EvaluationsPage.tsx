import {
  useEvaluations,
  useRefreshSuggestions,
  useTriggerEvaluation
} from '../api/hooks';
import { EvaluationSummaryCard } from '../components/EvaluationSummaryCard';

const EvaluationsPage = () => {
  const { data: evaluations = [], isLoading } = useEvaluations();
  const triggerEvaluation = useTriggerEvaluation();
  const refreshSuggestions = useRefreshSuggestions();

  return (
    <div className="grid">
      <header className="card">
        <h2>Evaluation History</h2>
        <p>
          Generate on-demand assessments to understand how admissions reviewers might perceive your application. Each run stores
          a snapshot so you can track growth.
        </p>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          <button type="button" onClick={() => triggerEvaluation.mutate()} disabled={triggerEvaluation.isPending}>
            {triggerEvaluation.isPending ? 'Running evaluation…' : 'Run new evaluation'}
          </button>
          {evaluations[0] && (
            <button
              type="button"
              onClick={() => refreshSuggestions.mutate(evaluations[0].id)}
              disabled={refreshSuggestions.isPending}
            >
              {refreshSuggestions.isPending ? 'Refreshing suggestions…' : 'Refresh suggestions'}
            </button>
          )}
        </div>
      </header>

      {isLoading ? (
        <p>Loading evaluations…</p>
      ) : evaluations.length ? (
        evaluations.map((evaluation) => <EvaluationSummaryCard key={evaluation.id} evaluation={evaluation} />)
      ) : (
        <p>No evaluations yet.</p>
      )}
    </div>
  );
};

export default EvaluationsPage;
