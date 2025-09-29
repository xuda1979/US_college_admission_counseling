import {
  useAcknowledgeSuggestion,
  useArchiveSuggestion,
  useMilestones,
  useSuggestions
} from '../api/hooks';
import { RecommendationList } from '../components/RecommendationList';
import { Timeline } from '../components/Timeline';

const PlannerPage = () => {
  const { data: milestones = [], isLoading: milestonesLoading } = useMilestones();
  const { data: suggestions = [], isLoading: suggestionsLoading } = useSuggestions();
  const acknowledgeSuggestion = useAcknowledgeSuggestion();
  const archiveSuggestion = useArchiveSuggestion();

  return (
    <div className="grid">
      <section>
        <h2>Action Plan</h2>
        {suggestionsLoading ? (
          <p>Loading suggestions…</p>
        ) : (
          <RecommendationList
            suggestions={suggestions}
            onAcknowledge={(id) => acknowledgeSuggestion.mutate(id)}
            onArchive={(id) => archiveSuggestion.mutate(id)}
          />
        )}
      </section>

      <section>
        <h2>Timeline</h2>
        {milestonesLoading ? <p>Loading milestones…</p> : <Timeline milestones={milestones} />}
      </section>
    </div>
  );
};

export default PlannerPage;
