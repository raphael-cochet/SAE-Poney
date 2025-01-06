import click
import yaml
from datetime import datetime
from .app import app, db
from .models import Client, Cotisation, Moniteur, Cours, CoursRealise, Poney, Reserver
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data(data, model, unique_keys, transform_keys=None):
    """Helper function to load data into the database, avoiding duplicates."""
    for entry in data:
        # Validate required keys
        missing_keys = [key for key in unique_keys if key not in entry]
        if missing_keys:
            logger.warning(f"Skipping {model.__tablename__}: Missing keys {missing_keys} in entry {entry}")
            continue

        # Apply transformations if needed
        if transform_keys:
            for key, func in transform_keys.items():
                if key in entry:
                    try:
                        entry[key] = func(entry[key])
                    except Exception as e:
                        logger.warning(f"Error transforming key '{key}' in entry {entry}: {e}")
                        continue

        # Check for existing record
        filter_conditions = {key: entry[key] for key in unique_keys}
        existing = model.query.filter_by(**filter_conditions).first()
        if existing is None:
            db.session.add(model(**entry))
        else:
            logger.info(f"{model.__tablename__.capitalize()} {entry} already exists.")


@app.cli.command()
@click.argument("filename")
def loaddb(filename):
    """Creates the tables and populates them with data from a YAML file, avoiding duplicates."""
    db.create_all()

    try:
        with open(filename, "r") as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        logger.error(f"Error loading YAML file: {e}")
        return
    except FileNotFoundError:
        logger.error(f"File {filename} not found.")
        return

    # Insert data into tables
    load_data(
        data.get("cotisations", []),
        Cotisation,
        ["idCotisation"],
        transform_keys={"dateRegCoti": lambda x: datetime.strptime(x, '%Y-%m-%d').date()},
    )
    # Other load_data calls...

    # Insert data into tables
    load_data(data.get("clients", []), Client, ["mail"])
    load_data(data.get("moniteurs", []), Moniteur, ["mail"])
    load_data(
        data.get("cours", []),
        Cours,
        ["idCours"],
        transform_keys={
            "jourCours": lambda x: datetime.strptime(x, '%Y-%m-%d').date(),
            "heureCours": lambda x: datetime.strptime(x, '%H:%M:%S').time()
        },
    )
    load_data(
        data.get("cours_realises", []),
        CoursRealise,
        ["idCours", "dateCours"],
        transform_keys={"dateCours": lambda x: datetime.strptime(x, '%Y-%m-%d').date()},
    )
    load_data(data.get("poneys", []), Poney, ["idPoney"])
    load_data(
        data.get("reservations", []),
        Reserver,
        ["idCours", "dateCours", "idPoney", "idCl"],
        transform_keys={"dateCours": lambda x: datetime.strptime(x, '%Y-%m-%d').date()},
    )

    db.session.commit()
    logger.info("Database successfully populated from YAML file.")



@app.cli.command()
def syncdb():
    """Creates all missing tables."""
    db.create_all()
    logger.info("All tables created successfully.")

@app.cli.command()
def dropdb():
    """Drops all tables."""
    db.drop_all()
    logger.info("All tables dropped successfully.")
