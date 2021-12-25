# corporate income tax Yr 2021
# ref https://www.rd.go.th/fileadmin/tax_pdf/cit/2563/251263Ins50.pdf (Page#14)
# #1 General case 
## The corporate income tax rate in Thailand is 20 % on net profit 
# #2.1 Small company 
## 1.0 - 300000, 0.0
## 300000.1 - 3000000, 0.15
## 3000000.1 - 9.99*10**10, 0.2

import pandas as pd
import numpy as np
#pd.options.display.float_format = '{:,.2f}'.format

taxtabledata =[
     [0.01, 300000.0, 0.0],
     [300000.01, 3000000.0, 0.15],
     [3000000.01, 9.999999*10**15, 0.2]
 ]

taxdf =pd.DataFrame(
{'Lower': {0: 0.01, 1: 300000.01, 2: 3000000.01},
 'Higher': {0: 300000.0, 1: 3000000.0, 2: 9999999000000000.0},
 'Taxrate': {0: 0.0, 1: 0.15, 2: 0.2}}
)

cittax = lambda ac, ri, cr : (ri*cr)+ac if ~np.isnan(ac) else 0
taxdf['ranginterval'] = [int(x) - int(y) for x , y in zip(taxdf['Higher'] , taxdf['Lower'])]
taxdf['accumtaxbase'] = taxdf['ranginterval'].cumsum()
taxdf['maxtaxinterval'] = taxdf['ranginterval'] * taxdf['Taxrate']
taxdf['accumtax'] = taxdf['maxtaxinterval'].cumsum()


def cal_cit_2564(netprofit)-> float:

    if np.isnan(taxdf[taxdf['Higher']<=netprofit]['accumtax'].max()):
        # print(f'{netprofit} net profit < 300,000' )
        return 0
    else :
        # print(netprofit)
        tax = taxdf[(taxdf['Lower']<= netprofit) & (taxdf['Higher']>= netprofit)]
        # print(tax)
        return cittax(taxdf[taxdf['Higher']<=netprofit]['accumtax'].max(), 
                     netprofit - int(tax['Lower']),tax['Taxrate'].max())

def main():
    netprofit = 299900.0
    while netprofit <= 15000000.0:
        # print(netprofit)
        taxcal =  cal_cit_2564(netprofit)
        print(f'net profit :{netprofit:,.0f} Cit :{taxcal:,.2f}')
        netprofit+=10000.0

if __name__ =='__main__':
    main()
