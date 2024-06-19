import os
import math
import struct

SRTM_DICT = {'SRTM1': 3601, 'SRTM3': 1201}

# Get the type of SRTM files or use SRTM3 by default
SRTM_TYPE = os.getenv('SRTM_TYPE', 'SRTM3')
SAMPLES = SRTM_DICT[SRTM_TYPE]

# put uncompressed hgt files in HGT_DIR, defaults to 'hgt'
HGTDIR = os.getenv('HGT_DIR', 'hgt')


def get_elevation(lat, lon):
    hgt_file = get_file_name(lat, lon)
    if hgt_file:
        return read_elevation_from_file(hgt_file, lat, lon)
    return None


def read_elevation_from_file(hgt_file, lat, lon):
    lines = int(SAMPLES - 1 - round((lat-math.floor(lat)) * (SAMPLES - 1), 0)) #lines max 'SAMPLES - 1'
    pixel = int(round((lon-math.floor(lon)) * (SAMPLES - 1), 0)) * 2 #2 bytes unsigned 16bit
    seek_val=lines*SAMPLES*2+pixel #start from the bottom left and continue upwards ;)
    with open(hgt_file, "rb") as f:
        f.seek(seek_val)
        buf = f.read(2) #read 2 bytes
        f.close()
        val = struct.unpack('>h', buf)[0]
        if val == -32768 or val == 65535:#?
            return None
        return val


def get_file_name(lat, lon):
    """
    Returns filename such as N27E086.hgt, concatenated
    with HGTDIR where these 'hgt' files are kept
    """
    ns='N' if lat >= 0 else 'S'
    ew='E' if lon >= 0 else 'W'
    if lat < 0:lat -= 1
    if lon < 0:lon -= 1
    hgt_file=f"{ns}{int(abs(lat)):02}{ew}{int(abs(lon)):03}.hgt"
    hgt_file_path = os.path.join(HGTDIR, hgt_file)
    if os.path.isfile(hgt_file_path):
        return hgt_file_path
    else:
        return None


if __name__ == '__main__':
    # Mt. Everest
    print('Mt. Everest: %d' % get_elevation(27.988056, 86.925278))
    # Kanchanjunga
    print('Kanchanjunga: %d' % get_elevation(27.7025, 88.146667))
