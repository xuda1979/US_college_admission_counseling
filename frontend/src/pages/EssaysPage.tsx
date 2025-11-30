import { useState } from 'react';

import { useCritiqueEssay, useEssays } from '../api/hooks';
import { EssayFeedbackPanel } from '../components/EssayFeedbackPanel';
import { PenTool, UploadCloud } from 'lucide-react';

const EssaysPage = () => {
  const { data: essays = [], isLoading } = useEssays();
  const critiqueEssay = useCritiqueEssay();
  const [activeEssay, setActiveEssay] = useState<number | null>(null);

  const handleCritique = (essayId: number) => {
    setActiveEssay(essayId);
    critiqueEssay.mutate(essayId, {
      onSettled: () => setActiveEssay(null)
    });
  };

  return (
    <div className="grid">
      <header className="card essay-header-card">
        <div className="essay-header-content">
          <h2>Essay Studio</h2>
          <p>
            Upload drafts and request targeted critiques focused on structure, voice, and alignment with each school prompt.
          </p>
          <button className="upload-button">
            <UploadCloud size={16} />
            Upload New Draft
          </button>
        </div>
        <div className="essay-header-icon">
          <PenTool size={64} strokeWidth={1} />
        </div>
      </header>

      {isLoading ? <p>Loading essays…</p> : <EssayFeedbackPanel essays={essays} onCritique={handleCritique} loadingId={activeEssay} />}

      <style>{`
        .essay-header-card {
          background: linear-gradient(135deg, #10b981, #059669);
          color: white;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 2.5rem;
          overflow: hidden;
          position: relative;
        }

        .essay-header-content {
          max-width: 600px;
          z-index: 1;
        }

        .essay-header-content h2 {
          color: white;
          font-size: 1.75rem;
          margin-bottom: 1rem;
        }

        .essay-header-content p {
          font-size: 1.1rem;
          opacity: 0.9;
          margin-bottom: 2rem;
          line-height: 1.6;
        }

        .essay-header-icon {
          color: rgba(255, 255, 255, 0.2);
          transform: rotate(-15deg) scale(1.5);
          margin-right: 2rem;
        }

        .upload-button {
          background: white;
          color: #059669;
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.75rem 1.5rem;
          font-size: 1rem;
          border-radius: 0.5rem;
          font-weight: 600;
          cursor: pointer;
          border: none;
        }

        .upload-button:hover {
          background: #f0fdf4;
        }
      `}</style>
    </div>
  );
};

export default EssaysPage;
