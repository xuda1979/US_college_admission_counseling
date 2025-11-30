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
import { PlayCircle, Award, Sparkles, TrendingUp } from 'lucide-react';

const DashboardPage = () => {
  const { data: evaluations = [], isLoading: evaluationsLoading } = useEvaluations();
  const { data: suggestions = [], isLoading: suggestionsLoading } = useSuggestions();
  const { data: milestones = [] } = useMilestones();
  const triggerEvaluation = useTriggerEvaluation();
  const acknowledgeSuggestion = useAcknowledgeSuggestion();
  const archiveSuggestion = useArchiveSuggestion();

  const latestEvaluation = evaluations[0];

  return (
    <div className="dashboard-grid">
      <section className="card welcome-card">
        <div className="welcome-content">
          <h2>Holistic Evaluation</h2>
          <p>
            Get instant insight into your profile across academics, extracurricular impact, essays, and overall fit. Use the AI
            counselor to guide your improvements.
          </p>
          <button
            type="button"
            onClick={() => triggerEvaluation.mutate()}
            disabled={triggerEvaluation.isPending}
            className="action-button"
          >
            <PlayCircle size={18} />
            {triggerEvaluation.isPending ? 'Running evaluation…' : 'Run fresh evaluation'}
          </button>
        </div>
        <div className="welcome-icon">
          <Sparkles size={64} strokeWidth={1} />
        </div>
      </section>

      <section className="dashboard-section">
        <div className="section-header">
          <TrendingUp size={24} />
          <h2>Latest Insights</h2>
        </div>
        {evaluationsLoading ? <p>Loading evaluations…</p> : latestEvaluation ? <EvaluationSummaryCard evaluation={latestEvaluation} /> : <p>No evaluations yet.</p>}
      </section>

      <div className="grid-split">
        <section className="dashboard-section">
          <div className="section-header">
            <Award size={24} />
            <h2>Top Recommendations</h2>
          </div>
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

        <section className="dashboard-section">
          <div className="section-header">
            <TrendingUp size={24} />
            <h2>Milestone Planner</h2>
          </div>
          <Timeline milestones={milestones} />
        </section>
      </div>

      <style>{`
        .dashboard-grid {
          display: flex;
          flex-direction: column;
          gap: 2rem;
        }

        .welcome-card {
          background: linear-gradient(135deg, #2563eb, #1e40af);
          color: white;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 2.5rem;
          overflow: hidden;
          position: relative;
        }

        .welcome-content {
          max-width: 600px;
          z-index: 1;
        }

        .welcome-content h2 {
          color: white;
          font-size: 1.75rem;
          margin-bottom: 1rem;
        }

        .welcome-content p {
          font-size: 1.1rem;
          opacity: 0.9;
          margin-bottom: 2rem;
          line-height: 1.6;
        }

        .welcome-icon {
          color: rgba(255, 255, 255, 0.2);
          transform: rotate(15deg) scale(1.5);
          margin-right: 2rem;
        }

        .action-button {
          background: white;
          color: #2563eb;
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.75rem 1.5rem;
          font-size: 1rem;
        }

        .action-button:hover {
          background: #f8fafc;
        }

        .section-header {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 1.5rem;
          color: #334155;
        }

        .section-header h2 {
          margin: 0;
          font-size: 1.25rem;
        }

        .grid-split {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
          gap: 2rem;
        }
      `}</style>
    </div>
  );
};

export default DashboardPage;
