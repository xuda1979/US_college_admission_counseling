import {
  useAcknowledgeSuggestion,
  useArchiveSuggestion,
  useMilestones,
  useSuggestions
} from '../api/hooks';
import { RecommendationList } from '../components/RecommendationList';
import { Timeline } from '../components/Timeline';
import { Search, MapPin, ExternalLink } from 'lucide-react';
import { useState } from 'react';

const PlannerPage = () => {
  const { data: milestones = [], isLoading: milestonesLoading } = useMilestones();
  const { data: suggestions = [], isLoading: suggestionsLoading } = useSuggestions();
  const acknowledgeSuggestion = useAcknowledgeSuggestion();
  const archiveSuggestion = useArchiveSuggestion();
  const [searchTerm, setSearchTerm] = useState('');

  const universities = [
    { name: 'Stanford University', location: 'Stanford, CA', rank: '#3', url: 'https://stanford.edu' },
    { name: 'Massachusetts Institute of Technology', location: 'Cambridge, MA', rank: '#1', url: 'https://mit.edu' },
    { name: 'Harvard University', location: 'Cambridge, MA', rank: '#2', url: 'https://harvard.edu' },
    { name: 'Princeton University', location: 'Princeton, NJ', rank: '#1', url: 'https://princeton.edu' },
    { name: 'Yale University', location: 'New Haven, CT', rank: '#5', url: 'https://yale.edu' },
  ];

  const filteredUniversities = universities.filter(uni =>
    uni.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="grid">
      <section className="card" style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h2>University Search</h2>
          <div className="search-bar">
            <Search size={20} />
            <input
              type="text"
              placeholder="Search universities..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        <div className="university-grid">
          {filteredUniversities.map((uni) => (
            <div key={uni.name} className="university-card">
              <h3>{uni.name}</h3>
              <div className="university-meta">
                <span className="location"><MapPin size={14} /> {uni.location}</span>
                <span className="rank">{uni.rank} National Universities</span>
              </div>
              <a href={uni.url} target="_blank" rel="noopener noreferrer" className="visit-link">
                Visit Website <ExternalLink size={14} />
              </a>
            </div>
          ))}
        </div>
      </section>

      <div className="grid-split">
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

      <style>{`
        .search-bar {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          background: #f1f5f9;
          padding: 0.5rem 1rem;
          border-radius: 0.5rem;
          width: 300px;
        }

        .search-bar input {
          border: none;
          background: transparent;
          outline: none;
          width: 100%;
          font-size: 0.95rem;
        }

        .university-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
          gap: 1.5rem;
        }

        .university-card {
          border: 1px solid #e2e8f0;
          border-radius: 0.75rem;
          padding: 1.25rem;
          transition: transform 0.2s, box-shadow 0.2s;
        }

        .university-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .university-card h3 {
          margin: 0 0 0.5rem 0;
          font-size: 1.1rem;
        }

        .university-meta {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
          margin-bottom: 1rem;
          color: #64748b;
          font-size: 0.875rem;
        }

        .university-meta .location {
          display: flex;
          align-items: center;
          gap: 0.25rem;
        }

        .visit-link {
          display: inline-flex;
          align-items: center;
          gap: 0.25rem;
          color: #2563eb;
          text-decoration: none;
          font-size: 0.875rem;
          font-weight: 500;
        }

        .visit-link:hover {
          text-decoration: underline;
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

export default PlannerPage;
