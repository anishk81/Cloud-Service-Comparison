import React, { useState, useEffect } from 'react';
import { AWSService, ServiceCategory } from './types';
import { apiService, GetServicesParams } from './services/api';
import { ServiceCard } from './components/ServiceCard';
import { ComparisonTable } from './components/ComparisonTable';
import './App.css';

function App() {
  const [services, setServices] = useState<AWSService[]>([]);
  const [selectedServices, setSelectedServices] = useState<AWSService[]>([]);
  const [categories, setCategories] = useState<ServiceCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<GetServicesParams>({});
  const [selectedServiceDetails, setSelectedServiceDetails] = useState<AWSService | null>(null);
  const [showComparison, setShowComparison] = useState(false);
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode');
    return saved ? JSON.parse(saved) : false;
  });

  useEffect(() => {
    loadServices();
  }, [filters]);

  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const loadServices = async () => {
    try {
      setLoading(true);
      const response = await apiService.getServices(filters);
      setServices(response.services);
      setCategories(response.categories);
      setError(null);
    } catch (err) {
      setError('Failed to load services. Please make sure the backend is running.');
      console.error('Error loading services:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleServiceSelect = (serviceId: string) => {
    const service = services.find(s => s.id === serviceId);
    if (!service) return;

    const isSelected = selectedServices.some(s => s.id === serviceId);
    if (isSelected) {
      setSelectedServices(prev => prev.filter(s => s.id !== serviceId));
    } else {
      if (selectedServices.length >= 5) {
        alert('You can compare up to 5 services at a time.');
        return;
      }
      setSelectedServices(prev => [...prev, service]);
    }
  };

  const handleRemoveFromComparison = (serviceId: string) => {
    setSelectedServices(prev => prev.filter(s => s.id !== serviceId));
  };

  const handleViewDetails = (service: AWSService) => {
    setSelectedServiceDetails(service);
  };

  const handleCloseDetails = () => {
    setSelectedServiceDetails(null);
  };

  const handleFilterChange = (newFilters: Partial<GetServicesParams>) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const clearFilters = () => {
    setFilters({});
  };

  const clearComparison = () => {
    setSelectedServices([]);
  };

  if (loading) {
    return (
      <div className="app-loading">
        <h2>Loading AWS services...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-error">
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={loadServices} className="retry-btn">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className={`App ${darkMode ? 'dark-mode' : ''}`}>
      <header className="app-header">
        <div className="header-content">
          <div className="header-text">
            <h1>AWS Service Comparison</h1>
            <p>Compare AWS services to find the best fit for your needs</p>
          </div>
          <button 
            className="theme-toggle" 
            onClick={toggleDarkMode}
            aria-label={`Switch to ${darkMode ? 'light' : 'dark'} mode`}
          >
            {darkMode ? (
              <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd" />
              </svg>
            ) : (
              <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
              </svg>
            )}
          </button>
        </div>
      </header>

      <main className="app-main">
        {/* Filters Section */}
        <section className="filters-section">
          <div className="filters-container">
            <div className="filter-group">
              <label htmlFor="search">Search services:</label>
              <input
                id="search"
                type="text"
                placeholder="Search by name or description..."
                value={filters.search || ''}
                onChange={(e) => handleFilterChange({ search: e.target.value || undefined })}
                className="search-input"
              />
            </div>

            <div className="filter-group">
              <label htmlFor="category">Category:</label>
              <select
                id="category"
                value={filters.category || ''}
                onChange={(e) => handleFilterChange({ category: e.target.value || undefined })}
                className="category-select"
              >
                <option value="">All Categories</option>
                {categories.map(category => (
                  <option key={category} value={category}>{category}</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="free-tier">Free Tier:</label>
              <select
                id="free-tier"
                value={filters.free_tier === undefined ? '' : filters.free_tier.toString()}
                onChange={(e) => {
                  const value = e.target.value;
                  handleFilterChange({ 
                    free_tier: value === '' ? undefined : value === 'true'
                  });
                }}
                className="free-tier-select"
              >
                <option value="">All Services</option>
                <option value="true">Free Tier Available</option>
                <option value="false">No Free Tier</option>
              </select>
            </div>

            <button onClick={clearFilters} className="clear-filters-btn">
              Clear Filters
            </button>
          </div>

          <div className="results-summary">
            <p>Showing {services.length} services</p>
            {selectedServices.length > 0 && (
              <div className="comparison-controls">
                <span>{selectedServices.length} services selected</span>
                <button 
                  onClick={() => setShowComparison(!showComparison)}
                  className="toggle-comparison-btn"
                >
                  {showComparison ? 'Hide' : 'Show'} Comparison
                </button>
                <button onClick={clearComparison} className="clear-comparison-btn">
                  Clear Selection
                </button>
              </div>
            )}
          </div>
        </section>

        {/* Comparison Section */}
        {showComparison && selectedServices.length > 0 && (
          <section className="comparison-section">
            <ComparisonTable 
              services={selectedServices}
              onRemoveService={handleRemoveFromComparison}
            />
          </section>
        )}

        {/* Services Grid */}
        <section className="services-section">
          <div className="services-grid">
            {services.map(service => (
              <ServiceCard
                key={service.id}
                service={service}
                isSelected={selectedServices.some(s => s.id === service.id)}
                onToggleSelect={handleServiceSelect}
                onViewDetails={handleViewDetails}
              />
            ))}
          </div>
        </section>
      </main>

      {/* Service Details Modal */}
      {selectedServiceDetails && (
        <div className="modal-overlay" onClick={handleCloseDetails}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{selectedServiceDetails.name}</h2>
              <button onClick={handleCloseDetails} className="close-btn">×</button>
            </div>
            <div className="modal-body">
              <div className="service-detail-section">
                <h3>Description</h3>
                <p>{selectedServiceDetails.description}</p>
              </div>
              
              <div className="service-detail-section">
                <h3>Key Features</h3>
                <ul>
                  {selectedServiceDetails.key_features.map((feature, index) => (
                    <li key={index}>{feature}</li>
                  ))}
                </ul>
              </div>
              
              <div className="service-detail-section">
                <h3>Use Cases</h3>
                <ul>
                  {selectedServiceDetails.use_cases.map((useCase, index) => (
                    <li key={index}>{useCase}</li>
                  ))}
                </ul>
              </div>
              
              <div className="service-detail-section">
                <h3>Pricing Information</h3>
                <p>{selectedServiceDetails.pricing_notes}</p>
                <div className="pricing-models">
                  {selectedServiceDetails.pricing_models.map((model, index) => (
                    <span key={index} className="pricing-model-tag">{model}</span>
                  ))}
                </div>
              </div>
              
              {selectedServiceDetails.limitations.length > 0 && (
                <div className="service-detail-section">
                  <h3>Limitations</h3>
                  <ul>
                    {selectedServiceDetails.limitations.map((limitation, index) => (
                      <li key={index}>{limitation}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              <div className="service-detail-section">
                <h3>Additional Information</h3>
                <p><strong>Category:</strong> {selectedServiceDetails.category}</p>
                <p><strong>Free Tier:</strong> {selectedServiceDetails.free_tier_available ? 'Available' : 'Not Available'}</p>
                <p><strong>Region Availability:</strong> {selectedServiceDetails.region_availability}</p>
                {selectedServiceDetails.documentation_url && (
                  <p>
                    <a 
                      href={selectedServiceDetails.documentation_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="docs-link"
                    >
                      View Official Documentation
                    </a>
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
