#######################################################################################################################
"""
Static data for horse breeds in backend.

Defines the HORSE_BREEDS tuple and the ensure_horse_breeds utility for populating the database with standard breeds.
"""

#######################################################################################################################
# Imports
#######################################################################################################################

from sqlmodel import select

from database.core.models import Breed, Species

#######################################################################################################################
# Globals
#######################################################################################################################

HORSE_BREEDS = (
    "Akhal-Teke",
    "American Paint Horse",
    "American Quarter Horse",
    "Andalusian",
    "Appaloosa",
    "Arabian",
    "Belgian",
    "Clydesdale",
    "Dutch Warmblood",
    "Exmoor Pony",
    "Friesian",
    "Gypsy Vanner",
    "Hanoverian",
    "Holsteiner",
    "Icelandic Horse",
    "Irish Draught",
    "Lipizzaner",
    "Miniature Horse",
    "Morgan",
    "Mustang",
    "Oldenburg",
    "Percheron",
    "Peruvian Paso",
    "Pony of the Americas",
    "Shetland Pony",
    "Shire",
    "Standardbred",
    "Tennessee Walking Horse",
    "Thoroughbred",
    "Trakehner",
    "Welsh Pony",
    "Other",
    "Unknown",
)

#######################################################################################################################
# Body
#######################################################################################################################


def ensure_horse_breeds(session):
    """Ensure all standard horse breeds exist in the database for the Equine species."""
    existing = set(name for name in session.exec(select(Breed.name).where(Breed.species == Species.EQUINE)).all())
    to_add = [Breed(name=horse, species=Species.EQUINE) for horse in HORSE_BREEDS if horse not in existing]
    if to_add:
        session.add_all(to_add)
        session.commit()


#######################################################################################################################
# End of file
#######################################################################################################################
