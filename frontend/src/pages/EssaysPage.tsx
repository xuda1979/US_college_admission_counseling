import { useState } from 'react';

import { useCritiqueEssay, useEssays } from '../api/hooks';
import { EssayFeedbackPanel } from '../components/EssayFeedbackPanel';

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
      <header className="card">
        <h2>Essay Studio</h2>
        <p>
          Upload drafts and request targeted critiques focused on structure, voice, and alignment with each school prompt.
        </p>
      </header>

      {isLoading ? <p>Loading essays…</p> : <EssayFeedbackPanel essays={essays} onCritique={handleCritique} loadingId={activeEssay} />}
    </div>
  );
};

export default EssaysPage;
