import {
  useAcknowledgeSuggestion,
  useEvaluations,
  useMilestones,
  useSuggestions,
  useTriggerEvaluation,
  useArchiveSuggestion
} from '../api/hooks';
import { EvaluationSummaryCard } from '../components/EvaluationSummaryCard';
import { RecommendationList } from '../components/RecommendationList';
import { Timeline } from '../components/Timeline';

const DashboardPage = () => {
  const { data: evaluations = [], isLoading: evaluationsLoading } = useEvaluations();
  const { data: suggestions = [], isLoading: suggestionsLoading } = useSuggestions();
  const { data: milestones = [] } = useMilestones();
  const triggerEvaluation = useTriggerEvaluation();
  const acknowledgeSuggestion = useAcknowledgeSuggestion();
  const archiveSuggestion = useArchiveSuggestion();

  const latestEvaluation = evaluations[0];

  return (
    <div className="grid">
      <section className="card">
        <h2>Holistic Evaluation</h2>
        <p>
          Get instant insight into your profile across academics, extracurricular impact, essays, and overall fit. Use the AI
          counselor to guide your improvements.
        </p>
        <button type="button" onClick={() => triggerEvaluation.mutate()} disabled={triggerEvaluation.isPending}>
          {triggerEvaluation.isPending ? 'Running evaluation…' : 'Run fresh evaluation'}
        </button>
      </section>

      <section>
        <h2>Latest Insights</h2>
        {evaluationsLoading ? <p>Loading evaluations…</p> : latestEvaluation ? <EvaluationSummaryCard evaluation={latestEvaluation} /> : <p>No evaluations yet.</p>}
      </section>

      <section>
        <h2>Top Recommendations</h2>
        {suggestionsLoading ? (
          <p>Loading recommendations…</p>
        ) : (
          <RecommendationList
            suggestions={suggestions.slice(0, 4)}
            onAcknowledge={(id) => acknowledgeSuggestion.mutate(id)}
            onArchive={(id) => archiveSuggestion.mutate(id)}
          />
        )}
      </section>

      <section>
        <h2>Milestone Planner</h2>
        <Timeline milestones={milestones} />
      </section>
    </div>
  );
};

export default DashboardPage;
