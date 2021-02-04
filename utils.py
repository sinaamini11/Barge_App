def plot_barge(barge, loaded_fb, unloaded_fb, material):
    import pandas as pd
    from scipy.interpolate import interp1d
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from matplotlib import rcParams
    rcParams['font.family'] = 'arial'
    rcParams['font.size'] = 8
    
    tables = pd.read_excel('tables/Ingram Barge Company Barges.xlsx')
    
    tables.set_index('Barge Number', inplace=True)
    
    tables['Hull Depth'] = tables['Dimensions'].apply(lambda x: int(x[-3:-1]))
    
    hull_depth = tables.loc[barge, 'Hull Depth']
    hull_type = tables.loc[barge, 'Hull Type']
    
    draft_columns = ['8 feet. 0"', '8 ft 6"', '9 ft 0" ', '9 ft 3"',
                      '9 ft 6"', '9 ft 9"', '10 ft 0"', '10 ft 3"',
                      '10 ft 6"', '11 ft 0"'] 
    
    draft_values = np.array([8.0, 8.5, 9.0, 9.25, 9.5, 9.75, 10.0, 10.25,
                              10.5, 11.0])
    
    displacements = tables.loc[barge, draft_columns].values
    
    fb_values = hull_depth - draft_values
    
    assert unloaded_fb < hull_depth
    assert loaded_fb > 0
    
    interp_fun = interp1d(x=fb_values, y=displacements, fill_value='extrapolate')
    
    loaded_displacement = np.rint(interp_fun(loaded_fb)).astype('int64')
    unloaded_displacement = np.rint(interp_fun(unloaded_fb)).astype('int64')
    
    net_displacement = loaded_displacement - unloaded_displacement
    
    plt.figure()
    ax = plt.gca()
    plt.scatter(displacements, fb_values, ec='tab:blue', fc='None', 
                label='Table Values', s=20, zorder=100)
    
    fb = np.linspace(0, hull_depth, 100)
    disp = interp_fun(fb)
    plt.plot(disp, fb, lw=0.8, ls='--', c='tab:gray', label='Interpolation')
    plt.scatter(interp_fun(np.array([loaded_fb, unloaded_fb])),
                        np.array([loaded_fb, unloaded_fb]), s= 12, 
                        label='Measurements',
                        marker='x', zorder=200, c='tab:red')
    
    plt.title(f'Barge: {barge}, Hull Type: {hull_type}')
    
    ax.invert_yaxis()
    
    secay = ax.secondary_yaxis('right', functions=(lambda x: hull_depth-x,
                                                   lambda x: hull_depth-x))
    
    ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    plt.xlabel('Displacement (ton)')
    plt.ylabel('Freeboard (ft)')
    secay.set_ylabel('Draft (ft)')
    plt.tight_layout()
    plt.annotate((f'{loaded_fb} ft\n'+
                  '{:,} tons'.format(loaded_displacement)), 
                 xy=(loaded_displacement, loaded_fb),
                 xytext=(5,-10),
                 textcoords=('offset pixels'),
                 ha='left', va='top', arrowprops={'arrowstyle':'-|>', 'lw':1,
                                                  'fc':'black'},
                 bbox={'fc':'gray', 'alpha':0.3,'ec':'None', 'pad':2})
    
    plt.annotate((f'{unloaded_fb} ft\n'+
                  '{:,} tons'.format(unloaded_displacement)), 
                 xy=(unloaded_displacement, unloaded_fb),
                 xytext=(5,-10),
                 textcoords=('offset pixels'),
                 ha='left', va='top', arrowprops={'arrowstyle':'-|>', 'lw':1,
                                                  'fc':'black'},
                 bbox={'fc':'gray', 'alpha':0.3,'ec':'None', 'pad':2})
    
    plt.text(x=0.03, y=0.95,
             s=('Net Displacement: {:,} tons\n'.format(net_displacement)+
                f'Material: {material}'), va='top',
             transform=ax.transAxes,
             fontsize=8)
    
    
    plt.savefig('./templates/result.svg')

if __name__ =='__main__':
    plot_barge(barge='ING 1959', loaded_fb=2.0, unloaded_fb=10, material='Bedding Stone')
