import { Milestone } from '../types';
import './Timeline.css';

export const Timeline = ({ milestones }: { milestones: Milestone[] }) => {
  if (!milestones.length) {
    return <p>No milestones yet. Recommendations will add tasks here automatically.</p>;
  }

  return (
    <ol className="timeline">
      {milestones.map((milestone) => (
        <li key={milestone.id} className="timeline__item">
          <div className="timeline__date">
            {milestone.due_date ? new Date(milestone.due_date).toLocaleDateString() : 'TBD'}
          </div>
          <div>
            <h3>{milestone.title}</h3>
            {milestone.description && <p>{milestone.description}</p>}
          </div>
        </li>
      ))}
    </ol>
  );
};
