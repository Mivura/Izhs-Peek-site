# House Template System - Refactoring Documentation

## Overview
This refactoring introduces a unified template system for house pages, eliminating code duplication and making it easier to add new houses.

## Changes Made

### 1. Unified House Template
- **File**: `templates/house_template.html`
- All house pages now use a single template
- Accepts parameters for house-specific data
- Reduces code duplication from ~1200 lines per house to a single shared template

### 2. House Data Configuration
- **File**: `house_data.py`
- Centralized configuration for all house-specific data
- Common data (services, features, configurations) defined once and reused
- Easy to add new houses by adding entries to the `HOUSES` dictionary

### 3. Optimized Slider System
- **CSS**: `static/css/house.css` - Modern, responsive styles
- **JavaScript**: `static/js/house.js` - Optimized slider functionality
- Features:
  - Smooth transitions with cubic-bezier easing
  - Touch/swipe support for mobile devices
  - Keyboard navigation (Arrow keys)
  - Auto-play capability (currently disabled, can be enabled)
  - Mobile-responsive design

### 4. Updated Flask Routes
- Routes now use the unified template
- Pull data from `house_data.py` configuration
- Cleaner, more maintainable code

## How to Add a New House

1. **Add house images** to `static/img/dom{N}_kark/` folder:
   - `1.jpg`, `2.jpg`, etc. (house photos)
   - `plan.png` (floor plan)

2. **Add house data** to `house_data.py`:
   ```python
   "dom6_kark": {
       "name": "Название дома 6",
       "folder": "dom6_kark",
       "specs": {
           "total_area": 191,
           "living_area": 136,
           "terrace_area": 55,
           "floors": "1 этаж",
           "bedrooms": "3 спальни",
           "bathrooms": "2 санузла"
       },
       "floor_plans": ["plan.png"],
       "photos": ["/1.jpg", "/2.jpg", "/3.jpg"],
       "prices": {
           "warm": 11088182,
           "engineering": 13550769,
           "finishing": 16837493
       },
       "features": COMMON_FEATURES,
       "configurations": COMMON_CONFIGURATIONS,
       "services": COMMON_SERVICES
   }
   ```

3. **Add route** in `app.py`:
   ```python
   @app.route('/house6')
   def house_kark_6():
       house_data = HOUSES.get('dom6_kark')
       return render_template("house_template.html", 
                             house_name=house_data['name'],
                             house_folder=house_data['folder'],
                             specs=house_data['specs'],
                             floor_plans=house_data['floor_plans'],
                             photos=house_data['photos'],
                             features=house_data['features'],
                             prices=house_data['prices'],
                             configurations=house_data['configurations'],
                             services=house_data['services'])
   ```

4. **Update catalog** in `index.html` to link to the new house.

## Slider Features

### Photo Slider
- Modern, responsive design
- Navigation buttons with hover effects
- Dot indicators
- Touch/swipe support for mobile
- Keyboard navigation
- Smooth CSS transitions

### Floor Plan Slider
- For multi-floor houses
- Same navigation features as photo slider
- Automatically hides if only one floor plan

### Index Page Slider
- Hover to pause auto-play
- Smooth fade transitions
- Mobile-responsive

## Mobile Responsiveness
All sliders and layouts are optimized for mobile devices:
- Responsive breakpoints at 768px
- Touch/swipe gestures
- Adjusted button sizes
- Optimized image loading
- Fixed calculator total bar for mobile

## Benefits
1. **Reduced Code Duplication**: From ~6000 lines (5 houses × ~1200 lines) to one template
2. **Easier Maintenance**: Changes apply to all houses automatically
3. **Consistent Design**: All houses use the same modern design
4. **Faster Development**: Add new houses in minutes, not hours
5. **Better Performance**: Optimized CSS and JavaScript
6. **Mobile-Friendly**: Touch support and responsive design

## Old vs New
- **Before**: Each house had its own HTML file with duplicated code
- **After**: One template, data-driven approach
- **Lines of Code Saved**: ~5000+ lines
