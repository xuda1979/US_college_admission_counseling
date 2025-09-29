import { Navigate, Route, Routes } from 'react-router-dom';

import DashboardPage from './pages/DashboardPage';
import EvaluationsPage from './pages/EvaluationsPage';
import EssaysPage from './pages/EssaysPage';
import PlannerPage from './pages/PlannerPage';
import { AppShell } from './components/AppShell';

const App = () => {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/evaluations" element={<EvaluationsPage />} />
        <Route path="/essays" element={<EssaysPage />} />
        <Route path="/planner" element={<PlannerPage />} />
      </Routes>
    </AppShell>
  );
};

export default App;
