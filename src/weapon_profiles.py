# src/weapon_profiles.py
from config import WEAPON_PROFILES, WEAPON_LIST

def get_weapon_profile(weapon_name: str):
    return WEAPON_PROFILES.get(weapon_name.upper(), WEAPON_PROFILES.get("M416"))

def get_all_weapons():
    return WEAPON_LIST
