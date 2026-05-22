FROM python:3.10-slim

# 1) Dépendances système nécessaires pour requirements Odoo (lxml, Pillow, ldap, psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    python3-dev \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libldap2-dev \
    libsasl2-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 2) Upgrade tooling pip
RUN python -m pip install --upgrade pip setuptools wheel

# 3) Récupérer Odoo 19 (shallow clone pour éviter un clone trop lourd)
WORKDIR /odoo
RUN git clone --depth 1 https://github.com/odoo/odoo.git -b 19.0

# 4) Installer requirements Python d'Odoo
WORKDIR /odoo/odoo
RUN pip install --no-cache-dir -r requirements.txt

# 5) Lancer Odoo
CMD ["python", "odoo-bin"]
