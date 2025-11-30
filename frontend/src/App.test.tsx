import { render } from '@testing-library/react';
import { describe, it } from 'vitest';
import App from './App';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

describe('App', () => {
  it('renders without crashing', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </QueryClientProvider>
    );
    // Since App might redirect or show loading, we just check if it renders.
    // Ideally we should check for specific elements, but for a smoke test this is okay.
  });
});
