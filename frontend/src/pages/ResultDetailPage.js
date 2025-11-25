import React, { useState, useEffect } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { getVisualizationRequestById } from '../services/api';
import ResultsDisplay from '../components/Results/ResultsDisplay';

const ResultDetailPage = () => {
  // Get the result ID from the URL parameters
  const { id } = useParams();
  const navigate = useNavigate();

  const [request, setRequest] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let pollInterval;

    const fetchRequestDetails = async () => {
      try {
        const data = await getVisualizationRequestById(id);
        setRequest(data);
        setError(null);

        // Stop polling if complete or failed
        if (data.status === 'complete' || data.status === 'failed') {
          setIsLoading(false);
          return true; // Stop polling
        }
      } catch (err) {
        console.error(`Error fetching visualization request #${id}:`, err);
        if (err.response?.status === 404) {
          setError(`Visualization request #${id} not found.`);
          return true; // Stop polling
        } else {
          // Don't set error on poll failure, just log it
          if (isLoading) {
            setError('Failed to load visualization request details. Please try again later.');
          }
        }
      } finally {
        setIsLoading(false);
      }
      return false; // Continue polling
    };

    // Initial fetch
    fetchRequestDetails();

    // Set up polling
    pollInterval = setInterval(async () => {
      const shouldStop = await fetchRequestDetails();
      if (shouldStop) {
        clearInterval(pollInterval);
      }
    }, 3000); // Poll every 3 seconds

    return () => clearInterval(pollInterval);
  }, [id]);

  if (isLoading && !request) {
    return (
      <div className="result-detail-page loading">
        <h1>Result Details</h1>
        <div className="loading-indicator">
          <div className="spinner"></div>
          <p>Loading visualization request details...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="result-detail-page error">
        <h1>Result Details</h1>
        <div className="error-message">{error}</div>
        <p>
          <Link to="/results">Back to Results</Link>
        </p>
      </div>
    );
  }

  // Get the first result image if available
  const resultImageUrl = request.results && request.results.length > 0
    ? request.results[0].generated_image_url
    : null;

  return (
    <div className="result-detail-page">
      <h1>Visualization Request #{id}</h1>

      <div className="request-details">
        <div className="detail-row">
          <span className="detail-label">Status:</span>
          <span className={`status-${request.status}`}>{request.status}</span>
        </div>

        <div className="detail-row">
          <span className="detail-label">Screen Type:</span>
          <span>{request.screen_type_details?.name || 'Unknown'}</span>
        </div>

        <div className="detail-row">
          <span className="detail-label">Created:</span>
          <span>{new Date(request.created_at).toLocaleString()}</span>
        </div>

        {request.processing_completed_at && (
          <div className="detail-row">
            <span className="detail-label">Completed:</span>
            <span>{new Date(request.processing_completed_at).toLocaleString()}</span>
          </div>
        )}
      </div>

      <ResultsDisplay
        originalImage={request.original_image_url}
        resultImage={resultImageUrl}
        status={request.status}
      />

      <div className="detail-actions">
        <Link to="/results" className="back-button">Back to Results</Link>
        <Link to="/upload" className="upload-button">Upload New Image</Link>
      </div>
    </div>
  );
};

export default ResultDetailPage;
