import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getVisualizationRequests } from '../services/api';

const ResultsPage = () => {
  const [requests, setRequests] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRequests = async () => {
      try {
        setIsLoading(true);
        const data = await getVisualizationRequests();
        setRequests(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching visualization requests:', err);
        setError('Failed to load visualization requests. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchRequests();
  }, []);

  if (isLoading) {
    return (
      <div className="results-page loading">
        <h1>Results</h1>
        <div className="loading-indicator">
          <div className="spinner"></div>
          <p>Loading visualization requests...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="results-page error">
        <h1>Results</h1>
        <div className="error-message">{error}</div>
        <p>
          <Link to="/upload">Upload New Image</Link>
        </p>
      </div>
    );
  }

  return (
    <div className="results-page">
      <h1>Visualization Results</h1>

      <div className="results-actions">
        <Link to="/upload" className="upload-button">Upload New Image</Link>
      </div>

      {requests.length === 0 ? (
        <div className="no-results">
          <p>No visualization requests found.</p>
          <p>Upload an image to create your first visualization.</p>
        </div>
      ) : (
        <div className="results-list">
          {requests.map((request) => (
            <div key={request.id} className="result-item">
              <div className="result-thumbnail">
                {request.image && (
                  <img
                    src={request.image}
                    alt="Thumbnail"
                    className="thumbnail-image"
                  />
                )}
              </div>

              <div className="result-info">
                <h3>Request #{request.id}</h3>
                <p>
                  <strong>Status:</strong>
                  <span className={`status-${request.status}`}>
                    {request.status}
                  </span>
                </p>
                <p>
                  <strong>Screen Type:</strong> {request.screen_type_name || 'Unknown'}
                </p>
                <p>
                  <strong>Created:</strong> {new Date(request.created_at).toLocaleString()}
                </p>
              </div>

              <div className="result-actions">
                <Link to={`/results/${request.id}`} className="view-details-button">
                  View Details
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ResultsPage;
