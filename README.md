# 🇬🇭 Easy Eats
### An Intelligent Ghanaian Breakfast Recommendation Engine

Inspired by Chef Eric Adjepong's award-winning cookbook ***Ghana to the World*** (with Korsha Wilson), this web application eliminates morning decision fatigue by intelligently matching users to authentic Ghanaian breakfast options based on their **exact budget in Ghana Cedis (GH₵)**, **available preparation time**, and **flavor/mood cravings**.

---

## 🌟 Key Features

1. **Dynamic Numeric Budget Entry in Ghana Cedis (GH₵)**
   - No rigid tiers or arbitrary brackets (`$`, `$$`). Users enter their exact available money (e.g. `GH₵ 35.00`, `GH₵ 50.00`, `GH₵ 120.00`).
   - Servings scaling (1 person, 2 people, 4 people) with instant cost recalculations.
   - Calculates and displays exact **budget surplus** (e.g., *"Costs GH₵ 25.00 — leaves GH₵ 15.00 in your pocket"*).
   - **Smart Fallback Engine**: If a user enters an amount under the lowest cost item (e.g., `GH₵ 10.00`), the app surfaces the closest affordable Ghanaian morning staple just a few Cedis away.

2. **Multi-Factor Recommendation Engine**
   - Deterministic affinity scoring (0 to 100 points) balancing budget efficiency (40%), time fit (30%), flavor mood (20%), and cultural heritage alignment (10%).
   - Transparent "Why we chose this for you" reasoning badges on every recommendation.
   - Displays a primary **Hero Card** plus runner-up alternative choices.

3. **Comprehensive 40-Recipe Ghanaian Breakfast Catalog**
   - **Porridges & Warm Bowls**: Ablemamu (Tom Brown), Hausa Koko with Koose, Oblayo with Coconut, Rice Porridge, Spiced Fonio with Coconut, Ghanaian Oats with Groundnuts, Mpampa, Tapioca, Farina, Akple Koko.
   - **Breads, Sandwiches & Bakes**: Chibom (Egg Sandwich), Crusty Tea Bread with Blue Band & Sardines, Sugar Bread with Eggs & Milo, Bofrot (Nutmeg Puff-Puff), Pinkaso, Tatale (Plantain Pancakes), Meat Pie, Cassava Pancakes with Malted Crumble, Biscuits with Guava Thyme Jam.
   - **Hearty Sustenance & Beans**: Gob3 (Red Red / Beans & Gari with Plantain), Traditional Waakye Morning Plate, Ga Kenkey with Fried Fish & Shito, Ampesi (Boiled Yam with Kontomire Stew), Boiled Sweet Potatoes with Sardine & Egg Sauce, Fried Puna Yam with Chofi & Shito, Boiled Yam with Garden Egg Stew, Fried Plantains with Corned Beef Stew, Tubani (Steamed Bean Pudding).
   - **Morning Drinks & Beverages**: Steamed Hot Milo, Spiced Ghanaian Black Tea, Brukina (Millet & Yogurt Smoothie), Asana (Caramelized Fermented Corn Drink), Atadwe Milk (Tigernut Pudding).
   - **Proteins & Weekend Brunch Feasts**: Koose, Kelewele & Peanuts, Fried Wagashi with Suya, Roasted Banana Grits with Shrimp, Eggs Benedict with Scallops & Piri Piri, Apapransa with Crab.

4. **Minimalist Aesthetic with Orange Highlights**
   - Styled with **Tailwind CSS**.
   - Generous white space, crisp typography (`font-serif` titles, clean sans body), and energetic Ghanaian Sunset Orange (`orange-600` / `#EA580C`) focus rings, badges, and CTAs.
   - Interactive cooking checklist with strike-through scratch-off animations.
   - Timers attached to preparation steps.

5. **Integrated Django Admin (`/admin/`)**
   - Manage, add, edit, and delete recipes, ingredients, and steps.
   - Single-point ingredient market price updates: update the price of eggs or milk in Accra and linked recipe costs recalculate automatically.

---

## 🛠 Tech Stack

- **Backend**: Python 3.11+ / Django 5.x
- **Database**: PostgreSQL 16 (in Docker) with automatic local SQLite fallback
- **Frontend**: Django Templates + Tailwind CSS (via CDN)
- **Containerization**: Docker & Docker Compose

---

## 🚀 Quickstart with Docker Compose

### Prerequisites
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

### 1. Clone & Run
```bash
docker compose up --build
```

The application will:
1. Spin up the PostgreSQL 16 container (`easybreakfast_db`).
2. Run database healthchecks.
3. Apply Django migrations.
4. Automatically seed the 10 Ghanaian breakfast recipes with Ghana Cedis pricing.
5. Launch the web server at **http://localhost:8000/**.

---

## 💻 Running Locally (Without Docker)

If running outside Docker:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations (defaults to SQLite if PostgreSQL is not active)
python manage.py migrate

# 3. Seed the breakfast catalog
python manage.py seed_recipes

# 4. Start the development server
python manage.py runserver
```

Open your browser to:
- **Web App**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Recipe Catalog**: [http://127.0.0.1:8000/recipes/](http://127.0.0.1:8000/recipes/)
- **Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔐 Admin Credentials

Default superuser credentials created for local development and testing:
- **Username**: `admin`
- **Password**: `admin1234`

To create another superuser:
```bash
python manage.py createsuperuser
# Or inside docker:
docker compose exec web python manage.py createsuperuser
```

---

## 🧪 Running Automated Tests

```bash
python manage.py test
```
All unit tests verify:
- Budget numeric filtering and strict ceiling checks.
- Low-budget fallback advice generation.
- Template rendering for home, results, recipe detail, and catalog.
- Multi-factor recommendation scoring.

---

## 🚢 Deploying to Dokploy

This repository is pre-configured for direct deployment on **Dokploy** via Dockerfile or Docker Compose.

### Recommended: Deploy via Dokploy Application (Dockerfile)
1. **Create a Database**:
   - In Dokploy, go to **Databases** → **New Database** → Select **PostgreSQL 16**.
   - Copy the internal connection string (e.g. `postgres://user:pass@postgres:5432/db`).
2. **Create an Application**:
   - Go to **Applications** → **New Application**.
   - Connect your GitHub repository.
   - Build Type: **Dockerfile**.
3. **Configure Environment Variables**:
   In the **Environment** tab of your Dokploy application, provide:
   ```env
   DEBUG=False
   SECRET_KEY=generate-a-strong-random-key-here
   ALLOWED_HOSTS=yourdomain.com,*.yourdomain.com,web,localhost
   CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://easyeats.yourdomain.com
   DATABASE_URL=postgres://user:pass@postgres:5432/db
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_PASSWORD=secure-password-here
   DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
   ```
4. **Ports**:
   - Under **General** / **Network**, set Container Port to `8000`.
   - Traefik automatically provisions and manages free Let's Encrypt SSL certificates for your domain.
5. **Deploy**:
   - Click **Deploy**. The `entrypoint.sh` automatically runs database migrations, seeds the 40 breakfast recipes, collects static files via WhiteNoise, and starts Gunicorn with 3 workers.
