# Graph Report - HCL_Project  (2026-09-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 329 nodes · 659 edges · 19 communities (13 shown, 6 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 74 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `47349f03`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- store/views.py
- Appointment
- Vehicle
- Cart
- django_db
- settings.py
- store/admin.py
- seed_carcraft.py
- django_apps
- carcraft_tags.py
- carcraft/urls.py
- service/admin.py
- carcraft/__init__.py
- HomeDashboardTests

## God Nodes (most connected - your core abstractions)
1. `Cart` - 31 edges
2. `Vehicle` - 29 edges
3. `Appointment` - 27 edges
4. `Part` - 25 edges
5. `Category` - 15 edges
6. `Order` - 15 edges
7. `get_active_bays()` - 15 edges
8. `ServiceBay` - 12 edges
9. `StoreAndCartTests` - 11 edges
10. `Command` - 11 edges

## Surprising Connections (you probably didn't know these)
- `HomeDashboardTests` --uses--> `Category`  [INFERRED]
  carcraft/tests.py → store/models.py
- `HomeDashboardView` --uses--> `Category`  [INFERRED]
  carcraft/views.py → store/models.py
- `Command` --uses--> `Category`  [INFERRED]
  inventory/management/commands/seed_carcraft.py → store/models.py
- `Command` --uses--> `Order`  [INFERRED]
  inventory/management/commands/seed_carcraft.py → store/models.py
- `Command` --uses--> `OrderItem`  [INFERRED]
  inventory/management/commands/seed_carcraft.py → store/models.py

## Import Cycles
- None detected.

## Communities (19 total, 6 thin omitted)

### Community 0 - "store/views.py"
Cohesion: 0.06
Nodes (37): decimal, django_contrib_sessions_middleware, django_test, django_urls, AddToCartForm, CheckoutForm, Meta, PartFilterForm (+29 more)

### Community 1 - "Appointment"
Cohesion: 0.07
Nodes (34): datetime, django_core_exceptions, django_utils, AppointmentBookingForm, AppointmentStatusForm, Meta, Appointment, Meta (+26 more)

### Community 2 - "Vehicle"
Cohesion: 0.06
Nodes (26): DeleteView, django_db_models, django_http, django_shortcuts, django_views_generic, Meta, VehicleFilterForm, VehicleForm (+18 more)

### Community 3 - "Cart"
Cohesion: 0.15
Nodes (7): Cart, cart_context(), CartDetailView, TemplateView, View, RemoveFromCartView, UpdateCartView

### Community 4 - "django_db"
Cohesion: 0.11
Nodes (12): django_core_validators, django_db, django_db_models_deletion, Migration, Migration, Migration, Migration, Migration (+4 more)

### Community 5 - "settings.py"
Cohesion: 0.12
Nodes (13): ASGI config for carcraft project. It exposes the ASGI callable as a module-…, Django settings for CarCraft Dealership Suite., WSGI config for carcraft project. It exposes the WSGI callable as a module-…, django_contrib_messages, django_core_asgi, django_core_wsgi, dotenv, main() (+5 more)

### Community 6 - "store/admin.py"
Cohesion: 0.17
Nodes (11): django_contrib, action, register, VehicleAdmin, VehicleImageAdmin, VehicleImageInline, CategoryAdmin, OrderAdmin (+3 more)

### Community 7 - "seed_carcraft.py"
Cohesion: 0.22
Nodes (6): BaseCommand, django_contrib_auth, django_core_management_base, Command, Meta, VehicleImage

### Community 8 - "django_apps"
Cohesion: 0.20
Nodes (7): django_apps, InventoryConfig, AppConfig, AppConfig, ServiceConfig, AppConfig, StoreConfig

### Community 9 - "carcraft_tags.py"
Cohesion: 0.31
Nodes (8): django, filter, format_indian_number(), indian_number_filter(), inr_filter(), Format value as Indian Rupee string: e.g. ₹24,50,000, Format a number with Indian comma grouping without currency symbol., Format a number in Indian numbering system: e.g. 1000 -> 1,000 100000 ->…

### Community 10 - "carcraft/urls.py"
Cohesion: 0.25
Nodes (6): URL configuration for CarCraft Dealership Suite., HomeDashboardView, TemplateView, django_conf, django_conf_urls_static, django_contrib_staticfiles_urls

### Community 11 - "service/admin.py"
Cohesion: 0.36
Nodes (4): AppointmentAdmin, action, register, ServiceBayAdmin

### Community 12 - "carcraft/__init__.py"
Cohesion: 0.40
Nodes (3): CarCraft Dealership Suite Initialization: setup PyMySQL as MySQLdb…, django_template_context, pymysql

## Knowledge Gaps
- **10 isolated node(s):** `Meta`, `Migration`, `Migration`, `Migration`, `Migration` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 128 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Vehicle` connect `Vehicle` to `store/views.py`, `store/admin.py`, `seed_carcraft.py`, `carcraft/urls.py`, `HomeDashboardTests`?**
  _High betweenness centrality (0.139) - this node is a cross-community bridge._
- **Why does `Part` connect `store/views.py` to `Vehicle`, `Cart`, `store/admin.py`, `seed_carcraft.py`, `carcraft/urls.py`, `HomeDashboardTests`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Why does `Appointment` connect `Appointment` to `service/admin.py`, `Vehicle`, `carcraft/urls.py`, `seed_carcraft.py`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Cart` (e.g. with `Part` and `StoreAndCartTests`) actually correct?**
  _`Cart` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `Vehicle` (e.g. with `HomeDashboardTests` and `HomeDashboardView`) actually correct?**
  _`Vehicle` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Appointment` (e.g. with `HomeDashboardView` and `Command`) actually correct?**
  _`Appointment` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Part` (e.g. with `HomeDashboardTests` and `HomeDashboardView`) actually correct?**
  _`Part` has 11 INFERRED edges - model-reasoned connections that need verification._