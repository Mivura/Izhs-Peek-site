# House data configuration
# This file contains all house-specific data for the template system

# Common services available for all houses
COMMON_SERVICES = [
    {"name": "Свайно-винтовой фундамент 16 свай", "description": "• проба грунта", "price": 132000},
    {"name": "Железобетонные сваи 16 шт.", "description": "• пробное бурение", "price": 147000},
    {"name": "Монолитная железобетонная плита толщиной 250мм", "description": "• с учётом опалубки, подсыпки песка и щебня (При условии ровного участка)", "price": 432000},
    {"name": "Усиление половых лаг первого этажа", "description": "", "price": 40500},
    {"name": "Водосточная система деке, цвет на выбор", "description": "", "price": 85000},
    {"name": "Вентиляция комплект вент. грибков в кровлю • приточные КИВ клапаны", "description": "", "price": 160000},
    {"name": "Зашивка цоколя в 1 ряд панелями деке", "description": "", "price": 67400},
    {"name": "до точек электропроводки • щиток", "description": "", "price": 210000},
    {"name": "Черновая разводка ГВС, ХВС и канализации по дому", "description": "", "price": 170000},
    {"name": "Отопление электрическими обогревателями (комплект с установкой на весь дом)", "description": "", "price": 90000},
    {"name": "Отопление дома от электро котла: 1 этаж - водяные тёплые полы с полусухой стяжкой, 2 этаж - радиаторы", "description": "", "price": 559000},
    {"name": "Отопление водяными радиаторами • электро котёл", "description": "", "price": 510000},
    {"name": "Автономная канализация. Станция биологической очистки (Септик)", "description": "", "price": 260000},
    {"name": "Фильтрационная система", "description": "• стоимость может измениться после анализа воды", "price": 300000},
    {"name": "Временка для рабочих схем", "description": "• временное электроснабжение на период строительства", "price": 45000},
    {"name": "Аренда блок-контейнера для проживания бригады", "description": "• на весь срок строительства", "price": 120000},
    {"name": "Вывоз мусора после строительства", "description": "• 1 Пухто или 2 газели", "price": 35000},
    {"name": "Регистрация дома", "description": "• технический план здания с подачей документов в Росреестр", "price": 55000},
]

# Common features for all houses
COMMON_FEATURES = [
    {"name": "Фундамент", "details": "Монолитная железобетонная плита 200мм", "warm": True, "engineering": True, "finishing": True},
    {"name": "Силовой каркас", "details": "Силовой каркас заводского изготовления QuickFrame", "warm": True, "engineering": True, "finishing": True},
    {"name": "Кровля", "details": "Фальцевая кровля (сталь 0,5 мм)", "warm": True, "engineering": True, "finishing": True},
    {"name": "Окна и входные двери", "details": "Окна REHAU Delight\nВходная дверь: Jeld-Wen F 2000 или аналог", "warm": True, "engineering": True, "finishing": True},
    {"name": "Отделка фасада", "details": "Скандинавская технологичная доска\nИмпрегнированная террасная доска", "warm": True, "engineering": True, "finishing": True},
    {"name": "Сопровождение строительства", "details": "Технадзор\nВидеонаблюдение", "warm": True, "engineering": True, "finishing": True},
    {"name": "Инженерные сети", "details": "Канализация, отопление, водоснабжение, электричество", "warm": False, "engineering": True, "finishing": True},
    {"name": "Внутренняя отделка", "details": "Отделка стен", "warm": False, "engineering": False, "finishing": True},
]

# Common configurations for all houses
COMMON_CONFIGURATIONS = [
    {"name": "Сруб из бруса 150x150мм", "description": "Базовый комплект: коробка дома, кровля", "price": 1200000},
    {"name": "Дом из бруса 150x150мм", "description": "Полная комплектация: отделка, окна, двери", "price": 1800000},
    {"name": "Дом из бруса 200x150мм", "description": "Премиум: утепление, полная отделка", "price": 2200000},
]

# House-specific data
HOUSES = {
    "dom1_kark": {
        "name": "Название дома 1",
        "folder": "dom1_kark",
        "specs": {
            "total_area": 191,
            "living_area": 136,
            "terrace_area": 55,
            "floors": "2 этажа",
            "bedrooms": "3 спальни",
            "bathrooms": "2 санузла"
        },
        "floor_plans": ["plan.png", "plan2.PNG"],
        "photos": ["/1.jpg", "/2.jpg", "/3.jpg", "/4.jpg"],
        "prices": {
            "warm": 11088182,
            "engineering": 13550769,
            "finishing": 16837493
        },
        "features": COMMON_FEATURES,
        "configurations": COMMON_CONFIGURATIONS,
        "services": COMMON_SERVICES
    },
    "dom2_kark": {
        "name": "Название дома 2",
        "folder": "dom2_kark",
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
    },
    "dom3_kark": {
        "name": "Название дома 3",
        "folder": "dom3_kark",
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
    },
    "dom4_kark": {
        "name": "Название дома 4",
        "folder": "dom4_kark",
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
    },
    "dom5_kark": {
        "name": "Название дома 5",
        "folder": "dom5_kark",
        "specs": {
            "total_area": 191,
            "living_area": 136,
            "terrace_area": 55,
            "floors": "1 этаж",
            "bedrooms": "3 спальни",
            "bathrooms": "2 санузла"
        },
        "floor_plans": ["plan.png"],
        "photos": ["/1.jpg", "/2.jpg", "/3.jpg", "/4.jpg"],
        "prices": {
            "warm": 11088182,
            "engineering": 13550769,
            "finishing": 16837493
        },
        "features": COMMON_FEATURES,
        "configurations": COMMON_CONFIGURATIONS,
        "services": COMMON_SERVICES
    },
}
