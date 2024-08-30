from os.path import join
from jinja2 import Template
from astropy.io import fits, ascii

CUBESPATH = '/PATH/TO/CUBES'
MASTERLIST = '/PATH/TO/MASTERLIST'
CUBESPATH = '/storage/hdd/scubes_S20/'
MASTERLIST = '/storage/hdd/backup/dhubax/dev/astro/splus/s-cubes/workdir/masterlist_Hydra-Fornax_v02.csv'
ML_COLS = ['SNAME', 'NAME', 'FIELD', 'RA__deg', 'DEC__deg', 'REDSHIFT', 'SIZE__pix']

if __name__ == '__main__':
    ml = ascii.read(MASTERLIST)
    n_ml = len(ml)

    index_template_filename = 'index.template.html'
    with open(index_template_filename, 'r') as f:
        index_template = Template(f.read())    

    object_template_filename = 'object.template.html'
    with open(object_template_filename, 'r') as f:
        object_template = Template(f.read())    

    scubes = []
    for i in range(n_ml):
        gal_ml = ml[i]
        scube = {col: gal_ml[col] for col in ML_COLS}
        h = fits.getheader(join(CUBESPATH, f'{gal_ml["SNAME"]}_cube.fits'), 0)
        scube['SIZE'] = h.get('SIZE')
        with open(f'{gal_ml["SNAME"]}.html', 'w') as f:
            f.write(object_template.render(dict(scube=scube)))
        scubes.append(scube)
    with open('index.html', 'w') as f:
        f.write(index_template.render(dict(scubes=scubes)))