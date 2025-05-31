# Backend Refactoring Guide

This document provides a comprehensive overview of the backend refactoring improvements made to the Homescreen Visualization App.

## Overview

The backend has been significantly refactored to improve:
- **Code Quality**: Better structure, readability, and maintainability
- **Performance**: Optimized database queries and API responses
- **Security**: Enhanced validation and permission handling
- **Scalability**: Better architecture for future growth
- **Developer Experience**: Comprehensive documentation and error handling

## Major Changes

### 1. Enhanced Django Models

#### Key Improvements:
- **Custom Validators**: Added image size and dimension validation
- **Custom Managers**: Implemented specialized query methods
- **Model Methods**: Added business logic methods and properties
- **Database Indexes**: Optimized query performance
- **File Upload Paths**: Organized file storage by user

#### New Features:
- **UserProfile Model**: Extended user information with company and phone
- **ScreenType Enhancements**: Added active status and sort ordering
- **Request Tracking**: Added processing timestamps and error messages
- **Image Metadata**: Automatic extraction of file size and dimensions

#### Example Usage:
```python
# Get active screen types
active_types = ScreenType.objects.active()

# Get recent requests for a user
recent_requests = VisualizationRequest.objects.for_user(user).recent(days=7)

# Mark request as processing
request.mark_as_processing(task_id="task_123")
```

### 2. Improved API Serializers

#### Key Improvements:
- **Comprehensive Validation**: Field-level and cross-field validation
- **Custom Methods**: SerializerMethodField for computed values
- **Nested Serialization**: Related object details in responses
- **Performance Optimization**: Separate serializers for list/detail views
- **Error Handling**: Detailed validation error messages

#### New Serializers:
- `UserProfileSerializer`: User profile management
- `VisualizationRequestCreateSerializer`: Simplified creation
- Enhanced validation for all existing serializers

#### Example Usage:
```python
# Validation automatically handles:
# - Image file type and size validation
# - Screen type availability checking
# - Phone number format validation
# - Unique name constraints
```

### 3. Advanced ViewSets

#### Key Improvements:
- **Custom Permissions**: Owner-only access with proper checks
- **Database Optimization**: select_related and prefetch_related
- **Filtering & Search**: Django-filter integration
- **Pagination**: Standardized pagination across endpoints
- **Caching**: Response caching for static data
- **Logging**: Comprehensive request/error logging

#### New Features:
- **Custom Actions**: `/stats`, `/retry`, `/active` endpoints
- **Permission Classes**: `IsOwnerOrReadOnly` for secure access
- **Error Handling**: Proper HTTP status codes and messages
- **Transaction Safety**: Atomic operations for data integrity

#### API Endpoints:

##### Screen Types
```
GET /api/screentypes/          # List all active screen types
GET /api/screentypes/active/   # Get only active types
GET /api/screentypes/{id}/     # Get specific screen type
```

##### Visualization Requests
```
GET /api/visualizations/           # List user's requests (paginated)
POST /api/visualizations/          # Create new request
GET /api/visualizations/{id}/      # Get request details
PUT /api/visualizations/{id}/      # Update request
DELETE /api/visualizations/{id}/   # Delete request
POST /api/visualizations/{id}/retry/  # Retry failed request
GET /api/visualizations/stats/     # Get user statistics
```

##### Generated Images
```
GET /api/generated-images/         # List user's generated images
GET /api/generated-images/{id}/    # Get specific image
```

##### User Profile
```
GET /api/profile/                  # Get user profile
PUT /api/profile/                  # Update user profile
```

### 4. Query Optimization

#### Database Indexes:
- User + created_at for request listings
- Status for filtering
- Screen type name for lookups
- Generated image timestamps

#### Query Optimization:
- `select_related()` for foreign keys
- `prefetch_related()` for reverse foreign keys
- Optimized querysets per action type

### 5. Enhanced Security

#### Validation:
- File type and size validation
- Image dimension checking
- Input sanitization
- Cross-field validation

#### Permissions:
- User-specific data access
- Owner-only modifications
- Proper permission inheritance

## Configuration Changes

### Requirements
Added new dependencies:
```
django-filter>=23.0  # For API filtering
```

### Settings
Updated `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... existing apps
    'django_filters',  # Added for filtering
    # ... rest of apps
]
```

### URL Configuration
Enhanced API routing:
```python
router.register(r'screentypes', views.ScreenTypeViewSet)
router.register(r'visualizations', views.VisualizationRequestViewSet)
router.register(r'generated-images', views.GeneratedImageViewSet)
router.register(r'profile', views.UserProfileViewSet)
```

## Migration Guide

### Database Migration
Run the following to apply model changes:
```bash
python manage.py makemigrations api
python manage.py migrate
```

### API Changes
The API is backward compatible, but new features are available:

#### New Query Parameters:
- `?page_size=20` - Control pagination
- `?status=pending` - Filter by status
- `?search=security` - Search screen types
- `?ordering=-created_at` - Custom ordering

#### New Response Fields:
- Processing duration in seconds
- File size in MB
- Image dimensions
- User profile information

## Performance Improvements

### Database Queries:
- Reduced N+1 queries with select_related
- Optimized list views with minimal data
- Added database indexes for common queries

### Caching:
- Screen types cached for 15 minutes
- Static data cached at view level

### Pagination:
- Default 20 items per page
- Configurable page size
- Maximum 100 items per page

## Error Handling

### Validation Errors:
- Detailed field-level error messages
- Cross-field validation feedback
- File upload error descriptions

### Permission Errors:
- Clear access denied messages
- Proper HTTP status codes
- Security-conscious error details

### Server Errors:
- Comprehensive logging
- User-friendly error messages
- Error tracking for debugging

## Testing Recommendations

### Unit Tests:
- Model validation and methods
- Serializer validation logic
- Custom manager methods

### Integration Tests:
- API endpoint functionality
- Permission enforcement
- Database query optimization

### Performance Tests:
- Query count verification
- Response time benchmarks
- Pagination efficiency

## Future Enhancements

### Planned Improvements:
1. **JWT Authentication**: Token-based auth with refresh
2. **Rate Limiting**: API request throttling
3. **Background Tasks**: Celery integration for AI processing
4. **File Storage**: Cloud storage integration
5. **Monitoring**: Health checks and metrics

### Extension Points:
- Custom permission classes
- Additional serializer fields
- New API endpoints
- Enhanced filtering options

## Troubleshooting

### Common Issues:

#### Migration Errors:
```bash
# If migration fails, try:
python manage.py migrate --fake-initial
```

#### Import Errors:
```bash
# Install missing dependencies:
pip install -r requirements.txt
```

#### Permission Errors:
- Check user authentication
- Verify object ownership
- Review permission classes

## Conclusion

The refactored backend provides a solid foundation for the Homescreen Visualization App with improved performance, security, and maintainability. The modular architecture supports future enhancements while maintaining backward compatibility.
