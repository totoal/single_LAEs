import pandas as pd

def load_s_cats(cat_list=['minijpas', 'jnep']):
    '''
    Loads the single mode catalogs of miniJPAS and J-NEP
    (specify one or both, default=both).
    '''
    # Column names
    columns = ['tileid', 'filterid', 'flags', 'number', 'RA', 'DEC',
               'x_im', 'y_im', 'background', 'threshold', 'flux',
               'flux_relerr', 'mask_flags']
    types_list = ['int', 'int', 'int', 'int', 'float', 'float', 'float',
                  'float', 'float', 'float', 'float', 'float', 'int']
    types_dict = {}
    for colname, dt in zip(columns, types_list):
        types_dict[colname] = dt

    merged_cat = pd.DataFrame([])

    for cat_name in cat_list:
        cat = pd.read_csv(f'csv/{cat_name}.Flambda_single.csv', header=1,
                          names=columns)
        cat = cat.astype(types_dict)

        # Convert fluxes to erg s^-1 cm^-2 units and relerr to err
        cat['flux'] = cat['flux'] * 1e-19
        cat['flux_err'] = cat['flux_relerr'] * cat['flux']
        cat = cat.drop('flux_relerr', axis=1)

        # Drop flagged
        mflags = (cat['mask_flags'] + cat['flags']) == 0
        cat = cat[mflags]

        merged_cat = pd.concat([merged_cat, cat])

    return merged_cat


if __name__ == '__main__':
    load_s_cats()