#######################################################################################################################
"""
Static data for cat breeds in backend.

Defines the CAT_BREEDS tuple and the ensure_cat_breeds utility for populating the database with standard breeds.
"""

#######################################################################################################################
# Imports
#######################################################################################################################

from sqlmodel import select

from database.core.models import Breed, Species

#######################################################################################################################
# Globals
#######################################################################################################################

CAT_BREEDS = (
    "Abyssinian",
    "American Bobtail",
    "American Curl",
    "American Shorthair",
    "American Wirehair",
    "Balinese",
    "Bengal",
    "Birman",
    "Bombay",
    "British Longhair",
    "British Shorthair",
    "Burmese",
    "Burmilla",
    "Chartreux",
    "Cornish Rex",
    "Devon Rex",
    "Egyptian Mau",
    "European Burmese",
    "Exotic Shorthair",
    "Havana Brown",
    "Himalayan",
    "Japanese Bobtail",
    "Korat",
    "LaPerm",
    "Maine Coon",
    "Manx",
    "Norwegian Forest Cat",
    "Ocicat",
    "Oriental",
    "Persian",
    "Ragdoll",
    "Russian Blue",
    "Scottish Fold",
    "Selkirk Rex",
    "Siamese",
    "Siberian",
    "Singapura",
    "Snowshoe",
    "Somali",
    "Sphynx",
    "Tonkinese",
    "Turkish Angora",
    "Turkish Van",
    "Other",
    "Unknown",
)

#######################################################################################################################
# Body
#######################################################################################################################


def ensure_cat_breeds(session):
    """Ensure all standard cat breeds exist in the database for the Feline species."""
    existing = set(name for name in session.exec(select(Breed.name).where(Breed.species == Species.FELINE)).all())
    to_add = [Breed(name=cat, species=Species.FELINE) for cat in CAT_BREEDS if cat not in existing]
    if to_add:
        session.add_all(to_add)
        session.commit()


#######################################################################################################################
# End of file
#######################################################################################################################
