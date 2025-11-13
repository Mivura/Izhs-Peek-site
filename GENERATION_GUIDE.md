# House Pages Generation Guide

This document explains how the 20 new house pages were automatically generated from the archive.

## Overview

The `generate_houses.py` script was created to automate the process of creating house pages from the archive folders. It reads Excel files, copies images, generates HTML templates, and updates the Flask application.

## What the Script Does

1. **Reads Excel Data**:
   - `Характеристики.xlsx` (or variations like `Характристики.xlsx`, `характер.xlsx`)
   - `калькулятор.xlsx` (or `калькулятор1.xlsx`)
   - Extracts house characteristics from cells A2:B8
   - Extracts calculator services with automatic parsing

2. **Processes Images**:
   - Finds photos: 1.png, 2.png, 3.png, 4.png (any extension)
   - Finds floor plans: plan.JPG, plan 1.PNG, plan 2.PNG, Проект.JPG
   - Copies all to `static/img/domN_kark/` with normalized names

3. **Generates HTML Templates**:
   - Creates `templates/domN_kark/house_1.html` for each house
   - Includes characteristics, photo slider, floor plans, calculator
   - Uses Jinja2 templating syntax for Flask

4. **Updates Configuration**:
   - Adds entries to `houses_data.json`
   - Generates Flask routes for `app.py`

## Archive Structure Expected

```
Дома/
├── ДВ- 201/
│   ├── 1.png
│   ├── 2.png
│   ├── 3.png
│   ├── 4.png
│   ├── plan 1.PNG
│   ├── plan 2.PNG
│   ├── Характристики.xlsx
│   └── калькулятор.xlsx
├── ДВ- 202/
│   └── ...
└── ... (20 folders total)
```

## Excel File Formats

### Характеристики.xlsx (A2:B8)
| Column A (название) | Column B (значение) |
|---------------------|---------------------|
| Общая площадь дома: | 124 м2 |
| Жилая площадь дома: | 108 м2 |
| Площадь террасы: | 16 м2 |
| Кол-во этажей: | 2 этаж |
| Кол-во спален: | 4 спальни |
| Кол-во санузлов: | 2 санузла |

### калькулятор.xlsx
| Column A (услуга) | Column B (цена) |
|-------------------|-----------------|
| железобетонные сваи 25 шт. + пробное бурение. | 215000 |
| Замена базового кровельного материала на мягкую кровлю Шинглас (Технониколь) | 386750 |

The script automatically:
- Extracts main title and description from service names
- Text in parentheses becomes description
- Text after '+' becomes description
- Formats prices with spaces (215000 → 215 000 ₽)

## Running the Script

```bash
cd /home/runner/work/Izhs-Peek-site/Izhs-Peek-site
python3 generate_houses.py
```

Output:
- Creates template folders and HTML files
- Copies images to static/img/
- Updates houses_data.json
- Generates new_routes.py with Flask routes

Then manually:
1. Copy routes from new_routes.py to app.py (already done)
2. Test the application
3. Commit changes

## Generated House Pages

Each house page includes:

1. **Header**: House name and main image
2. **Characteristics Section**: 6 key characteristics from Excel
3. **Floor Plans Slider**: Interactive slider for multiple floors
4. **Photo Gallery**: Swiper.js slider with all house photos
5. **Calculator**: Services from Excel with checkboxes and price calculation
6. **Contact Button**: Link to contact form

## Key Features

### Intelligent Parsing
- Handles various Excel file naming conventions
- Detects image formats automatically (.png, .jpg, .PNG, .JPG)
- Parses service titles to extract descriptions
- Supports both single and multiple floor plans

### Template Generation
- Uses proper Jinja2 syntax
- Includes all necessary CSS and JavaScript
- Responsive design with media queries
- Swiper.js integration for galleries

### Error Handling
- Warns about missing files
- Provides fallback values for missing data
- Continues processing even if some files are missing

## Results

Successfully generated:
- 20 house templates (dom6_kark through dom25_kark)
- 20 Flask routes (house6 through house25)
- 20 entries in houses_data.json
- ~80 house photos
- ~30 floor plan images
- All with proper calculator services from Excel

## Future Use

If you need to add more houses:

1. Extract new archive folder to `Дома/`
2. Run `python3 generate_houses.py` again
3. Copy new routes to app.py
4. Commit and test

The script is reusable and can process any number of house folders following the same structure.

## Technical Notes

- Python 3 with openpyxl library required
- Flask and flask-wtf for the web application
- Jinja2 templating engine
- Swiper.js for sliders (already included in base.html)

## Troubleshooting

**Problem**: Script reports missing Excel files
- Check file names match expected patterns
- Ensure Excel files are not corrupted

**Problem**: Images not displaying
- Check file extensions are correct
- Verify images were copied to static/img/

**Problem**: Flask routes not working
- Ensure routes were added to app.py
- Check houses_data.json has correct paths
- Restart Flask application

## Security

The script has been checked with CodeQL and found no vulnerabilities:
- Safe file handling
- No SQL injection risks
- No XSS vulnerabilities
- Proper input validation
