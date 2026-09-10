import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from inventory.models import Vehicle, VehicleImage
from store.models import Category, Part, Order, OrderItem
from service.models import ServiceBay, Appointment

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds realistic automotive demo data for CarCraft Dealership Suite (India Market)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("🚀 Starting CarCraft database seeding for Indian Market..."))

        # 1. Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@carcraft.in', 'admin123')
            self.stdout.write(self.style.SUCCESS("  [+] Superuser created: admin / admin123"))

        # 2. Service Bays (Indian Technicians & Workshop Labs)
        bays_data = [
            {
                'bay_number': 1,
                'name': 'Bay 1 - Dyno Diagnostics & ECU Calibration Lab',
                'assigned_technician': 'Rameshwar Patil (Master Diagnostic Specialist)',
                'specialty': 'Dyno Tuning, ECU Remapping & Diagnostic Telematics',
                'is_active': True,
            },
            {
                'bay_number': 2,
                'name': 'Bay 2 - 3D Laser Alignment & Suspension Bay',
                'assigned_technician': 'Arjun Nair (Chassis & Alignment Specialist)',
                'specialty': 'Hunter 3D 4-Wheel Laser Alignment & Corner Balancing',
                'is_active': True,
            },
            {
                'bay_number': 3,
                'name': 'Bay 3 - Periodic Maintenance & Mechanical Bay',
                'assigned_technician': 'Siddharth Sengupta (Master Drivetrain Tech)',
                'specialty': 'Fully Synthetic Oil Service, Brake Overhauls & Mechanical Lube',
                'is_active': True,
            },
            {
                'bay_number': 4,
                'name': 'Bay 4 - High-Voltage EV & Hybrid Diagnostic Center',
                'assigned_technician': 'Priya Sharma (High-Voltage EV Specialist)',
                'specialty': 'EV High-Voltage Battery Thermal Management & Diagnostics',
                'is_active': True,
            },
        ]

        bays = {}
        for b_data in bays_data:
            bay_obj, _ = ServiceBay.objects.update_or_create(
                bay_number=b_data['bay_number'],
                defaults=b_data
            )
            bays[bay_obj.bay_number] = bay_obj
        self.stdout.write(self.style.SUCCESS(f"  [+] {len(bays)} Service bays configured."))

        # 3. Vehicle Inventory (India Market Lineup Across All Key Segments)
        # Clear old vehicles to prevent lingering US models
        Vehicle.objects.all().delete()

        vehicles_data = [
            # Hatchback: Maruti Suzuki Baleno, Tata Altroz
            {
                'vin': 'MA3EWB1S0RP104921',
                'year': 2024,
                'make': 'Maruti Suzuki',
                'model': 'Baleno',
                'trim': 'Alpha 1.2L DualJet MT',
                'type': 'Hatchback',
                'status': 'available',
                'odometer': 6400,
                'price': Decimal('938000.00'),
                'fuel_type': 'Gasoline',
                'transmission': 'Manual',
                'drivetrain': 'FWD',
                'exterior_color': 'Nexa Blue',
                'interior_color': 'Dual-Tone Black & Deep Blue Fabric',
                'engine': '1.2L K-Series DualJet Dual VVT Petrol',
                'horsepower': 89,
                'primary_image_url': 'https://images.unsplash.com/photo-1590362891988-f77612a7a588?auto=format&fit=crop&w=1200&q=80',
                'description': 'Top-spec 2024 Maruti Suzuki Baleno Alpha in signature Nexa Blue. Featuring 9-inch SmartPlay Pro+ touchscreen with surround sound by Arkamys, 360-degree HD view camera, and color Head-Up Display (HUD). Ideal premium hatchback for Indian urban commuting and highway road trips.',
                'features': '9-inch SmartPlay Pro+ Touchscreen, 360 View HD Camera, Head-Up Display (HUD), Suzuki Connect Connected Car Tech, Auto Climate Control, 6 Airbags, UV Cut Glass',
                'featured': False,
                'gallery': [
                    'https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=1200&q=80',
                ]
            },
            {
                'vin': 'MAT612349RP281903',
                'year': 2024,
                'make': 'Tata',
                'model': 'Altroz',
                'trim': 'Racer R3 Turbo MT',
                'type': 'Hatchback',
                'status': 'available',
                'odometer': 4200,
                'price': Decimal('1099000.00'),
                'fuel_type': 'Gasoline',
                'transmission': 'Manual',
                'drivetrain': 'FWD',
                'exterior_color': 'Atomic Orange Dual-Tone',
                'interior_color': 'Granite Black Leatherette with Racing Orange Accents',
                'engine': '1.2L i-Turbo+ 3-Cylinder Turbocharged Petrol',
                'horsepower': 118,
                'primary_image_url': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80',
                'description': 'Performance-tuned 2024 Tata Altroz Racer R3. Powered by the 120 PS turbocharged petrol motor paired with a slick 6-speed manual transmission. 5-star Global NCAP safety rating chassis with ventilated front seats, electric sunroof with voice assist, and 360-degree camera.',
                'features': '10.25-inch Floating Infotainment, Front Ventilated Seats, Voice-Activated Electric Sunroof, 360-Degree Surround Camera, 7-inch Digital Cluster, Blind Spot Monitor, 6 Airbags',
                'featured': False,
                'gallery': []
            },
            # Sedan: Honda City, Hyundai Verna, Skoda Slavia
            {
                'vin': 'MAKGM6680RP394821',
                'year': 2024,
                'make': 'Honda',
                'model': 'City',
                'trim': 'ZX e:HEV Strong Hybrid',
                'type': 'Sedan',
                'status': 'available',
                'odometer': 11500,
                'price': Decimal('2055000.00'),
                'fuel_type': 'Hybrid',
                'transmission': 'Automatic',
                'drivetrain': 'FWD',
                'exterior_color': 'Obsidian Blue Pearl',
                'interior_color': 'Beige & Black Two-Tone Leather',
                'engine': '1.5L Atkinson-Cycle i-VTEC Dual-Motor Strong Hybrid',
                'horsepower': 124,
                'primary_image_url': 'https://images.unsplash.com/photo-1550355291-bbee04a92027?auto=format&fit=crop&w=1200&q=80',
                'description': 'The executive hybrid benchmark. 2024 Honda City ZX e:HEV delivering class-leading 27.13 km/l fuel economy with self-charging dual-motor electric hybrid technology. Equipped with Honda SENSING Level 2 ADAS suite, lane watch camera, electric sunroof, and remote engine start.',
                'features': 'Honda SENSING ADAS Level 2 Suite, Self-Charging e:HEV Dual Motor, Electric Sunroof with One-Touch, LaneWatch Camera, Ambient Lighting, 8-Speaker Premium Sound, 6 Airbags',
                'featured': True,
                'gallery': [
                    'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1200&q=80'
                ]
            },
            {
                'vin': 'MALC451CLRP493820',
                'year': 2024,
                'make': 'Hyundai',
                'model': 'Verna',
                'trim': 'SX (O) 1.5 Turbo DCT',
                'type': 'Sedan',
                'status': 'available',
                'odometer': 8800,
                'price': Decimal('1738000.00'),
                'fuel_type': 'Gasoline',
                'transmission': 'Dual-Clutch',
                'drivetrain': 'FWD',
                'exterior_color': 'Abyss Black Pearl',
                'interior_color': 'All-Black Leatherette with Red Ambient Piping',
                'engine': '1.5L Turbo GDi 4-Cylinder Petrol (160 PS)',
                'horsepower': 158,
                'primary_image_url': 'https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=1200&q=80',
                'description': 'Futuristic fastback sedan with segment-leading 160 PS power. 2024 Hyundai Verna SX (O) Turbo with 7-speed DCT and paddle shifters. 0-100 km/h in just 8.1 seconds. Fitted with Hyundai SmartSense Level 2 ADAS, heated & ventilated front seats, and Bose 8-speaker audio.',
                'features': '0-100 km/h in 8.1s, Hyundai SmartSense Level 2 ADAS (17 Features), Dual 10.25-inch Curved Screens, Heated & Ventilated Front Seats, Bose 8-Speaker Sound, Smart Electric Sunroof',
                'featured': True,
                'gallery': []
            },
            {
                'vin': 'TMBNA2AA8RP583921',
                'year': 2023,
                'make': 'Skoda',
                'model': 'Slavia',
                'trim': 'Style 1.5 TSI Monte Carlo DSG',
                'type': 'Sedan',
                'status': 'available',
                'odometer': 14200,
                'price': Decimal('1869000.00'),
                'fuel_type': 'Gasoline',
                'transmission': 'Dual-Clutch',
                'drivetrain': 'FWD',
                'exterior_color': 'Tornado Red Dual-Tone',
                'interior_color': 'Monte Carlo Black & Red Leatherette',
                'engine': '1.5L TSI Turbocharged with Active Cylinder Technology (ACT)',
                'horsepower': 148,
                'primary_image_url': 'https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&w=1200&q=80',
                'description': 'Pure European driving dynamics engineered on the MQB-A0-IN platform. 2023 Skoda Slavia 1.5 TSI Monte Carlo in striking Tornado Red. Features blacked-out alloy wheels, electronic differential lock (XDS+), digital cockpit, and 521-liter boot capacity.',
                'features': '1.5L TSI with ACT Cylinder Deactivation, 7-Speed DSG Dual-Clutch, Monte Carlo Blackout Package, 10-inch Touchscreen with Wireless Apple CarPlay, Ventilated Seats, 6 Airbags',
                'featured': False,
                'gallery': []
            },
            # SUV / Compact SUV: Hyundai Creta, Tata Nexon, Mahindra XUV700, Kia Seltos
            {
                'vin': 'MALH581CLRP692810',
                'year': 2024,
                'make': 'Hyundai',
                'model': 'Creta',
                'trim': 'SX (O) 1.5 Turbo DCT',
                'type': 'SUV',
                'status': 'available',
                'odometer': 7500,
                'price': Decimal('2015000.00'),
                'fuel_type': 'Gasoline',
                'transmission': 'Dual-Clutch',
                'drivetrain': 'FWD',
                'exterior_color': 'Ranger Khaki Dual-Tone',
                'interior_color': 'Dual-Tone Grey & Black Leatherette',
                'engine': '1.5L Turbo GDi 4-Cylinder Petrol',
                'horsepower': 158,
                'primary_image_url': 'https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&w=1200&q=80',
                'description': "India's favorite midsize SUV. 2024 Facelift Hyundai Creta SX (O) Turbo featuring parametric black chrome grille, dual panoramic sunroof, Level 2 ADAS with 19 safety features, dual-zone climate control, and Hyundai BlueLink connected car telematics.",
                'features': 'Panoramic Sunroof, Level 2 ADAS Suite (19 Features), Dual-Zone Automatic Climate Control, Bose 8-Speaker Sound, Ventilated Seats, 360-Degree Camera, 8-Way Powered Driver Seat',
                'featured': True,
                'gallery': [
                    'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=1200&q=80'
                ]
            },
            {
                'vin': 'MAT613459RP782914',
                'year': 2024,
                'make': 'Tata',
                'model': 'Nexon',
                'trim': 'Fearless+ S 1.5 Diesel DCA',
                'type': 'SUV',
                'status': 'available',
                'odometer': 9200,
                'price': Decimal('1549000.00'),
                'fuel_type': 'Diesel',
                'transmission': 'Dual-Clutch',
                'drivetrain': 'FWD',
                'exterior_color': 'Daytona Grey',
                'interior_color': 'Fearless Black & Purple Leatherette',
                'engine': '1.5L 4-Cylinder Turbocharged Revotorq Diesel (260 Nm)',
                'horsepower': 113,
                'primary_image_url': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80',
                'description': '5-Star BNCAP rated compact SUV champion. 2024 Tata Nexon Fearless+ S Diesel DCA with 260 Nm punchy torque. Equipped with sequential bi-functional LED DRLs, 10.25-inch high-resolution infotainment screen, JBL 9-speaker audio with subwoofer, and 360 3D surround camera.',
                'features': '5-Star BNCAP Safety Rating, JBL 9-Speaker Audio with Subwoofer, 10.25-inch Harman Display, Voice-Assisted Electric Sunroof, Air Purifier with AQI Display, 360 3D Camera',
                'featured': False,
                'gallery': []
            },
            {
                'vin': 'MA1XU7000RP891234',
                'year': 2024,
                'make': 'Mahindra',
                'model': 'XUV700',
                'trim': 'AX7 L mStallion Petrol AT AWD',
                'type': 'SUV',
                'status': 'available',
                'odometer': 12800,
                'price': Decimal('2699000.00'),
                'fuel_type': 'Gasoline',
                'transmission': 'Automatic',
                'drivetrain': 'AWD',
                'exterior_color': 'Midnight Black',
                'interior_color': 'Luxury White Quilted Leatherette',
                'engine': '2.0L Turbocharged mStallion Petrol TGDi (200 PS / 380 Nm)',
                'horsepower': 197,
                'primary_image_url': 'https://images.unsplash.com/photo-1520050206274-a1ae44613e6d?auto=format&fit=crop&w=1200&q=80',
                'description': 'Flagship 7-seater powerhouse. 2024 Mahindra XUV700 AX7 Luxury Pack with All-Wheel Drive (AWD). Boasts 200 PS power, Sony 12-speaker 3D surround sound with roof-mounted tweeters, Panoramic Skyroof, flush smart door handles, and comprehensive Level 2 ADAS.',
                'features': 'All-Wheel Drive (AWD), Sony 12-Speaker 3D Immersive Audio, Dual 10.25-inch Superscreen, Panoramic Skyroof, Level 2 ADAS with Auto Emergency Braking, Smart Door Handles',
                'featured': True,
                'gallery': [
                    'https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&w=1200&q=80'
                ]
            },
            {
                'vin': 'MZBG881CLRP902341',
                'year': 2024,
                'make': 'Kia',
                'model': 'Seltos',
                'trim': 'X-Line 1.5 T-GDi 7DCT',
                'type': 'SUV',
                'status': 'pending',
                'odometer': 6100,
                'price': Decimal('2035000.00'),
                'fuel_type': 'Gasoline',
                'transmission': 'Dual-Clutch',
                'drivetrain': 'FWD',
                'exterior_color': 'Matte Graphite',
                'interior_color': 'Sage Green Leatherette with Orange Stitching',
                'engine': 'Smartstream 1.5L Turbo GDi (160 PS)',
                'horsepower': 158,
                'primary_image_url': 'https://images.unsplash.com/photo-1594502184342-2e12f877aa73?auto=format&fit=crop&w=1200&q=80',
                'description': 'Exquisite matte-finish styling with aggressive road presence. 2024 Kia Seltos X-Line with 160 PS Turbo-petrol engine. Features dual panoramic 10.25-inch cockpit displays, 8-inch smart Head-Up Display, Bose 8-speaker premium sound, and 360-degree blind view monitor.',
                'features': 'Matte Graphite Finish, Dual Panoramic 10.25-inch Displays, 8-inch Head-Up Display, Level 2 ADAS Suite (17 Features), Dual-Pane Panoramic Sunroof, Bose Sound System',
                'featured': False,
                'gallery': []
            },
            # Premium / Luxury: BMW 3 Series, Mercedes-Benz C-Class, Audi Q5
            {
                'vin': 'WBA330L00RP194820',
                'year': 2024,
                'make': 'BMW',
                'model': '3 Series Gran Limousine',
                'trim': '330Li M Sport Pro Edition',
                'type': 'Luxury',
                'status': 'available',
                'odometer': 5400,
                'price': Decimal('6260000.00'),
                'fuel_type': 'Gasoline',
                'transmission': 'Automatic',
                'drivetrain': 'RWD',
                'exterior_color': 'Portimao Blue Metallic',
                'interior_color': 'Vernasca Cognac Leather with M Headliner',
                'engine': '2.0L BMW TwinPower Turbo 4-Cylinder Petrol (258 HP / 400 Nm)',
                'horsepower': 255,
                'primary_image_url': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=1200&q=80',
                'description': 'The longest and most spacious sedan in its class. 2024 BMW 330Li M Sport Gran Limousine with 110mm extended wheelbase for supreme rear legroom. Features BMW Curved Display (14.9-inch + 12.3-inch) running iDrive 8, Harman Kardon 16-speaker sound, and 0-100 km/h in 6.2 seconds.',
                'features': '0-100 km/h in 6.2s, BMW Curved Display with OS 8, Harman Kardon 16-Speaker Audio (464W), Extended Limousine Wheelbase, Panorama Glass Roof, Adaptive LED Headlights with M Shadowline',
                'featured': True,
                'gallery': []
            },
            {
                'vin': 'W1K206004RP283910',
                'year': 2023,
                'make': 'Mercedes-Benz',
                'model': 'C-Class',
                'trim': 'C 220d AMG Line',
                'type': 'Luxury',
                'status': 'available',
                'odometer': 11200,
                'price': Decimal('6185000.00'),
                'fuel_type': 'Diesel',
                'transmission': 'Automatic',
                'drivetrain': 'RWD',
                'exterior_color': 'Selenite Grey Metallic',
                'interior_color': 'Sienna Brown & Black Nappa Leather',
                'engine': '2.0L 4-Cylinder OM654M Turbo Diesel with 48V Mild-Hybrid ISG (200 HP / 440 Nm)',
                'horsepower': 197,
                'primary_image_url': 'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=1200&q=80',
                'description': 'Referred to as the "Baby S-Class". 2023 Mercedes-Benz C 220d AMG Line with 11.9-inch portrait MBUX touchscreen, Burmester 3D surround sound system with 15 speakers, DIGITAL LIGHT projection headlights, and 48V integrated starter generator mild-hybrid boost.',
                'features': '11.9-inch Portrait MBUX Display, Burmester 3D Surround Sound (710W), DIGITAL LIGHT with Projection, AMG Body Styling & 18-inch AMG Alloys, 64-Color Ambient Lighting',
                'featured': False,
                'gallery': []
            },
            {
                'vin': 'WAUZZZFY8RP392819',
                'year': 2024,
                'make': 'Audi',
                'model': 'Q5',
                'trim': '45 TFSI Technology Quattro',
                'type': 'Luxury',
                'status': 'sold',
                'odometer': 7800,
                'price': Decimal('7080000.00'),
                'fuel_type': 'Gasoline',
                'transmission': 'Dual-Clutch',
                'drivetrain': 'AWD',
                'exterior_color': 'Navarra Blue Metallic',
                'interior_color': 'Okapi Brown Cricket Leather',
                'engine': '2.0L TFSI Turbocharged Petrol with 12V Mild-Hybrid (265 HP / 370 Nm)',
                'horsepower': 261,
                'primary_image_url': 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=1200&q=80',
                'description': 'The gold standard of luxury SUVs. 2024 Audi Q5 45 TFSI Technology with legendary Quattro all-wheel drive. 0-100 km/h in 6.1 seconds. Equipped with Audi Virtual Cockpit Plus, Matrix LED headlamps, Bang & Olufsen 3D 19-speaker audio system, and adaptive suspension damping.',
                'features': '0-100 km/h in 6.1s, Quattro All-Wheel Drive with Ultra Tech, Bang & Olufsen 3D 19-Speaker Sound (755W), Matrix LED Headlamps with Dynamic Indicators, Audi Virtual Cockpit Plus',
                'featured': False,
                'gallery': []
            },
            # Electric Vehicles (EV): Tata Nexon EV, MG ZS EV, Hyundai Ioniq 5
            {
                'vin': 'MAT614569RP482910',
                'year': 2024,
                'make': 'Tata',
                'model': 'Nexon EV',
                'trim': 'Empowered Plus LR (45 kWh)',
                'type': 'EV',
                'status': 'available',
                'odometer': 3800,
                'price': Decimal('1719000.00'),
                'fuel_type': 'Electric',
                'transmission': 'Single-Speed',
                'drivetrain': 'FWD',
                'exterior_color': 'Empowered Oxide Dual-Tone',
                'interior_color': 'Oceanic White Leatherette with Blue Stitching',
                'engine': 'Permanent Magnet Synchronous Motor (45 kWh Liquid-Cooled LFP Battery)',
                'horsepower': 143,
                'primary_image_url': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&w=1200&q=80',
                'description': "India's highest selling electric SUV. 2024 Tata Nexon EV Long Range with 45 kWh high-density battery pack delivering 489 km ARAI certified range. Features V2V (Vehicle to Vehicle) & V2L (Vehicle to Load) bi-directional charging, 12.3-inch cinematic touchscreen, and smart digital shifter.",
                'features': '489 km ARAI Certified Range, V2V & V2L Bi-Directional Power Bank Capability, 12.3-inch Harman Cinematic Screen, Arcade.ev App Suite, 360 Blind View Monitor, Paddle Regenerative Braking',
                'featured': True,
                'gallery': []
            },
            {
                'vin': 'SDZ788100RP592810',
                'year': 2024,
                'make': 'MG',
                'model': 'ZS EV',
                'trim': 'Exclusive Plus (50.3 kWh)',
                'type': 'EV',
                'status': 'available',
                'odometer': 8200,
                'price': Decimal('2448000.00'),
                'fuel_type': 'Electric',
                'transmission': 'Single-Speed',
                'drivetrain': 'FWD',
                'exterior_color': 'Glaze Red',
                'interior_color': 'Dark Grey Luxury Leatherette',
                'engine': 'PMS Motor with 50.3 kWh Prismatic High-Density Battery (176 PS / 280 Nm)',
                'horsepower': 174,
                'primary_image_url': 'https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=1200&q=80',
                'description': 'Refined global electric crossover. 2024 MG ZS EV Exclusive Plus with 50.3 kWh IP69K-certified battery pack offering 461 km range. Features dual-pane panoramic skyroof, Level 2 ADAS with 17 autonomous driving aids, PM 2.5 air purification, and Bluetooth digital key.',
                'features': '461 km Range, 0-100 km/h in 8.5s, Dual-Pane Panoramic Skyroof, Level 2 ADAS Suite (17 Features), 10.1-inch HD Touchscreen with i-SMART 2.0, PM 2.5 Air Filter, Digital Key',
                'featured': False,
                'gallery': []
            },
            {
                'vin': 'KMHF841DARP692810',
                'year': 2024,
                'make': 'Hyundai',
                'model': 'Ioniq 5',
                'trim': 'Long Range RWD (72.6 kWh)',
                'type': 'EV',
                'status': 'available',
                'odometer': 4900,
                'price': Decimal('4605000.00'),
                'fuel_type': 'Electric',
                'transmission': 'Single-Speed',
                'drivetrain': 'RWD',
                'exterior_color': 'Gravity Gold Matte',
                'interior_color': 'Dark Pebble Grey Eco-Processed Leather',
                'engine': 'Ultra-Fast 800V Architecture Motor (72.6 kWh Battery / 217 PS / 350 Nm)',
                'horsepower': 215,
                'primary_image_url': 'https://images.unsplash.com/photo-1594502184342-2e12f877aa73?auto=format&fit=crop&w=1200&q=80',
                'description': 'World Car of the Year winner. 2024 Hyundai Ioniq 5 on E-GMP 800V ultra-fast charging platform. 631 km ARAI certified range. 350 kW DC charging (10% to 80% in 18 minutes). Features relaxation seats with leg support, parametric pixel LED lighting, and Vehicle-to-Load (V2L) exterior & interior 3.6 kW output.',
                'features': '631 km ARAI Certified Range, 800V Ultra-Fast Architecture (10-80% in 18 mins), V2L Inside & Outside 3.6kW Power Output, Vision Panoramic Glass Roof, Relaxation Front Seats, Smart Sense ADAS',
                'featured': True,
                'gallery': [
                    'https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&w=1200&q=80'
                ]
            },
        ]

        for v_data in vehicles_data:
            gallery = v_data.pop('gallery', [])
            vehicle_obj, created = Vehicle.objects.update_or_create(
                vin=v_data['vin'],
                defaults=v_data
            )
            for idx, g_url in enumerate(gallery):
                VehicleImage.objects.get_or_create(
                    vehicle=vehicle_obj,
                    image_url=g_url,
                    defaults={'caption': f"Showroom View {idx+1}", 'display_order': idx}
                )

        self.stdout.write(self.style.SUCCESS(f"  [+] {len(vehicles_data)} India-market vehicles seeded."))

        # 4. Store Categories
        categories_data = [
            {'name': 'Braking Systems', 'slug': 'brakes', 'icon': 'bi-disc', 'description': 'High-performance Brembo calipers, ventilated slotted rotors, and low-dust ceramic pads.'},
            {'name': 'Exhaust & Performance', 'slug': 'exhaust', 'icon': 'bi-fire', 'description': 'Stainless steel free-flow exhausts, high-flow downpipes, and performance mufflers.'},
            {'name': 'Wheels & Tyres', 'slug': 'wheels-suspension', 'icon': 'bi-circle', 'description': 'Alloy wheel sets, Apollo/MRF/Michelin tyres, and comfort coilover suspension.'},
            {'name': 'Intake & Lubricants', 'slug': 'engine-intake', 'icon': 'bi-gear-wide-connected', 'description': 'K&N high-flow cold air filters, Bosch cabin air systems, and Motul 100% synthetic engine oils.'},
            {'name': 'Exterior & Carbon Aero', 'slug': 'aero-body', 'icon': 'bi-shield-shaded', 'description': 'Pre-preg carbon fiber boot spoilers, front splitters, and gloss rear diffusers.'},
            {'name': 'EV & Charging Solutions', 'slug': 'ev-charging', 'icon': 'bi-lightning-charge', 'description': 'Level 2 smart 7.4kW/11kW fast home wallbox chargers, Type-2 cables, and EV accessories.'},
        ]

        categories = {}
        for c_data in categories_data:
            cat_obj, _ = Category.objects.update_or_create(
                slug=c_data['slug'],
                defaults=c_data
            )
            categories[cat_obj.slug] = cat_obj
        self.stdout.write(self.style.SUCCESS(f"  [+] {len(categories)} Store categories configured."))

        # 5. Store Parts (India Market Pricing & Fitments)
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Part.objects.all().delete()
        parts_data = [
            {
                'sku': 'BRM-IN-330F',
                'name': 'Brembo GT High-Performance Front Brake Kit (330mm Rotors)',
                'category': categories['brakes'],
                'brand': 'Brembo Performance',
                'price': Decimal('48500.00'),
                'stock': 8,
                'description': 'Engineered for exceptional stopping power and thermal stability under rigorous Indian driving conditions. Monoblock 4-piston aluminum calipers with two-piece ventilated slotted disc rotors.',
                'specifications': 'Fitment: Mahindra XUV700 / Tata Safari / Hyundai Creta / Kia Seltos | Rotor: 330x28mm | Caliper Color: Acid Yellow | Pad Compound: Ferodo FM1000 Low-Dust',
                'primary_image_url': 'https://images.unsplash.com/photo-1600705722908-bab1e61c0b4d?auto=format&fit=crop&w=800&q=80',
                'featured': True,
            },
            {
                'sku': 'BSH-AERO-SET',
                'name': 'Bosch Aerotwin Beam Wiper Blade Set & Carbon Cabin Filter',
                'category': categories['engine-intake'],
                'brand': 'Bosch India',
                'price': Decimal('3450.00'),
                'stock': 25,
                'description': 'All-weather monsoon beam wiper blades paired with an active carbon HEPA cabin air filter for complete PM2.5 dust and allergen protection.',
                'specifications': 'Fitment: Hyundai Creta, Kia Seltos, Tata Nexon, Maruti Baleno | Dual-precision tensioned steel springs | Includes HEPA Activated-Carbon PM2.5 Filter',
                'primary_image_url': 'https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=800&q=80',
                'featured': False,
            },
            {
                'sku': 'APL-ASP-18SET',
                'name': 'Apollo Aspire 4G High-Performance Tyres 235/55 R18 (Set of 4)',
                'category': categories['wheels-suspension'],
                'brand': 'Apollo Tyres',
                'price': Decimal('46800.00'),
                'stock': 12,
                'description': 'High-silica tread compound providing supreme wet grip during monsoon downpours and low tyre roar on national expressways.',
                'specifications': 'Sizes: 235/55 R18 100V | Wet Grip Rating: A | Fitment: Mahindra XUV700, Hyundai Creta, Tata Harrier / Safari, MG Hector',
                'primary_image_url': 'https://images.unsplash.com/photo-1578844251758-2f71da64c96f?auto=format&fit=crop&w=800&q=80',
                'featured': True,
            },
            {
                'sku': 'MRF-PRF-16SET',
                'name': 'MRF Perfinza CLX1 Luxury Touring Tyre Set 205/55 R16 (Set of 4)',
                'category': categories['wheels-suspension'],
                'brand': 'MRF Tyres',
                'price': Decimal('32400.00'),
                'stock': 16,
                'description': 'Asymmetric luxury tread design engineered for whisper-quiet highway cruising, plush ride comfort, and high mileage longevity.',
                'specifications': 'Sizes: 205/55 R16 91V | Fitment: Honda City, Skoda Slavia, Hyundai Verna, Maruti Baleno (16-inch upgrade)',
                'primary_image_url': 'https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=800&q=80',
                'featured': False,
            },
            {
                'sku': 'MCH-PS4-19SET',
                'name': 'Michelin Pilot Sport 4 SUV Tyres 235/50 R19 (Set of 4)',
                'category': categories['wheels-suspension'],
                'brand': 'Michelin India',
                'price': Decimal('78500.00'),
                'stock': 6,
                'description': 'Ultra-high-performance SUV tyres with Dynamic Response Technology. Delivers razor-sharp steering precision and outstanding braking on wet and dry tarmac.',
                'specifications': 'Sizes: 235/50 R19 99V | Fitment: BMW 3 Series, Audi Q5, Hyundai Ioniq 5, Mercedes-Benz C-Class',
                'primary_image_url': 'https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&w=800&q=80',
                'featured': True,
            },
            {
                'sku': 'AKR-EXH-TSI15',
                'name': 'CarCraft Stainless Free-Flow Cat-Back Exhaust System',
                'category': categories['exhaust'],
                'brand': 'CarCraft Tuning',
                'price': Decimal('42500.00'),
                'stock': 5,
                'description': 'Mandrel-bent 304 aircraft-grade stainless steel exhaust system with dual carbon-finish tailpipes. Dyno-proven +8 BHP gain and a deep sporty exhaust note.',
                'specifications': 'Fitment: Skoda Slavia 1.5 TSI / Hyundai Verna 1.5 Turbo / Tata Altroz Racer | Material: 304 Stainless Steel with Carbon Tips | Dyno Gain: +8 BHP',
                'primary_image_url': 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=800&q=80',
                'featured': True,
            },
            {
                'sku': 'KW-ST-COMFORT',
                'name': 'KW Suspension Street Comfort Adjustable Coilover Kit',
                'category': categories['wheels-suspension'],
                'brand': 'KW Automotive',
                'price': Decimal('145000.00'),
                'stock': 4,
                'description': 'Stainless steel coilover kit with rebound damping adjustability specifically tuned to absorb uneven Indian road surfaces while maintaining precise high-speed composure.',
                'specifications': 'Fitment: BMW 3 Series (G20/G28) / Skoda Slavia / Audi Q5 | Lowering Range: 15-35mm | Rebound Valve Adjustment: 16 clicks',
                'primary_image_url': 'https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=800&q=80',
                'featured': False,
            },
            {
                'sku': 'KN-INT-VRNA15',
                'name': 'K&N High-Flow Cold Air Intake Induction Kit',
                'category': categories['engine-intake'],
                'brand': 'K&N Engineering',
                'price': Decimal('18900.00'),
                'stock': 15,
                'description': 'Washable oiled cotton gauze high-flow induction system with heat shield. Enhances turbocharger spool acoustic feedback and delivers up to +6 BHP power increase.',
                'specifications': 'Fitment: Hyundai Verna 1.5 Turbo / Creta 1.5 Turbo / Kia Seltos Turbo | Filter: Washable Lifetime Cotton | Power Gain: +6 BHP / +8 Nm',
                'primary_image_url': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80',
                'featured': True,
            },
            {
                'sku': 'CC-EV-WB74',
                'name': 'CarCraft Pro Series 7.4kW / 32A Smart Home EV Fast Wallbox Charger',
                'category': categories['ev-charging'],
                'brand': 'CarCraft EV Labs India',
                'price': Decimal('38500.00'),
                'stock': 20,
                'description': 'Commercial-grade residential AC fast charger. 7.4 kW / 32A single-phase output providing up to 45 km of range per hour of charge. Equipped with Type-2 universal gun, RFID card access, WiFi smart app, and IP65 weatherproof enclosure.',
                'specifications': 'Output: 7.4 kW / 32A (230V AC Single Phase) | Connector: Type-2 Gun with 5m Ultra-Flexible Cable | Protection: IP65 Outdoor Weatherproof, Residual Current Detection | Smart Tech: RFID, WiFi, OCPP 1.6J',
                'primary_image_url': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&w=800&q=80',
                'featured': True,
            },
            {
                'sku': 'MOT-8100-5L',
                'name': 'Motul 8100 X-cess Gen2 100% Synthetic 5W-40 Motor Oil (5L Combo)',
                'category': categories['engine-intake'],
                'brand': 'Motul India',
                'price': Decimal('4850.00'),
                'stock': 45,
                'description': '100% synthetic high-performance engine lubricant formulated with advanced additive technology for severe heat conditions in Indian summer stop-and-go traffic.',
                'specifications': 'Viscosity: 5W-40 | Volume: 5 Liters (4L + 1L) | Approvals: API SP, ACEA A3/B4, BMW LL-01, MB 229.5, Porsche A40, VW 502 00 / 505 00',
                'primary_image_url': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80',
                'featured': False,
            },
            {
                'sku': 'BBS-SR-18SET',
                'name': 'BBS SR Satin Himalaya Grey 18-inch Alloy Wheel Set (Set of 4)',
                'category': categories['wheels-suspension'],
                'brand': 'BBS Germany',
                'price': Decimal('138000.00'),
                'stock': 3,
                'description': 'German engineered one-piece low-pressure cast alloy wheels with distinctive soft radius spokes and durable winter/monsoon-proof powder coating.',
                'specifications': 'Fitment: BMW 3 Series / Skoda Slavia / Audi Q5 | Specs: 18x8.0J PCD 5x112 ET45 | Finish: Satin Himalaya Grey | Certified: TÜV Rheinland Approved',
                'primary_image_url': 'https://images.unsplash.com/photo-1578844251758-2f71da64c96f?auto=format&fit=crop&w=800&q=80',
                'featured': True,
            },
            {
                'sku': 'CC-AERO-SEDAN',
                'name': 'CarCraft Carbon Aero Boot Lip Spoiler & Gloss Diffuser Set',
                'category': categories['aero-body'],
                'brand': 'CarCraft Aero Labs',
                'price': Decimal('24500.00'),
                'stock': 8,
                'description': '3K twill-weave real carbon fiber boot spoiler and aerodynamic gloss rear diffuser combo for executive sedans.',
                'specifications': 'Fitment: Skoda Slavia / Hyundai Verna / Honda City / BMW 3 Series | Material: Real Carbon Fiber + ABS Composite | Mount: 3M Automotive VHB Tape & Screws Included',
                'primary_image_url': 'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80',
                'featured': False,
            },
        ]

        for p_data in parts_data:
            Part.objects.update_or_create(
                sku=p_data['sku'],
                defaults=p_data
            )
        self.stdout.write(self.style.SUCCESS(f"  [+] {len(parts_data)} High-performance parts seeded."))

        # 6. Service Appointments (Today + Upcoming Days with Indian Customers)
        today = timezone.now().date()
        tomorrow = today + datetime.timedelta(days=1)
        day_after = today + datetime.timedelta(days=2)

        appointments_data = [
            # Today's appointments
            {
                'customer_name': 'Rahul Sharma',
                'customer_email': 'rahul.sharma@techcorp.in',
                'customer_phone': '+91 98201 23456',
                'vehicle_description': '2024 Mahindra XUV700 AX7 L AWD',
                'vehicle_vin': 'MA1XU7000RP891234',
                'vehicle_odometer': 12800,
                'service_type': 'brake_performance',
                'date': today,
                'time_slot': '08:00',
                'assigned_bay': bays[1],
                'status': 'completed',
                'notes': 'Upgrade front brake pads to Brembo low-dust ceramic pads and bleed fresh DOT 4 brake fluid before Mumbai-Goa expressway trip.',
                'internal_notes': 'Front disc thickness measured at 27.9mm (well within tolerance). Brembo pads bedded in. Brake pressure 125 bar solid.',
                'estimated_cost': Decimal('12500.00'),
            },
            {
                'customer_name': 'Pooja Deshmukh',
                'customer_email': 'pooja.d@greenmobility.org',
                'customer_phone': '+91 98112 34567',
                'vehicle_description': '2024 Tata Nexon EV Empowered Plus LR',
                'vehicle_vin': 'MAT614569RP482910',
                'vehicle_odometer': 3800,
                'service_type': 'ev_battery_health',
                'date': today,
                'time_slot': '08:00',
                'assigned_bay': bays[4],
                'status': 'in_progress',
                'notes': '45 kWh high-voltage battery cell balance check and coolant thermal management loop inspection.',
                'internal_notes': 'Connected high-voltage diagnostic tablet. Cell voltage variance 3mV (optimum). Glycol loop pressure 1.3 bar holding steady.',
                'estimated_cost': Decimal('4200.00'),
            },
            {
                'customer_name': 'Aditya Singhania',
                'customer_email': 'aditya.s@capitalventures.in',
                'customer_phone': '+91 98450 12345',
                'vehicle_description': '2024 BMW 3 Series Gran Limousine 330Li',
                'vehicle_vin': 'WBA330L00RP194820',
                'vehicle_odometer': 5400,
                'service_type': 'performance_tune',
                'date': today,
                'time_slot': '09:30',
                'assigned_bay': bays[1],
                'status': 'in_progress',
                'notes': 'ECU Stage 1 calibration with baseline dyno run and high-flow air intake fitment.',
                'internal_notes': 'Baseline run: 254 BHP / 398 Nm. Stage 1 map flashed. Post-run: 295 BHP / 460 Nm (+41 BHP).',
                'estimated_cost': Decimal('18500.00'),
            },
            {
                'customer_name': 'Ananya Iyer',
                'customer_email': 'ananya.iyer@designstudio.in',
                'customer_phone': '+91 98230 98765',
                'vehicle_description': '2024 Honda City ZX e:HEV Hybrid',
                'vehicle_vin': 'MAKGM6680RP394821',
                'vehicle_odometer': 11500,
                'service_type': 'oil_synthetic',
                'date': today,
                'time_slot': '09:30',
                'assigned_bay': bays[3],
                'status': 'scheduled',
                'notes': '10,000 km periodic maintenance service. Motul 0W-20 Full Synthetic Oil + OEM Honda oil filter replacement.',
                'internal_notes': '',
                'estimated_cost': Decimal('4500.00'),
            },
            {
                'customer_name': 'Vikram Malhotra',
                'customer_email': 'vmalhotra@fintechgroup.co.in',
                'customer_phone': '+91 98901 23456',
                'vehicle_description': '2024 Hyundai Creta SX (O) 1.5 Turbo DCT',
                'vehicle_vin': 'MALH581CLRP692810',
                'vehicle_odometer': 7500,
                'service_type': 'tire_alignment',
                'date': today,
                'time_slot': '11:00',
                'assigned_bay': bays[2],
                'status': 'scheduled',
                'notes': 'Hunter 3D laser 4-wheel alignment and high-speed wheel balancing after tyre rotation.',
                'internal_notes': '',
                'estimated_cost': Decimal('3200.00'),
            },
            {
                'customer_name': 'Neha Verma',
                'customer_email': 'neha.verma@consulting.in',
                'customer_phone': '+91 97170 54321',
                'vehicle_description': '2023 Mercedes-Benz C-Class C 220d AMG Line',
                'vehicle_vin': 'W1K206004RP283910',
                'vehicle_odometer': 11200,
                'service_type': 'transmission_flush',
                'date': today,
                'time_slot': '13:00',
                'assigned_bay': bays[3],
                'status': 'scheduled',
                'notes': '9G-TRONIC transmission fluid inspection and rear axle differential lube top-up.',
                'internal_notes': '',
                'estimated_cost': Decimal('8900.00'),
            },
            {
                'customer_name': 'Rohan Kulkarni',
                'customer_email': 'rohan.k@logisticsindia.com',
                'customer_phone': '+91 98220 11223',
                'vehicle_description': '2024 Hyundai Ioniq 5 Long Range RWD',
                'vehicle_vin': 'KMHF841DARP692810',
                'vehicle_odometer': 4900,
                'service_type': 'multi_point_inspection',
                'date': today,
                'time_slot': '14:30',
                'assigned_bay': bays[4],
                'status': 'scheduled',
                'notes': '50-Point Certified monsoon safety inspection and V2L discharge circuit verification.',
                'internal_notes': '',
                'estimated_cost': Decimal('2500.00'),
            },
            # Tomorrow's appointments
            {
                'customer_name': 'Sneha Rao',
                'customer_email': 'sneha.rao@biotech.ac.in',
                'customer_phone': '+91 98800 44556',
                'vehicle_description': '2024 Maruti Suzuki Baleno Alpha MT',
                'vehicle_vin': 'MA3EWB1S0RP104921',
                'vehicle_odometer': 6400,
                'service_type': 'multi_point_inspection',
                'date': tomorrow,
                'time_slot': '08:00',
                'assigned_bay': bays[2],
                'status': 'scheduled',
                'notes': 'Pre-monsoon underbody coating inspection and wiper replacement.',
                'internal_notes': '',
                'estimated_cost': Decimal('2500.00'),
            },
            {
                'customer_name': 'Karan Banerjee',
                'customer_email': 'karan.b@mediaworks.in',
                'customer_phone': '+91 98300 77889',
                'vehicle_description': '2023 Skoda Slavia 1.5 TSI Monte Carlo',
                'vehicle_vin': 'TMBNA2AA8RP583921',
                'vehicle_odometer': 14200,
                'service_type': 'brake_performance',
                'date': tomorrow,
                'time_slot': '09:30',
                'assigned_bay': bays[1],
                'status': 'scheduled',
                'notes': 'Brake disc rotor thickness check and performance brake pad replacement.',
                'internal_notes': '',
                'estimated_cost': Decimal('12500.00'),
            },
            {
                'customer_name': 'Suresh Patel',
                'customer_email': 'suresh.patel@patelinfra.in',
                'customer_phone': '+91 98250 99887',
                'vehicle_description': '2024 Tata Nexon Fearless+ S Diesel',
                'vehicle_vin': 'MAT613459RP782914',
                'vehicle_odometer': 9200,
                'service_type': 'oil_synthetic',
                'date': tomorrow,
                'time_slot': '11:00',
                'assigned_bay': bays[3],
                'status': 'scheduled',
                'notes': '10,000 km oil service. Motul 5W-40 Synthetic + Fuel Filter replacement.',
                'internal_notes': '',
                'estimated_cost': Decimal('4500.00'),
            },
            # Day after tomorrow
            {
                'customer_name': 'Meera Nambiar',
                'customer_email': 'meera.nambiar@heritagefoods.in',
                'customer_phone': '+91 98470 66778',
                'vehicle_description': '2024 Hyundai Verna SX (O) 1.5 Turbo DCT',
                'vehicle_vin': 'MALC451CLRP493820',
                'vehicle_odometer': 8800,
                'service_type': 'performance_tune',
                'date': day_after,
                'time_slot': '08:00',
                'assigned_bay': bays[1],
                'status': 'scheduled',
                'notes': 'Stage 1 ECU throttle response optimization and launch control calibration.',
                'internal_notes': '',
                'estimated_cost': Decimal('18500.00'),
            },
        ]

        Appointment.objects.all().delete()  # Fresh demo schedule
        for appt_data in appointments_data:
            appt = Appointment(**appt_data)
            appt.save()
        self.stdout.write(self.style.SUCCESS(f"  [+] {len(appointments_data)} Service appointments seeded across schedule."))

        # 7. Demo Orders
        Order.objects.all().delete()
        order1 = Order.objects.create(
            order_number='CC-MUM0184',
            customer_name='Aarav Mehta',
            customer_email='aarav.mehta@example.in',
            customer_phone='+91 98201 55500',
            shipping_address='Flat 502, Sea Breeze Residency, Bandra West',
            city='Mumbai',
            state='Maharashtra',
            postal_code='400050',
            total_amount=Decimal('61242.00'),  # (48500 + 3450) * 1.18 = 61242.00 + Free shipping
            status='paid',
            payment_method='UPI (Google Pay / Instant Authorization)',
            notes='Deliver to security desk with OTP confirmation.'
        )
        part_brakes = Part.objects.get(sku='BRM-IN-330F')
        part_wipers = Part.objects.get(sku='BSH-AERO-SET')
        OrderItem.objects.create(
            order=order1,
            part=part_brakes,
            part_name=part_brakes.name,
            part_sku=part_brakes.sku,
            price=part_brakes.price,
            quantity=1
        )
        OrderItem.objects.create(
            order=order1,
            part=part_wipers,
            part_name=part_wipers.name,
            part_sku=part_wipers.sku,
            price=part_wipers.price,
            quantity=1
        )
        self.stdout.write(self.style.SUCCESS("  [+] Demo Order #CC-MUM0184 created."))

        self.stdout.write(self.style.SUCCESS("🎉 CarCraft India database seeding completed successfully!"))
