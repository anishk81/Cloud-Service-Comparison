import React from 'react';
import { AWSService } from '../types';
import './ServiceCard.css';

interface ServiceCardProps {
  service: AWSService;
  isSelected?: boolean;
  onToggleSelect?: (serviceId: string) => void;
  onViewDetails?: (service: AWSService) => void;
}

export const ServiceCard: React.FC<ServiceCardProps> = ({
  service,
  isSelected = false,
  onToggleSelect,
  onViewDetails,
}) => {
  const handleSelectToggle = () => {
    if (onToggleSelect) {
      onToggleSelect(service.id);
    }
  };

  const handleViewDetails = () => {
    if (onViewDetails) {
      onViewDetails(service);
    }
  };

  return (
    <div className={`service-card ${isSelected ? 'selected' : ''}`}>
      <div className="service-card-header">
        <h3 className="service-name">{service.name}</h3>
        <div className="service-badges">
          {service.free_tier_available && (
            <span className="badge free-tier">Free Tier</span>
          )}
          <span className="badge category">{service.category}</span>
        </div>
      </div>
      
      <p className="service-description">{service.description}</p>
      
      <div className="key-features">
        <h4>Key Features:</h4>
        <ul>
          {service.key_features.slice(0, 3).map((feature, index) => (
            <li key={index}>{feature}</li>
          ))}
          {service.key_features.length > 3 && (
            <li className="more-features">
              +{service.key_features.length - 3} more...
            </li>
          )}
        </ul>
      </div>

      <div className="pricing-summary">
        <strong>Pricing:</strong>
        <p className="pricing-note">
          {service.pricing_notes.length > 100
            ? `${service.pricing_notes.substring(0, 100)}...`
            : service.pricing_notes
          }
        </p>
      </div>

      <div className="service-actions">
        {onToggleSelect && (
          <button 
            className={`btn ${isSelected ? 'btn-selected' : 'btn-select'}`}
            onClick={handleSelectToggle}
          >
            {isSelected ? 'Selected ✓' : 'Select for Comparison'}
          </button>
        )}
        <button className="btn btn-details" onClick={handleViewDetails}>
          View Details
        </button>
        {service.documentation_url && (
          <a
            href={service.documentation_url}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-docs"
          >
            Documentation
          </a>
        )}
      </div>
    </div>
  );
};
