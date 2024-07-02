#!/bin/bash

# Lancer Docker Compose
echo "Lancement de Docker Compose..."
docker-compose up -d

# Attendre que les conteneurs soient prêts
echo "Attente que les conteneurs soient prêts..."
sleep 10

# Lancer le producteur
echo "Lancement du producteur..."
python financial_data_producer.py &
sleep 5

# Lancer le consommateur simple
echo "Lancement du consommateur..."
python financial_data_consumer.py &
sleep 5

# Lancer le consommateur vers MongoDB
echo "Lancement du consommateur vers MongoDB..."
python consumer_to_mongodb.py &