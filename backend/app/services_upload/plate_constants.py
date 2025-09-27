import numpy as np
import pandas as pd

def calculate(ar, dec, x, y):
  X3 = x*x*x
  X2Y = x*x*y
  XY2 = x*y*y
  Y3 = y*y*y
  X2 = x*x
  XY = x*y
  Y2 = y*y
  X = x
  Y = y
  ind = np.ones(x.size) 
 
  # Creamos la matriz de diseño X
  MX = np.column_stack((X3, X2Y, XY2, Y3, X2, XY, Y2, X, Y, ind))

  # Calculamos los coeficientes usando la fórmula de mínimos cuadrados
  a_est_AR = np.linalg.inv(MX.T @ MX) @ MX.T @ ar
  a_est_DEC = np.linalg.inv(MX.T @ MX) @ MX.T @ dec
  return [a_est_AR, a_est_DEC] 


def calculate_plate(df):
  # Obtener un array de una columna
  arr_ar = df['ar_app'].to_numpy()
  arr_dec = df['dec_app'].to_numpy()
  arr_x = df['field_x'].to_numpy()
  arr_y = df['field_y'].to_numpy()
  [pc_ar, pc_dec] = calculate(arr_ar, arr_dec, arr_x, arr_y)
  coefs_name = ['X³', 'X²Y', 'XY²', 'Y³', 'X²', 'XY', 'Y²', 'X', 'Y', 'ind'] 
  coefs = pd.DataFrame({
    'Coef': coefs_name,
    'AR': pc_ar,
    'DEC': pc_dec
})
  
  def calculate_residues(ra, dec, x, y, pc_ar, pc_dec):
    ar_res = ra - ((pc_ar[0] * x * x) + (pc_ar[1] * y * y) + (pc_ar[2] * x * y  ) + (pc_ar[3] * x) + (pc_ar[4] * y) + pc_ar[5]) 
    dec_res = dec - ((pc_dec[0] * x * x) + (pc_dec[1] * y * y) + (pc_dec[2] * x * y  ) + (pc_dec[3] * x) + (pc_dec[4] * y) + pc_dec[5])
    return [ar_res, dec_res] 

  df[['ra_resid', 'dec_resid']] = df.apply(lambda row: calculate_residues(row['ar_app'], row['dec_app'], row['field_x'], row['field_y'], pc_ar, pc_dec), axis=1, result_type='expand')
  return df, coefs
