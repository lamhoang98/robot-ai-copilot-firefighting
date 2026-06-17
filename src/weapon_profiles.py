WEAPON_PROFILES = {
    "M416": {"type": "AR", "damage": 41, "fire_rate": 6.5, "recoil": {"h": 0.12, "v": 0.25}},
    "AK47": {"type": "AR", "damage": 49, "fire_rate": 6.2, "recoil": {"h": 0.18, "v": 0.32}},
    "Beryl M762": {"type": "AR", "damage": 47, "fire_rate": 6.0, "recoil": {"h": 0.15, "v": 0.28}},
    "AUG": {"type": "AR", "damage": 41, "fire_rate": 7.5, "recoil": {"h": 0.10, "v": 0.22}},
    "SCAR-L": {"type": "AR", "damage": 42, "fire_rate": 6.5, "recoil": {"h": 0.11, "v": 0.23}},
    "Groza": {"type": "AR", "damage": 51, "fire_rate": 7.5, "recoil": {"h": 0.14, "v": 0.26}},
    "FAMAS": {"type": "AR", "damage": 39, "fire_rate": 8.0, "recoil": {"h": 0.13, "v": 0.24}},
    "MK12": {"type": "DMR", "damage": 62, "fire_rate": 3.5, "recoil": {"h": 0.08, "v": 0.35}},
    "ACE32": {"type": "DMR", "damage": 56, "fire_rate": 3.8, "recoil": {"h": 0.10, "v": 0.32}},
    "SLR": {"type": "DMR", "damage": 66, "fire_rate": 3.0, "recoil": {"h": 0.12, "v": 0.40}},
    "Dragunov": {"type": "Sniper", "damage": 79, "fire_rate": 2.0, "recoil": {"h": 0.15, "v": 0.45}},
    "Mini 14": {"type": "Sniper", "damage": 60, "fire_rate": 4.0, "recoil": {"h": 0.08, "v": 0.38}},
}

def get_weapon_profile(name):
    return WEAPON_PROFILES.get(name)
