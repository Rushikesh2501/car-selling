import datetime
from typing import List, Optional
from app.models import Car

# Dynamic star rating calculator based on condition and age
def calculate_rating(condition: str, year: int) -> float:
    # 1. Condition score (1-5)
    condition_map = {
        "Excellent": 5.0,
        "Very Good": 4.0,
        "Good": 3.0,
        "Fair": 2.0,
        "Poor": 1.0
    }
    cond_score = condition_map.get(condition, 3.0)
    
    # 2. Age score (1-5)
    current_year = datetime.datetime.now().year # 2026
    age = max(0, current_year - year)
    
    if age <= 1:
        age_score = 5.0
    elif age <= 3:
        age_score = 4.0
    elif age <= 6:
        age_score = 3.0
    elif age <= 10:
        age_score = 2.0
    else:
        age_score = 1.0
        
    # Average of condition and age
    avg_score = (cond_score + age_score) / 2.0
    # Round to nearest 0.5 for elegant star presentation
    return round(avg_score * 2) / 2.0

# Dynamic Image assigner matching body styles and brands
def get_car_image(body_type: str, seed: int) -> str:
    sedan_images = [
        "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1619767886558-efdc259cde1a?auto=format&fit=crop&w=600&q=80",
    ]
    hatchback_images = [
        "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1590362891991-f776e747a588?auto=format&fit=crop&w=600&q=80",
    ]
    mpv_images = [
        "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=600&q=80",
    ]
    
    if body_type == "sedan":
        return sedan_images[seed % len(sedan_images)]
    elif body_type == "hatchback":
        return hatchback_images[seed % len(hatchback_images)]
    else:
        return mpv_images[seed % len(mpv_images)]

# Master List of 51 completely unique Base Models in India (Prices in INR)
BASE_MODELS = [
    # Sedans (19 Models)
    ("Toyota", "Camry Hybrid", "sedan", 4600000.0, 2.5, "Hybrid", "Premium hybrid executive sedan with outstanding cabin luxury, soft ventilated seats, and absolute fuel efficiency."),
    ("Toyota", "Corolla Altis", "sedan", 2150000.0, 1.8, "Petrol", "Highly reliable executive sedan featuring absolute cabin safety, premium seating, and smooth gearbox."),
    ("Honda", "Civic", "sedan", 2400000.0, 1.5, "Petrol", "Sporty low-slung sedan with a turbocharged motor, sharp paddle shifters, and high-tech cabin."),
    ("Honda", "City i-VTEC", "sedan", 1450000.0, 1.5, "Petrol", "India's legendary premium family sedan with refined i-VTEC motor, premium leatherette upholstery, and spacious cabin."),
    ("Honda", "Amaze CVT", "sedan", 890000.0, 1.2, "Petrol", "Comfortable sub-compact city sedan with light steering dynamics, spacious boot capacity, and advanced CVT."),
    ("BMW", "3 Series GL", "sedan", 6100000.0, 2.0, "Diesel", "Long-wheelbase luxury sports sedan with massive rear legroom, panoramic dual sunroof, and athletic dynamics."),
    ("BMW", "5 Series M Sport", "sedan", 7450000.0, 2.0, "Petrol", "Luxurious executive business cruiser equipped with dynamic damping, gesture control cockpit, and premium sound."),
    ("Mercedes-Benz", "C-Class Elegance", "sedan", 6400000.0, 2.0, "Petrol", "Elegant baby S-Class sedan with high-res portrait touch console, mild-hybrid motor, and multi-color ambient lounge."),
    ("Mercedes-Benz", "E-Class LWB", "sedan", 7900000.0, 3.0, "Diesel", "Chauffeur-driven ultimate luxury sedan, featuring active air suspension, soft rear electric reclining seats."),
    ("Audi", "A4 TFSI", "sedan", 4750000.0, 2.0, "Petrol", "Crisp luxury sedan with virtual cockpit, legendary build quality, and super-fast dual-clutch transmission."),
    ("Audi", "A6 Matrix", "sedan", 6150000.0, 2.0, "Petrol", "Elite business sedan with touch acoustic responses, adaptive lane assists, and matrix LED lighting sweeps."),
    ("Hyundai", "Verna Turbo", "sedan", 1650000.0, 1.5, "Petrol", "Aggressive parametric sedan with heated/ventilated seats, ADAS Level 2, and best-in-class direct injection power."),
    ("Hyundai", "Aura Executive", "sedan", 820000.0, 1.2, "Petrol", "Compact commuter sedan with rich dual-tone cabins, rear AC ventilation, and highly light responsive controls."),
    ("Skoda", "Slavia TSI", "sedan", 1380000.0, 1.0, "Petrol", "European handling dynamics, high ground clearance, structural safety ratings, and highly punchy TSI pull."),
    ("Skoda", "Superb L&K", "sedan", 3900000.0, 2.0, "Petrol", "Premium flagship sedan offering massive rear executive legroom, high-end Canton acoustics, and fast TSI pull."),
    ("Volkswagen", "Virtus GT", "sedan", 1550000.0, 1.5, "Petrol", "Sporty GT-badged handling machine with cylinder deactivation technology, 5-star GNCAP, and red interior highlights."),
    ("Honda", "City e:HEV", "sedan", 1980000.0, 1.5, "Hybrid", "Advanced strong hybrid technology offering supreme fuel saving, ADAS safety aids, and silent city operations."),
    ("BMW", "7 Series Li", "sedan", 13500000.0, 3.0, "Petrol", "Absolute pinnacle of executive driving luxury. Theater screen in the back, acoustic quietness, and dynamic air suspension."),
    ("Mercedes-Benz", "S-Class Limousine", "sedan", 16000000.0, 3.0, "Diesel", "The finest car in the world, featuring level 3 autonomy, luxury pillows, rear axle steering, and pure dynamic class."),

    # Hatchbacks (18 Models)
    ("Toyota", "Glanza Luxury", "hatchback", 830000.0, 1.2, "Petrol", "Reliable premium hatchback with smart touch inputs, robust fuel economy, and absolute city maneuverability."),
    ("Hyundai", "i20 Asta", "hatchback", 980000.0, 1.2, "Petrol", "Vibrant premium hatchback featuring electric sunroof, advanced Bose surround system, and smart bluelink connectivity."),
    ("Hyundai", "i20 N Line Sport", "hatchback", 1250000.0, 1.0, "Petrol", "Aggressive sporty hot-hatch with stiffened handling dynamics, custom exhausts, and metallic N accents."),
    ("Hyundai", "Grand i10 Nios", "hatchback", 680000.0, 1.2, "Petrol", "Perfect city runabout with highly refined four-cylinder engine, wireless phone charging, and cozy seating."),
    ("Suzuki", "Swift ZXi", "hatchback", 720000.0, 1.2, "Petrol", "India's beloved agile handling hatchback, built on a lightweight frame with high-efficiency motor tuning."),
    ("Suzuki", "Baleno Alpha", "hatchback", 890000.0, 1.2, "Petrol", "Spacious premium hatchback loaded with interactive head-up display, 360-degree parking eyes, and high comfort."),
    ("Suzuki", "Alto K10", "hatchback", 430000.0, 1.0, "Petrol", "The absolute entry hatchback champion. High fuel economy, light parking, and low maintenance."),
    ("Suzuki", "WagonR ZXi", "hatchback", 590000.0, 1.2, "Petrol", "Tall-boy legendary family hatchback. Massive headroom, huge glass greenhouse, and incredibly easy ingress-egress."),
    ("Suzuki", "Ignis Alpha", "hatchback", 660000.0, 1.2, "Petrol", "Tough urban micro-hatchback with SUV-like high ground clearances, modular retro dashboards, and high visibility."),
    ("Tata", "Altroz XZ", "hatchback", 880000.0, 1.2, "Petrol", "Sturdy premium hatchback with gold GNCAP safety credentials, spacious cabin, and 90-degree opening doors."),
    ("Tata", "Tiago XZ", "hatchback", 580000.0, 1.2, "Petrol", "Solid commuter hatchback with premium Harman acoustics, cornering controls, and robust crash protection."),
    ("Tata", "Tiago EV Green", "hatchback", 1050000.0, 0.0, "Electric", "Silent commuter electric hatch with multi-regen systems, instant torque, and cheap green operating costs."),
    ("Mini", "Cooper S", "hatchback", 4400000.0, 2.0, "Petrol", "Luxury premium go-kart hatchback with dual turbo pulls, gorgeous round LED dials, and explosive speeds."),
    ("Suzuki", "Celerio VXi", "hatchback", 540000.0, 1.0, "Petrol", "Compact city commuter with high fuel economy, light controls, and incredibly low ownership costs."),
    ("Suzuki", "S-Presso", "hatchback", 480000.0, 1.0, "Petrol", "Mini crossover hatchback style, high seating position, strong dashboard console, and easy driving posture."),
    ("Tata", "Altroz iTurbo", "hatchback", 920000.0, 1.2, "Petrol", "Sporty variant of Altroz with a turbocharged 3-cylinder motor offering crisp acceleration and planted cornering."),
    ("Toyota", "Glanza V", "hatchback", 940000.0, 1.2, "Petrol", "Top-tier premium Toyota hatchback, with 6 airbags, 360-degree parking sensors, and heads up layout screen."),
    ("Honda", "Jazz ZX", "hatchback", 990000.0, 1.5, "Petrol", "Spacious family hatchback featuring electric sunroof, massive boot layout, and signature smooth engine refinement."),

    # MPVs (14 Models)
    ("Toyota", "Innova Crysta", "mpv", 2450000.0, 2.4, "Diesel", "The legendary mileage champion MPV. Extreme durability, plush captain seats, and robust highway diesel haul."),
    ("Toyota", "Innova Hycross", "mpv", 2950000.0, 2.0, "Hybrid", "Next-gen monocoque luxury hybrid MPV. Silent drives, immense fuel saving, panoramic skyroof, and ottoman reclines."),
    ("Toyota", "Vellfire VIP", "mpv", 12500000.0, 2.5, "Hybrid", "Ultra-premium mobile lounge MPV with heated massage recliners, drop-down screens, and dual sunroof luxury."),
    ("Toyota", "Rumion G", "mpv", 1220000.0, 1.5, "Petrol", "Spacious 7-seater MPV with automatic climate controls, smart hybrid engine tech, and elegant wood cabin finishes."),
    ("Suzuki", "Ertiga ZXi", "mpv", 1120000.0, 1.5, "Petrol", "India's highest selling practical 7-seater MPV. Exceptional cabin space utility, roof-mounted blowers, and smart hybrid."),
    ("Suzuki", "XL6 Alpha", "mpv", 1320000.0, 1.5, "Petrol", "Premium 6-seater lounge in deep black themes, captain rows, ventilated front seats, and smart automatic gearbox."),
    ("Kia", "Carens Luxury", "mpv", 1580000.0, 1.5, "Diesel", "Futuristic family recreational vehicle with air purifiers standard, full safety air curtains, and digital metrics."),
    ("Renault", "Triber RXZ", "mpv", 790000.0, 1.0, "Petrol", "Modular sub-4m MPV with removable third row, dual cooling air vents, and robust utility flexibility."),
    ("Kia", "Carnival VIP", "mpv", 4100000.0, 2.2, "Diesel", "Grand luxury limousine MPV, captain captain armrests, dual sunroof blocks, and effortless highway touring power."),
    ("Hyundai", "Staria Luxury", "mpv", 4600000.0, 2.2, "Diesel", "Futuristic premium lounge MPV with spaceship front lights, huge windows, and highly luxurious cabin options."),
    ("Mahindra", "Marazzo M6", "mpv", 1420000.0, 1.5, "Diesel", "Sturdy passenger MPV with shark-inspired body structure, roof-integrated surround cooling, and plush suspension."),
    ("Kia", "Carens Prestige", "mpv", 1280000.0, 1.5, "Petrol", "Value model family 7-seater Carens featuring robust build, massive dashboard, and advanced braking assists."),
    ("Suzuki", "Ertiga VXi", "mpv", 990000.0, 1.5, "Petrol", "Highly economical Ertiga model with essential tech, supreme seating comfort, and high fuel economy."),
    ("Renault", "Triber RXT", "mpv", 715000.0, 1.0, "Petrol", "Modular value-loaded MPV, dual gloveboxes, flexible storage spaces, and extremely compact city foot-print.")
]

# Clean Procedural Generator: 102 Completely Unique Cars (Zero Duplicates!)
def generate_seed_cars() -> List[Car]:
    generated_cars = []
    
    # We generate exactly 2 highly distinct sub-models for each of our 51 master lines:
    # 51 * 2 = 102 completely unique, distinct vehicles (No duplicates!).
    for i, base in enumerate(BASE_MODELS):
        brand, model, body_type, base_price, engine, fuel, base_desc = base
        
        # --- SUB-MODEL 1: "Pro Edition" (Year 2025/2026, Excellent) ---
        id_1 = i * 2 + 1
        year_1 = 2025
        # Premium model variant pricing
        price_1 = base_price * 1.05
        condition_1 = "Excellent"
        mileage_1 = 5000 + (id_1 * 95) % 5000  # deterministic low mileage
        image_1 = get_car_image(body_type, id_1)
        colors_pool_1 = ["White", "Black", "Red", "Blue", "Silver", "Grey", "Bronze"]
        color_1 = colors_pool_1[id_1 % len(colors_pool_1)]
        desc_1 = f"Color: {color_1}. {base_desc} Pro Edition. Brand new condition with advanced driver tech, zero signs of wear, and active manufacturer warranty."
        rating_1 = calculate_rating(condition_1, year_1)
        
        generated_cars.append(Car(
            id=id_1,
            brand=brand,
            model=f"{model} Pro",
            year=year_1,
            price=price_1,
            condition=condition_1,
            engine_capacity=engine,
            body_type=body_type,
            rating=rating_1,
            image_url=image_1,
            description=desc_1,
            mileage=mileage_1,
            fuel_type=fuel,
            color=color_1
        ))
        
        # --- SUB-MODEL 2: "Plus Edition" (Year 2023, Very Good) ---
        id_2 = i * 2 + 2
        year_2 = 2023
        # Pre-owned model variant pricing
        price_2 = base_price * 0.82
        condition_2 = "Very Good"
        mileage_2 = 24000 + (id_2 * 115) % 12000  # moderate mileage
        image_2 = get_car_image(body_type, id_2)
        colors_pool_2 = ["Silver", "Grey", "White", "Black", "Blue", "Red", "Bronze"]
        color_2 = colors_pool_2[id_2 % len(colors_pool_2)]
        desc_2 = f"Color: {color_2}. {base_desc} Plus Edition. Sparingly used in clean condition, complete dealer service logs, and single ownership history."
        rating_2 = calculate_rating(condition_2, year_2)
        
        generated_cars.append(Car(
            id=id_2,
            brand=brand,
            model=f"{model} Plus",
            year=year_2,
            price=price_2,
            condition=condition_2,
            engine_capacity=engine,
            body_type=body_type,
            rating=rating_2,
            image_url=image_2,
            description=desc_2,
            mileage=mileage_2,
            fuel_type=fuel,
            color=color_2
        ))
        
    return generated_cars

# Process and return completed Car models with computed dynamic ratings
def get_all_cars() -> List[Car]:
    # Returns 102 completely unique cars in INR
    return generate_seed_cars()
