import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import client from './client';
import { Essay, Evaluation, Milestone, Suggestion } from '../types';

export const useEvaluations = () =>
  useQuery<Evaluation[]>({
    queryKey: ['evaluations'],
    queryFn: async () => {
      const { data } = await client.get<Evaluation[]>('/evaluations');
      return data;
    }
  });

export const useTriggerEvaluation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      const { data } = await client.post<Evaluation>('/evaluations/trigger');
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['evaluations'] });
      queryClient.invalidateQueries({ queryKey: ['suggestions'] });
      queryClient.invalidateQueries({ queryKey: ['milestones'] });
    }
  });
};

export const useSuggestions = () =>
  useQuery<Suggestion[]>({
    queryKey: ['suggestions'],
    queryFn: async () => {
      const { data } = await client.get<Suggestion[]>('/suggestions');
      return data;
    }
  });

export const useRefreshSuggestions = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (evaluationId: number) => {
      const { data } = await client.post<Suggestion[]>(`/suggestions/refresh/${evaluationId}`);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['suggestions'] });
      queryClient.invalidateQueries({ queryKey: ['milestones'] });
    }
  });
};

export const useAcknowledgeSuggestion = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (suggestionId: number) => {
      const { data } = await client.post<Suggestion>(`/suggestions/${suggestionId}/acknowledge`);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['suggestions'] });
    }
  });
};

export const useArchiveSuggestion = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (suggestionId: number) => {
      const { data } = await client.post<Suggestion>(`/suggestions/${suggestionId}/archive`);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['suggestions'] });
      queryClient.invalidateQueries({ queryKey: ['milestones'] });
    }
  });
};

export const useMilestones = () =>
  useQuery<Milestone[]>({
    queryKey: ['milestones'],
    queryFn: async () => {
      const { data } = await client.get<Milestone[]>('/milestones');
      return data;
    }
  });

export const useEssays = () =>
  useQuery<Essay[]>({
    queryKey: ['essays'],
    queryFn: async () => {
      const { data } = await client.get<Essay[]>('/essays');
      return data;
    }
  });

export const useCritiqueEssay = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (essayId: number) => {
      const { data } = await client.post(`/essays/${essayId}/critique`);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['evaluations'] });
    }
  });
};
