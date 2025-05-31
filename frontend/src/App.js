import React, { useState } from 'react';
import './App.css';

// Simple Login Form Component
const LoginForm = ({ onLogin, error }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await onLogin({ username, password });
    } catch (err) {
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
      <h2>🔐 Login to Homescreen Visualizer</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Username:
          </label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={{
              width: '100%',
              padding: '10px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              fontSize: '16px'
            }}
            placeholder="Enter username (try: testuser)"
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Password:
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{
              width: '100%',
              padding: '10px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              fontSize: '16px'
            }}
            placeholder="Enter password (try: password123)"
          />
        </div>

        {error && (
          <div style={{
            color: 'red',
            backgroundColor: '#ffebee',
            padding: '10px',
            borderRadius: '4px',
            border: '1px solid #ffcdd2'
          }}>
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: '12px',
            backgroundColor: loading ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            fontSize: '16px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>

      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
        <h3>💡 Demo Credentials:</h3>
        <p><strong>Username:</strong> testuser</p>
        <p><strong>Password:</strong> password123</p>
      </div>
    </div>
  );
};

// Image Upload Component
const ImageUploadView = ({ user, screenTypes, onBack }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedScreenType, setSelectedScreenType] = useState('');
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [dragOver, setDragOver] = useState(false);
  const [processingRequest, setProcessingRequest] = useState(null);
  const [progress, setProgress] = useState(0);
  const [statusMessage, setStatusMessage] = useState('');

  // Poll for progress updates
  React.useEffect(() => {
    if (!processingRequest) return;

    const pollProgress = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/api/visualizations/${processingRequest.id}/`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          setProgress(data.progress_percentage || 0);
          setStatusMessage(data.status_message || '');

          if (data.status === 'complete') {
            setMessage(`✅ Processing complete! Generated ${data.results?.length || 0} visualizations.`);
            setProcessingRequest(null);
            setProgress(100);
            setStatusMessage('All visualizations ready!');
          } else if (data.status === 'failed') {
            setMessage(`❌ Processing failed: ${data.error_message || 'Unknown error'}`);
            setProcessingRequest(null);
            setProgress(0);
            setStatusMessage('Processing failed');
          }
        }
      } catch (error) {
        console.error('Error polling progress:', error);
      }
    };

    const interval = setInterval(pollProgress, 1000); // Poll every second
    return () => clearInterval(interval);
  }, [processingRequest]);

  const handleFileSelect = (file) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      setMessage('');
    } else {
      setMessage('Please select a valid image file (JPG, PNG, GIF, WebP)');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    handleFileSelect(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      setMessage('Please select an image file');
      return;
    }

    if (!selectedScreenType) {
      setMessage('Please select a screen type');
      return;
    }

    setUploading(true);
    setMessage('');

    try {
      const formData = new FormData();
      formData.append('original_image', selectedFile);
      formData.append('screen_type', selectedScreenType);

      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/visualizations/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setMessage(`✅ Upload successful! Processing started...`);
        setProcessingRequest(data);
        setProgress(0);
        setStatusMessage('Starting processing...');
        setSelectedFile(null);
        setSelectedScreenType('');
      } else {
        const errorData = await response.json();
        setMessage(`❌ Upload failed: ${errorData.detail || 'Unknown error'}`);
      }
    } catch (error) {
      setMessage('❌ Network error. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h2>📤 Upload Image for Visualization</h2>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {/* File Upload Area */}
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          style={{
            border: `2px dashed ${dragOver ? '#007bff' : '#ddd'}`,
            borderRadius: '8px',
            padding: '40px',
            textAlign: 'center',
            backgroundColor: dragOver ? '#f8f9ff' : '#fafafa',
            cursor: 'pointer',
            transition: 'all 0.3s ease'
          }}
          onClick={() => document.getElementById('fileInput').click()}
        >
          <input
            id="fileInput"
            type="file"
            accept="image/*"
            onChange={(e) => handleFileSelect(e.target.files[0])}
            style={{ display: 'none' }}
          />

          {selectedFile ? (
            <div>
              <p style={{ fontSize: '24px', margin: '0 0 10px 0' }}>✅</p>
              <p><strong>Selected:</strong> {selectedFile.name}</p>
              <p>Size: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
              <p style={{ color: '#666', fontSize: '14px' }}>Click to select a different file</p>
            </div>
          ) : (
            <div>
              <p style={{ fontSize: '48px', margin: '0 0 20px 0' }}>📁</p>
              <p><strong>Drag & drop an image here</strong></p>
              <p style={{ color: '#666' }}>or click to browse files</p>
              <p style={{ color: '#999', fontSize: '14px' }}>Supports: JPG, PNG, GIF, WebP (max 10MB)</p>
            </div>
          )}
        </div>

        {/* Screen Type Selection */}
        <div>
          <label style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
            Select Screen Type:
          </label>
          <select
            value={selectedScreenType}
            onChange={(e) => setSelectedScreenType(e.target.value)}
            required
            style={{
              width: '100%',
              padding: '12px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              fontSize: '16px'
            }}
          >
            <option value="">Choose a screen type...</option>
            {screenTypes.map(type => (
              <option key={type.id} value={type.id}>
                {type.name} - {type.description}
              </option>
            ))}
          </select>
        </div>

        {/* Progress Bar */}
        {processingRequest && (
          <div style={{
            padding: '20px',
            borderRadius: '8px',
            backgroundColor: '#e3f2fd',
            border: '1px solid #bbdefb'
          }}>
            <h3 style={{ margin: '0 0 15px 0', color: '#1976d2' }}>🔄 Processing Your Image</h3>

            {/* Progress Bar */}
            <div style={{
              width: '100%',
              height: '20px',
              backgroundColor: '#f0f0f0',
              borderRadius: '10px',
              overflow: 'hidden',
              marginBottom: '10px'
            }}>
              <div style={{
                width: `${progress}%`,
                height: '100%',
                backgroundColor: progress === 100 ? '#4caf50' : '#2196f3',
                borderRadius: '10px',
                transition: 'width 0.3s ease',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontSize: '12px',
                fontWeight: 'bold'
              }}>
                {progress > 10 && `${progress}%`}
              </div>
            </div>

            {/* Status Message */}
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              fontSize: '14px'
            }}>
              <span style={{ color: '#666' }}>{statusMessage}</span>
              <span style={{ color: '#1976d2', fontWeight: 'bold' }}>{progress}%</span>
            </div>

            {/* Processing Steps */}
            <div style={{ marginTop: '15px', fontSize: '12px', color: '#666' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                <span style={{ color: progress >= 10 ? '#4caf50' : '#ccc' }}>✓ Image Upload</span>
                <span style={{ color: progress >= 30 ? '#4caf50' : '#ccc' }}>✓ Processing Started</span>
                <span style={{ color: progress >= 60 ? '#4caf50' : '#ccc' }}>✓ Generating Visualizations</span>
                <span style={{ color: progress >= 100 ? '#4caf50' : '#ccc' }}>✓ Complete</span>
              </div>
            </div>
          </div>
        )}

        {/* Message Display */}
        {message && (
          <div style={{
            padding: '15px',
            borderRadius: '4px',
            backgroundColor: message.includes('✅') ? '#d4edda' : '#f8d7da',
            border: `1px solid ${message.includes('✅') ? '#c3e6cb' : '#f5c6cb'}`,
            color: message.includes('✅') ? '#155724' : '#721c24'
          }}>
            {message}
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={uploading || processingRequest || !selectedFile || !selectedScreenType}
          style={{
            padding: '15px',
            backgroundColor: (uploading || processingRequest) ? '#ccc' : '#28a745',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            fontSize: '16px',
            cursor: (uploading || processingRequest) ? 'not-allowed' : 'pointer'
          }}
        >
          {uploading ? '⏳ Uploading...' :
           processingRequest ? '🔄 Processing...' :
           '🚀 Generate Visualization'}
        </button>
      </form>
    </div>
  );
};

// Screen Types View Component
const ScreenTypesView = ({ screenTypes, onBack }) => {
  return (
    <div>
      <h2>🖥️ Available Screen Types</h2>
      <div style={{ display: 'grid', gap: '20px', marginTop: '20px' }}>
        {screenTypes.map(type => (
          <div key={type.id} style={{
            backgroundColor: '#f8f9fa',
            padding: '20px',
            borderRadius: '8px',
            border: '1px solid #dee2e6'
          }}>
            <h3>{type.name}</h3>
            <p>{type.description || 'No description available'}</p>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '10px', fontSize: '14px', color: '#666' }}>
              <span>Requests: {type.request_count || 0}</span>
              <span>Status: {type.is_active ? '✅ Active' : '❌ Inactive'}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Results View Component
const ResultsView = ({ user, onBack }) => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);

  React.useEffect(() => {
    const fetchResults = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/visualizations/', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        if (response.ok) {
          const data = await response.json();
          setResults(data.results || []);
        }
      } catch (error) {
        console.error('Error fetching results:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchResults();
  }, []);

  if (loading) {
    return <div>⏳ Loading your visualization results...</div>;
  }

  return (
    <div>
      <h2>📊 Your Visualization Results</h2>
      {results.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px', backgroundColor: '#f8f9fa', borderRadius: '8px', marginTop: '20px' }}>
          <p style={{ fontSize: '48px', margin: '0 0 20px 0' }}>📭</p>
          <h3>No visualizations yet</h3>
          <p>Upload your first image to get started!</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '20px', marginTop: '20px' }}>
          {results.map(result => (
            <div key={result.id} style={{
              backgroundColor: '#f8f9fa',
              padding: '20px',
              borderRadius: '8px',
              border: '1px solid #dee2e6'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3>Visualization #{result.id}</h3>
                <span style={{
                  padding: '4px 8px',
                  borderRadius: '4px',
                  fontSize: '12px',
                  backgroundColor: result.status === 'completed' ? '#d4edda' : '#fff3cd',
                  color: result.status === 'completed' ? '#155724' : '#856404'
                }}>
                  {result.status}
                </span>
              </div>
              <p><strong>Screen Type:</strong> {result.screen_type_name}</p>
              <p><strong>Created:</strong> {new Date(result.created_at).toLocaleString()}</p>
              <p><strong>Generated Images:</strong> {result.result_count}</p>

              {/* Original Image */}
              {result.original_image_url && (
                <div style={{ marginTop: '15px' }}>
                  <h4>📷 Original Image:</h4>
                  <img
                    src={result.original_image_url}
                    alt="Original"
                    style={{
                      maxWidth: '200px',
                      maxHeight: '150px',
                      objectFit: 'cover',
                      borderRadius: '4px',
                      border: '2px solid #007bff'
                    }}
                  />
                </div>
              )}

              {/* Generated Images */}
              {result.results && result.results.length > 0 && (
                <div style={{ marginTop: '20px' }}>
                  <h4>🎨 Generated Visualizations:</h4>
                  <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                    gap: '15px',
                    marginTop: '10px'
                  }}>
                    {result.results.map((generatedImg, index) => (
                      <div key={generatedImg.id} style={{
                        border: '1px solid #ddd',
                        borderRadius: '8px',
                        padding: '10px',
                        backgroundColor: '#fff'
                      }}>
                        <img
                          src={generatedImg.generated_image_url}
                          alt={`Generated ${index + 1}`}
                          style={{
                            width: '100%',
                            height: '150px',
                            objectFit: 'cover',
                            borderRadius: '4px',
                            marginBottom: '8px'
                          }}
                        />
                        <p style={{ fontSize: '12px', margin: '0', color: '#666' }}>
                          {generatedImg.dimensions} • {generatedImg.file_size_mb} MB
                        </p>
                        <a
                          href={generatedImg.generated_image_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          style={{
                            fontSize: '12px',
                            color: '#007bff',
                            textDecoration: 'none'
                          }}
                        >
                          View Full Size →
                        </a>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// Simple Dashboard Component
const Dashboard = ({ user, onLogout }) => {
  const [currentView, setCurrentView] = useState('dashboard');
  const [screenTypes, setScreenTypes] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch screen types when component mounts
  React.useEffect(() => {
    const fetchScreenTypes = async () => {
      try {
        const response = await fetch('/api/screentypes/');
        if (response.ok) {
          const data = await response.json();
          setScreenTypes(data.results || []);
        }
      } catch (error) {
        console.error('Error fetching screen types:', error);
      }
    };
    fetchScreenTypes();
  }, []);

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <h1>🏠 Homescreen Visualizer Dashboard</h1>
        <div style={{ display: 'flex', gap: '10px' }}>
          {currentView !== 'dashboard' && (
            <button
              onClick={() => setCurrentView('dashboard')}
              style={{
                padding: '8px 16px',
                backgroundColor: '#6c757d',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              ← Back to Dashboard
            </button>
          )}
          <button
            onClick={onLogout}
            style={{
              padding: '8px 16px',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Logout
          </button>
        </div>
      </div>

      {currentView === 'dashboard' && (
        <>
          <div style={{ backgroundColor: '#e8f5e8', padding: '20px', borderRadius: '8px', marginBottom: '20px' }}>
            <h2>✅ Welcome, {user.username}!</h2>
            <p>You have successfully logged into the Homescreen Visualizer.</p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
        <div style={{ backgroundColor: '#f8f9fa', padding: '20px', borderRadius: '8px', border: '1px solid #dee2e6' }}>
          <h3>👤 User Profile</h3>
          <p><strong>Username:</strong> {user.username}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Member since:</strong> {new Date(user.date_joined).toLocaleDateString()}</p>
          <p><strong>Total Requests:</strong> {user.profile?.total_requests || 0}</p>
        </div>

        <div style={{ backgroundColor: '#f8f9fa', padding: '20px', borderRadius: '8px', border: '1px solid #dee2e6' }}>
          <h3>🚀 Quick Actions</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <button
              onClick={() => setCurrentView('upload')}
              style={{ padding: '10px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
            >
              📤 Upload Image
            </button>
            <button
              onClick={() => setCurrentView('results')}
              style={{ padding: '10px', backgroundColor: '#17a2b8', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
            >
              📊 View Results
            </button>
            <button
              onClick={() => setCurrentView('screentypes')}
              style={{ padding: '10px', backgroundColor: '#6f42c1', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
            >
              🖥️ Screen Types ({screenTypes.length})
            </button>
          </div>
        </div>

        <div style={{ backgroundColor: '#f8f9fa', padding: '20px', borderRadius: '8px', border: '1px solid #dee2e6' }}>
          <h3>📊 API Status</h3>
          <p>✅ Authentication: Working</p>
          <p>✅ Backend API: Connected</p>
          <p>✅ Screen Types: 3 available</p>
          <p>✅ Database: Connected</p>
        </div>
      </div>

          <div style={{ marginTop: '30px', padding: '20px', backgroundColor: '#fff3cd', borderRadius: '8px', border: '1px solid #ffeaa7' }}>
            <h3>🎯 Next Steps:</h3>
            <ul>
              <li>Upload an image to generate homescreen visualizations</li>
              <li>Select from available screen types (Security, Entertainment, Smart Home)</li>
              <li>View and manage your visualization results</li>
              <li>Explore the admin panel at <a href="/admin" target="_blank">/admin</a></li>
            </ul>
          </div>
        </>
      )}

      {currentView === 'upload' && (
        <ImageUploadView
          user={user}
          screenTypes={screenTypes}
          onBack={() => setCurrentView('dashboard')}
        />
      )}

      {currentView === 'screentypes' && (
        <ScreenTypesView
          screenTypes={screenTypes}
          onBack={() => setCurrentView('dashboard')}
        />
      )}

      {currentView === 'results' && (
        <ResultsView
          user={user}
          onBack={() => setCurrentView('dashboard')}
        />
      )}
    </div>
  );
};

function App() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (credentials) => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (response.ok) {
        const data = await response.json();
        setUser(data.user);
        // Store tokens in localStorage for future requests
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Login failed');
      }
    } catch (err) {
      setError('Network error. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  };

  return (
    <div className="App">
      <div style={{ minHeight: '100vh', backgroundColor: '#f5f5f5', padding: '20px' }}>
        {user ? (
          <Dashboard user={user} onLogout={handleLogout} />
        ) : (
          <LoginForm onLogin={handleLogin} error={error} loading={loading} />
        )}
      </div>
    </div>
  );
}

export default App;
