# Conversation Export - November 24, 2025

## Session Overview
**Date:** November 24, 2025  
**Duration:** ~2 hours  
**Focus:** Implementing and debugging Gemini AI "Screen King" pipeline for homescreen visualization

---

## Work Completed

### Phase 1: Initial AI Pipeline Implementation
- Implemented `ScreenVisualizer` class with 4-step "Screen King" pipeline:
  1. **The Cleanse**: Remove clutter, fix lighting (with "Thinking Mode")
  2. **The Build Out**: Add structural elements (conditional)
  3. **The Screen Install**: Install motorized screens using reference images
  4. **The Check**: Quality control with retry logic
- Model: `gemini-3-pro-image-preview` ("Nano Banana Pro")
- Added retry logic for 429 rate limit errors
- Created live test script: `scripts/test_gemini_live.py`

### Phase 2: Fixing "Generate vs Edit" Issue
- **Problem:** AI was generating new images instead of editing existing ones
- **Solution:** 
  - Updated all prompts to start with "Edit this image..."
  - Added strict constraints: "Do not change the house structure or camera angle"
  - Implemented `guidance_scale=70` in `ImageGenerationConfig`
  - Added `person_generation="dont_generate_people"`

### Phase 3: Web Research & API Verification
- Confirmed `generate_content` is the ONLY method for Gemini 3 Pro editing in standard SDK
- Verified `edit_image` is Vertex AI only (not available with API key)
- Confirmed multimodal approach with `guidance_scale` is correct for strict editing

### Phase 4: Ruthless Codebase Cleanup
**Deleted Files:**
- Legacy providers: `mock_provider.py`, `openai_provider.py`
- Legacy processor: `image_processor.py`
- 50+ temporary scripts, markdown docs, test files, JSON reports

**Refactored Files:**
- `api/ai_enhanced_processor.py`: Reduced from 512 to ~100 lines, Gemini-only
- `api/views.py`: Removed fallback to legacy processor
- `api/ai_services/providers/__init__.py`: Gemini-only imports

**Final Structure:**
```
homescreen/
├── api/
│   ├── ai_enhanced_processor.py (Gemini-only, 100 lines)
│   ├── ai_services/
│   │   ├── screen_visualizer.py (4-step pipeline)
│   │   └── providers/
│   │       ├── gemini_provider.py
│   │       └── base_provider.py
├── frontend/
├── media/
├── scripts/
│   └── test_gemini_live.py (main test)
├── manage.py
├── requirements.txt
└── README.md
```

### Phase 5: Bug Fixes
**Import Error:**
- **Issue:** `ModuleNotFoundError: No module named 'api.ai_services.providers.mock_provider'`
- **Fix:** Updated `api/ai_services/providers/__init__.py` to remove deleted imports

**Unknown Error (Unresolved):**
- **Issue:** Web app returns exact same image as input
- **Status:** Created `potential_bugs.md` with 7 potential root causes
- **Most Likely:** API key not being passed through factory → provider → visualizer chain

---

## Key Files Modified

### Core AI Files
1. `api/ai_services/screen_visualizer.py`
   - Lines: 1-238
   - 4-step pipeline with Gemini 3 Pro
   - Strict editing prompts
   - Rate limit handling
   - QC loop with retry

2. `api/ai_enhanced_processor.py`
   - Lines: 1-183
   - Simplified to Gemini-only
   - Removed detection/analysis steps
   - Single variation per request

3. `api/ai_services/providers/gemini_provider.py`
   - Lines: 1-179
   - Wraps ScreenVisualizer
   - Maps screen_type to mesh_type
   - Converts PIL Image to bytes

4. `api/views.py`
   - Lines: 226-235
   - Removed fallback logic
   - Simplified processor instantiation

### Configuration
5. `.env`
   - Added: `GOOGLE_API_KEY=AIzaSyBX0cJ4nIOHtKv8ntFpx107YsplLqN88iM`

6. `requirements.txt`
   - Added: `google-genai`

---

## Test Results

### Manual Test (`scripts/test_gemini_live.py`)
- **Status:** ✅ Success
- **Output:** `media/generated/manual/final_result.jpg` (214KB)
- **Observations:** 
  - Pipeline executes all 4 steps
  - Rate limits encountered and handled
  - Image generated successfully
  - Processing time: ~1-2 minutes

### Web App Test
- **Status:** ❌ Failed
- **Issue:** Returns exact input image (no modification)
- **Error:** Silent failure, no exception logged
- **Next Steps:** Debug API key flow (see `potential_bugs.md`)

---

## Environment Details

### API Configuration
- Model: `gemini-3-pro-image-preview`
- Rate Limit: 2 requests per minute (free tier)
- Pipeline: 4 API calls per image
- Expected Time: 1-2 minutes per visualization

### Dependencies
```
Django==4.2.7
Pillow==10.1.0
google-genai==latest
python-dotenv==1.0.0
```

### Server
- Django dev server: `0.0.0.0:8000`
- Database: SQLite (`db.sqlite3`)

---

## Known Issues

### 1. Web App Returns Unmodified Image
**Severity:** High  
**Status:** Investigating  
**Root Causes (Suspected):**
- API key not passed through factory
- Silent fallback in `_generate_content_image`
- Background thread env var context issue
- Response structure mismatch in image extraction

**Debug File:** `potential_bugs.md`

### 2. Rate Limiting
**Severity:** Expected  
**Status:** Handled  
**Solution:** Retry logic with exponential backoff (5s, 10s, 15s)

### 3. Reference Images Not Loaded
**Severity:** Low  
**Status:** TODO  
**Issue:** `self.reference_images.get(mesh_type)` returns None
**Fix:** Need to populate reference images dict in ScreenVisualizer.__init__

---

## Code Snippets

### ScreenVisualizer Pipeline
```python
def process_pipeline(self, image: Image.Image, mesh_type: str = "solar") -> Image.Image:
    # Step 1: Cleanse
    cleaned = self.step_1_cleanse(image)
    
    # Step 2: Build Out (conditional)
    if self._analyze_structure(cleaned):
        built_out = self.step_2_build_out(cleaned)
    else:
        built_out = cleaned
    
    # Step 3: Screen Install
    screened = self.step_3_install_screen(built_out, None, mesh_type)
    
    # Step 4: Quality Check
    if not self.step_4_quality_check(screened, mesh_type):
        screened = self.step_3_install_screen(built_out, None, mesh_type, retry=True)
    
    return screened
```

### Strict Editing Prompt
```python
prompt = "Edit this image. Remove all visual clutter (hoses, trash, debris). Fix the lighting. Do not change the house structure or camera angle. Keep the canvas exact."
```

### Guidance Config
```python
config_args['image_generation_config'] = types.ImageGenerationConfig(
    guidance_scale=70,  # High guidance to adhere to prompt/image
    person_generation="dont_generate_people"
)
```

---

## Performance Metrics

### Pipeline Execution
- **Step 1 (Cleanse):** ~20-30s
- **Step 2 (Build Out):** ~20-30s (if needed)
- **Step 3 (Install):** ~20-30s
- **Step 4 (QC):** ~10s
- **Total:** 1-2 minutes
- **Rate Limits Hit:** Almost always (4 calls > 2 RPM limit)

### Code Statistics
- **Files Deleted:** 50+
- **Lines Removed:** ~400 (ai_enhanced_processor.py alone)
- **Code Reduced:** ~80% in core processor

---

## Next Steps

1. **Fix Web App Image Generation:**
   - Debug API key flow through factory/provider/visualizer
   - Add verbose logging to capture actual errors
   - Test direct API call vs factory pattern
   - Remove fallbacks temporarily to force error visibility

2. **Implement Reference Images:**
   - Load fabric swatches for each mesh_type
   - Store in `media/reference_images/`
   - Update ScreenVisualizer.__init__

3. **Optimize Rate Limiting:**
   - Consider caching Step 1 & 2 results
   - Implement request queuing
   - Add user feedback for rate limit delays

4. **Production Hardening:**
   - Add proper error messages to frontend
   - Implement request timeout handling
   - Add API usage tracking
   - Set up monitoring/alerting

---

## Artifacts Created

1. `task.md` - Task checklist (marked Phase 6 complete)
2. `walkthrough.md` - Implementation summary with Screen King details
3. `potential_bugs.md` - Debugging guide for web app issue

---

## Commands Run

### Project Cleanup
```bash
rm *_GUIDE.md *_SUMMARY.md chatgptapi*.md
rm analyze_*.py test_*.py debug_*.py
rm test_mask_*.png test_result_*.jpg
rm -rf test_utils/
```

### Server Management
```bash
pkill -f runserver
python3 manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &
```

### Testing
```bash
python3 scripts/test_gemini_live.py
python3 manage.py shell -c "from api.ai_enhanced_processor import AIEnhancedImageProcessor; print('Import successful')"
```

---

## Lessons Learned

1. **Gemini SDK:** `generate_content` with multimodal input is the only way to edit images with API key (not Vertex AI)
2. **Rate Limits:** 2 RPM on free tier is very restrictive for 4-step pipelines
3. **Silent Failures:** Fallback logic can hide real errors - be ruthless with error propagation
4. **Code Cleanup:** Deleting legacy code immediately reveals hidden dependencies (import errors)
5. **API Key Flow:** Complex factory patterns can obscure where config values come from

---

## End of Session Summary

**Goal:** Implement Gemini AI pipeline for screen visualization  
**Achieved:** ✅ Manual test script works, codebase is clean and modular  
**Blocked:** ❌ Web app integration has silent failure (API key issue suspected)  
**Time Invested:** ~2 hours  
**Code Quality:** Significantly improved (ruthless cleanup completed)  
**Next Session:** Debug web app API key flow and test live generation
