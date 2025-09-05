import React from 'react';
import { AWSService } from '../types';
import './ComparisonTable.css';

interface ComparisonTableProps {
  services: AWSService[];
  onRemoveService?: (serviceId: string) => void;
}

export const ComparisonTable: React.FC<ComparisonTableProps> = ({
  services,
  onRemoveService,
}) => {
  if (services.length === 0) {
    return (
      <div className="comparison-empty">
        <h3>No services selected for comparison</h3>
        <p>Select services from the list above to compare them side by side.</p>
      </div>
    );
  }

  const renderArrayField = (items: string[]) => (
    <ul className="comparison-list">
      {items.map((item, index) => (
        <li key={index}>{item}</li>
      ))}
    </ul>
  );

  return (
    <div className="comparison-container">
      <div className="comparison-header">
        <h2>Service Comparison ({services.length} services)</h2>
        <p>Compare AWS services side by side</p>
      </div>

      <div className="comparison-table-wrapper">
        <table className="comparison-table">
          <thead>
            <tr>
              <th className="criteria-column">Criteria</th>
              {services.map((service) => (
                <th key={service.id} className="service-column">
                  <div className="service-header">
                    <h4>{service.name}</h4>
                    {onRemoveService && (
                      <button
                        className="remove-service-btn"
                        onClick={() => onRemoveService(service.id)}
                        title="Remove from comparison"
                      >
                        ×
                      </button>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="criteria-cell"><strong>Category</strong></td>
              {services.map((service) => (
                <td key={`${service.id}-category`} className="value-cell">
                  <span className="category-badge">{service.category}</span>
                </td>
              ))}
            </tr>
            
            <tr>
              <td className="criteria-cell"><strong>Description</strong></td>
              {services.map((service) => (
                <td key={`${service.id}-description`} className="value-cell">
                  {service.description}
                </td>
              ))}
            </tr>

            <tr>
              <td className="criteria-cell"><strong>Key Features</strong></td>
              {services.map((service) => (
                <td key={`${service.id}-features`} className="value-cell">
                  {renderArrayField(service.key_features)}
                </td>
              ))}
            </tr>

            <tr>
              <td className="criteria-cell"><strong>Pricing Models</strong></td>
              {services.map((service) => (
                <td key={`${service.id}-pricing-models`} className="value-cell">
                  <div className="pricing-models">
                    {service.pricing_models.map((model, index) => (
                      <span key={index} className="pricing-model-badge">
                        {model}
                      </span>
                    ))}
                  </div>
                </td>
              ))}
            </tr>

            <tr>
              <td className="criteria-cell"><strong>Pricing Notes</strong></td>
              {services.map((service) => (
                <td key={`${service.id}-pricing-notes`} className="value-cell">
                  <div className="pricing-notes">{service.pricing_notes}</div>
                </td>
              ))}
            </tr>

            <tr>
              <td className="criteria-cell"><strong>Use Cases</strong></td>
              {services.map((service) => (
                <td key={`${service.id}-use-cases`} className="value-cell">
                  {renderArrayField(service.use_cases)}
                </td>
              ))}
            </tr>

            <tr>
              <td className="criteria-cell"><strong>Limitations</strong></td>
              {services.map((service) => (
                <td key={`${service.id}-limitations`} className="value-cell">
                  {service.limitations.length > 0 ? (
                    renderArrayField(service.limitations)
                  ) : (
                    <span className="no-data">No major limitations listed</span>
                  )}
                </td>
              ))}
            </tr>

            <tr>
              <td className="criteria-cell"><strong>Free Tier</strong></td>
              {services.map((service) => (
                <td key={`${service.id}-free-tier`} className="value-cell">
                  <span className={`free-tier-status ${service.free_tier_available ? 'available' : 'not-available'}`}>
                    {service.free_tier_available ? '✓ Available' : '✗ Not Available'}
                  </span>
                </td>
              ))}
            </tr>

            <tr>
              <td className="criteria-cell"><strong>Region Availability</strong></td>
              {services.map((service) => (
                <td key={`${service.id}-regions`} className="value-cell">
                  {service.region_availability}
                </td>
              ))}
            </tr>

            <tr>
              <td className="criteria-cell"><strong>Documentation</strong></td>
              {services.map((service) => (
                <td key={`${service.id}-docs`} className="value-cell">
                  {service.documentation_url ? (
                    <a
                      href={service.documentation_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="docs-link"
                    >
                      View Documentation
                    </a>
                  ) : (
                    <span className="no-data">No documentation link</span>
                  )}
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
