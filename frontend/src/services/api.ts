import axios from 'axios';
import { AWSService, ServicesResponse, ComparisonResponse, ServiceCategory } from '../types';

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '' // Use relative URLs in production (same domain)
  : 'http://localhost:8000'; // Use localhost in development

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface GetServicesParams {
  category?: string;
  free_tier?: boolean;
  search?: string;
}

export const apiService = {
  // Get all services with optional filtering
  getServices: async (params?: GetServicesParams): Promise<ServicesResponse> => {
    const response = await api.get('/api/services', { params });
    return response.data;
  },

  // Get a specific service by ID
  getService: async (serviceId: string): Promise<AWSService> => {
    const response = await api.get(`/api/services/${serviceId}`);
    return response.data;
  },

  // Get all categories
  getCategories: async (): Promise<{ categories: ServiceCategory[] }> => {
    const response = await api.get('/api/categories');
    return response.data;
  },

  // Get services by category
  getServicesByCategory: async (category: string): Promise<AWSService[]> => {
    const response = await api.get(`/api/services/category/${category}`);
    return response.data;
  },

  // Compare services
  compareServices: async (serviceIds: string[]): Promise<ComparisonResponse> => {
    const response = await api.get('/api/compare', {
      params: { service_ids: serviceIds.join(',') }
    });
    return response.data;
  },

  // Health check
  healthCheck: async (): Promise<{ status: string; services_count: number }> => {
    const response = await api.get('/health');
    return response.data;
  },
};
